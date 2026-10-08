"""R4: cross-encoder reranker on top of the app's hybrid ranking.

Takes the top-30 chunks of the hybrid ranking (app weights, deep fusion), scores every
(question, chunk) pair with a cross-encoder and compares the new order with the old one.

  docker compose exec -e PYTHONPATH=/app -w /eval api python -m retrieval.rerank
"""
import json
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
from sentence_transformers import CrossEncoder

from core.config import settings
from rag.retriever import load_chunks_from_json
from dataset.validate import load_questions
from retrieval.metrics import mean, paired_bootstrap
from retrieval.report import column, context_stats, fuse, md_table, score_pages
from retrieval.fusion import chunks_to_pages

EVAL_DIR = Path(__file__).parent.parent
RUN_PATH = EVAL_DIR / "runs" / "retrieval.json"
RERANK_PATH = EVAL_DIR / "runs" / "rerank.json"
RESULTS_DIR = EVAL_DIR / "results"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
POOL_SIZE = 30                      # how many fused chunks the reranker gets to reorder
METRICS = ["recall@5", "recall@10", "mrr@10", "ndcg@10"]


def main():
    with open(RUN_PATH, encoding="utf-8") as f:
        run = json.load(f)
    app = run["meta"]["app_config"]
    bm25_w, vector_w, depth = app["bm25_weight"], app["vector_weight"], run["meta"]["depth"]
    gold = {q["id"]: q["gold_pages"] for q in load_questions()}
    chunks = load_chunks_from_json(settings.CHUNKS_PATH)
    chunk_text = {c.metadata["chunk_index"]: c.page_content for c in chunks}
    chunk_chars = {index: len(text) for index, text in chunk_text.items()}

    model = CrossEncoder(RERANK_MODEL, device="cpu")
    model.predict([("warm-up question", "warm-up passage")])   # keep model start-up out of timings

    # ---- score every (question, chunk) pair in the pool; all 50 questions -------------
    reranked_runs = []
    for record in run["questions"]:
        pool = fuse(record, bm25_w, vector_w, depth)[:POOL_SIZE]
        pairs = [(record["question"], chunk_text[hit["chunk_index"]]) for hit in pool]
        start = time.perf_counter()
        scores = np.asarray(model.predict(pairs), dtype=float)
        elapsed_ms = (time.perf_counter() - start) * 1000
        new_order = np.argsort(-scores, kind="stable")          # highest score first, ties keep fused order
        reranked_runs.append({
            "id": record["id"], "type": record["type"],
            "pool": pool,                                        # fused order (the baseline)
            "reranked": [dict(pool[i], rerank_score=round(float(scores[i]), 4)) for i in new_order],
            "rerank_ms": round(elapsed_ms, 1),
        })

    meta = {"rerank_model": RERANK_MODEL, "pool_size": POOL_SIZE,
            "base": f"weighted RRF {bm25_w}/{vector_w}, depth {depth}",
            "retrieval_commit": run["meta"]["git_commit"],
            "sentence_transformers": version("sentence-transformers")}
    with open(RERANK_PATH, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "questions": reranked_runs}, f)

    # ---- metrics on the answerable questions ------------------------------------------
    answerable = [dict(r, gold_pages=gold[r["id"]]) for r in reranked_runs if r["type"] != "unanswerable"]
    base = [score_pages(chunks_to_pages(r["pool"]), r["gold_pages"]) for r in answerable]
    after = [score_pages(chunks_to_pages(r["reranked"]), r["gold_pages"]) for r in answerable]
    in_pool = mean([1.0 if set(r["gold_pages"]) & {h["page"] for h in r["pool"]} else 0.0
                    for r in answerable])

    rows = []
    for metric in METRICS:
        diff, low, high = paired_bootstrap(column(base, metric), column(after, metric))
        excludes_zero = "yes" if (low > 0 or high < 0) else "no"
        rows.append([metric, f"{mean(column(base, metric)):.3f}", f"{mean(column(after, metric)):.3f}",
                     f"{diff:+.3f}", f"[{low:+.3f}, {high:+.3f}]", excludes_zero])
    out = [f"# R4 - cross-encoder reranker\n\nModel `{RERANK_MODEL}` on CPU, reordering the top "
           f"{POOL_SIZE} chunks of the hybrid ranking ({bm25_w}/{vector_w}). "
           f"{len(answerable)} answerable questions.\n\n"
           f"Gold page somewhere in the pool (ceiling for the reranker): {in_pool:.3f}",
           "## Ranking quality\n\n"
           + md_table(["metric", "hybrid", "hybrid + reranker", "difference", "95% CI", "CI excludes 0"], rows)]

    # ---- what the LLM would see if only the top N chunks were sent --------------------
    rows = []
    for n in [3, 5, 8, 10]:
        before = context_stats(answerable, [r["pool"][:n] for r in answerable], chunk_chars)
        with_rerank = context_stats(answerable, [r["reranked"][:n] for r in answerable], chunk_chars)
        rows.append([n, f"{before['hit']:.3f}", f"{with_rerank['hit']:.3f}", f"{with_rerank['tokens']:.0f}"])
    out.append("## Gold page in context when only the top N chunks are sent\n\n"
               + md_table(["top N chunks", "hybrid", "hybrid + reranker", "est. tokens (reranked)"], rows))

    times = [r["rerank_ms"] for r in reranked_runs]
    out.append(f"## Added latency\n\nReranking {POOL_SIZE} chunks per question on CPU: "
               f"p50 {np.percentile(times, 50):.0f} ms, p95 {np.percentile(times, 95):.0f} ms "
               f"(over {len(times)} questions).")

    report = "\n\n".join(out) + "\n"
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "rerank_report.md").write_text(report, encoding="utf-8")
    print(report)
    print("wrote runs/rerank.json and results/rerank_report.md")


if __name__ == "__main__":
    main()