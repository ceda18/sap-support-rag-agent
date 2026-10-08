"""Retrieval report (R1, R2, R3, R5, R7), computed offline from runs/retrieval.json.

No database and no LLM: only the snapshot, the gold labels and arithmetic.

  docker compose exec -e PYTHONPATH=/app -w /eval api python -m retrieval.report
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                                # write PNG files, no display needed
import matplotlib.pyplot as plt

from core.config import settings
from rag.retriever import load_chunks_from_json      # chunk texts, for context-size estimates
from dataset.validate import load_questions
from retrieval.fusion import chunks_to_pages, weighted_rrf
from retrieval.metrics import (mean, ndcg_at_k, paired_bootstrap, recall_at_k,
                               reciprocal_rank_at_k)

EVAL_DIR = Path(__file__).parent.parent
RUN_PATH = EVAL_DIR / "runs" / "retrieval.json"
RESULTS_DIR = EVAL_DIR / "results"
METRICS = ["recall@5", "recall@10", "recall@20", "mrr@10", "ndcg@10"]


def score_pages(pages, gold):
    """All retrieval metrics for one question."""
    return {
        "recall@5": recall_at_k(pages, gold, 5),
        "recall@10": recall_at_k(pages, gold, 10),
        "recall@20": recall_at_k(pages, gold, 20),
        "mrr@10": reciprocal_rank_at_k(pages, gold, 10),
        "ndcg@10": ndcg_at_k(pages, gold, 10),
    }


def fuse(record, bm25_weight, vector_weight, depth):
    """The app's fusion formula over the first `depth` hits of each snapshot list."""
    return weighted_rrf([record["bm25"][:depth], record["vector"][:depth]],
                        [bm25_weight, vector_weight])


def evaluate(records, ranker):
    """ranker(record) -> ranked hits. Returns one metrics dict per question, in order."""
    return [score_pages(chunks_to_pages(ranker(r)), r["gold_pages"]) for r in records]


def column(per_question, metric):
    return [scores[metric] for scores in per_question]


def has_boosted_duplicate(record, fused, depth):
    """True if a chunk in the fused top 10 has text that occurs 2+ times inside ONE list.

    The app's formula adds the scores of identical-text chunks, so such a chunk can
    jump ahead of everything else. Rare at TOP_K=5, more likely with deep lists.
    """
    repeated = set()
    for hits in (record["bm25"][:depth], record["vector"][:depth]):
        keys = [h["dup_of"] for h in hits]
        repeated |= {key for key in keys if keys.count(key) > 1}
    return any(h["dup_of"] in repeated for h in fused[:10])


def context_stats(records, contexts, chunk_chars):
    """What the LLM would see: is a gold page in the context, and how big is the context."""
    in_context = [1.0 if set(r["gold_pages"]) & {h["page"] for h in ctx} else 0.0
                  for r, ctx in zip(records, contexts)]
    return {
        "hit": mean(in_context),
        "chunks": mean([len(ctx) for ctx in contexts]),
        "pages": mean([len(chunks_to_pages(ctx)) for ctx in contexts]),
        "tokens": mean([sum(chunk_chars[h["chunk_index"]] for h in ctx) / 4 for ctx in contexts]),
    }


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines)


def main():
    with open(RUN_PATH, encoding="utf-8") as f:
        run = json.load(f)
    RESULTS_DIR.mkdir(exist_ok=True)
    app = run["meta"]["app_config"]
    depth = run["meta"]["depth"]
    bm25_w, vector_w, top_k = app["bm25_weight"], app["vector_weight"], app["top_k"]

    # Gold labels always come from questions.jsonl, so label fixes need no new snapshot.
    gold = {q["id"]: q["gold_pages"] for q in load_questions()}
    records = [dict(r, gold_pages=gold[r["id"]]) for r in run["questions"]
               if r["type"] != "unanswerable"]
    chunk_chars = {c.metadata["chunk_index"]: len(c.page_content)
                   for c in load_chunks_from_json(settings.CHUNKS_PATH)}
    out = [f"# Retrieval report\n\nSnapshot: commit `{run['meta']['git_commit']}`, "
           f"{len(records)} answerable questions, unit of relevance = page, "
           f"fusion depth = {depth} per retriever."]

    # ---- R1: four rankers, deep lists -------------------------------------------------
    hybrid_name = f"Hybrid {bm25_w}/{vector_w} (app weights)"
    rankers = {
        "BM25 only": lambda r: r["bm25"],
        "Vector only": lambda r: r["vector"],
        hybrid_name: lambda r: fuse(r, bm25_w, vector_w, depth),
        "RRF 0.5/0.5": lambda r: fuse(r, 0.5, 0.5, depth),
    }
    results = {name: evaluate(records, ranker) for name, ranker in rankers.items()}
    rows = [[name] + [f"{mean(column(per_q, m)):.3f}" for m in METRICS]
            for name, per_q in results.items()]
    boosted = sum(has_boosted_duplicate(r, fuse(r, bm25_w, vector_w, depth), depth) for r in records)
    out.append("## R1 - ranker quality\n\n" + md_table(["config"] + METRICS, rows)
               + f"\n\nDuplicate-text check: in {boosted} of {len(records)} questions a chunk whose "
                 "text repeats inside one list reached the hybrid top 10 with a summed score.")

    # ---- App as deployed: top_k per retriever, fused, nothing cut off -----------------
    deployed = context_stats(records, [fuse(r, bm25_w, vector_w, top_k) for r in records],
                             chunk_chars)
    out.append(f"## App as deployed (TOP_K={top_k} per retriever, no cut after fusion)\n\n"
               + md_table(["gold page in context", "mean chunks", "mean pages", "est. tokens"],
                          [[f"{deployed['hit']:.3f}", f"{deployed['chunks']:.1f}",
                            f"{deployed['pages']:.1f}", f"{deployed['tokens']:.0f}"]])
               + "\n\nTokens are estimated as chunk characters / 4.")

    # ---- R2: sweep the vector weight (same formula as the app) ------------------------
    sweep = []
    for step in range(11):
        w_vec = step / 10
        per_q = evaluate(records, lambda r: fuse(r, round(1 - w_vec, 1), w_vec, depth))
        sweep.append({"vector_weight": w_vec, "per_question": per_q,
                      "mrr@10": mean(column(per_q, "mrr@10")),
                      "recall@5": mean(column(per_q, "recall@5"))})
    best = max(sweep, key=lambda s: (s["mrr@10"], s["recall@5"]))
    rows = [[f"{s['vector_weight']:.1f}", f"{s['mrr@10']:.3f}", f"{s['recall@5']:.3f}"]
            for s in sweep]
    out.append("## R2 - vector weight sweep\n\n" + md_table(["vector weight", "mrr@10", "recall@5"], rows)
               + f"\n\nHighest MRR@10 at vector weight {best['vector_weight']:.1f} "
                 f"(app uses {vector_w}). Chosen on the same questions it is measured on.")

    plt.figure(figsize=(6, 4))
    weights = [s["vector_weight"] for s in sweep]
    plt.plot(weights, [s["mrr@10"] for s in sweep], marker="o", label="MRR@10")
    plt.plot(weights, [s["recall@5"] for s in sweep], marker="s", label="Recall@5")
    plt.axvline(vector_w, linestyle="--", color="gray", label=f"app weight ({vector_w})")
    plt.xlabel("vector weight (BM25 weight = 1 - vector weight)")
    plt.ylabel("mean over questions")
    plt.title("R2: weighted RRF, vector weight sweep")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "r2_weight_sweep.png", dpi=150)
    plt.close()

    # ---- R3: how much context is needed (sweep TOP_K with the app's fusion) -----------
    r3 = []
    for k in range(1, 21):
        stats = context_stats(records, [fuse(r, bm25_w, vector_w, k) for r in records], chunk_chars)
        r3.append(dict(stats, top_k=k))
    rows = [[s["top_k"], f"{s['hit']:.3f}", f"{s['chunks']:.1f}", f"{s['tokens']:.0f}"] for s in r3]
    out.append("## R3 - gold page in context vs. context size\n\n"
               + md_table(["TOP_K", "gold page in context", "mean chunks", "est. tokens"], rows)
               + "\n\nTOP_K is per retriever; the context is the fused union of both lists.")

    plt.figure(figsize=(6, 4))
    plt.plot([s["tokens"] for s in r3], [s["hit"] for s in r3], marker="o")
    for s in r3:
        if s["top_k"] in (1, 2, 3, 5, 10, 15, 20):
            plt.annotate(f"k={s['top_k']}", (s["tokens"], s["hit"]),
                         textcoords="offset points", xytext=(5, -12), fontsize=8)
    plt.scatter([deployed["tokens"]], [deployed["hit"]], color="red", zorder=3,
                label=f"deployed (TOP_K={top_k})")
    plt.xlabel("estimated context tokens (chunk characters / 4)")
    plt.ylabel("share of questions with a gold page in context")
    plt.title("R3: recall vs. context size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "r3_context_size.png", dpi=150)
    plt.close()

    # ---- R5: synthetic vs. manual questions -------------------------------------------
    rows = []
    for name, per_q in results.items():
        for qtype in ["synthetic", "manual"]:
            subset = [s for s, r in zip(per_q, records) if r["type"] == qtype]
            rows.append([name, qtype, len(subset)]
                        + [f"{mean(column(subset, m)):.3f}" for m in ["recall@5", "recall@10", "mrr@10"]])
    out.append("## R5 - by question type\n\n"
               + md_table(["config", "type", "n", "recall@5", "recall@10", "mrr@10"], rows))

    # ---- R7: paired bootstrap, B minus A ----------------------------------------------
    best_name = f"Best sweep weight ({best['vector_weight']:.1f})"
    results[best_name] = best["per_question"]
    pairs = [("BM25 only", "Vector only"), ("BM25 only", hybrid_name),
             ("Vector only", hybrid_name), (hybrid_name, "RRF 0.5/0.5"), (hybrid_name, best_name)]
    rows = []
    for name_a, name_b in pairs:
        for metric in ["mrr@10", "recall@5", "ndcg@10"]:
            diff, low, high = paired_bootstrap(column(results[name_a], metric),
                                               column(results[name_b], metric))
            excludes_zero = "yes" if (low > 0 or high < 0) else "no"
            rows.append([name_a, name_b, metric, f"{diff:+.3f}",
                         f"[{low:+.3f}, {high:+.3f}]", excludes_zero])
    out.append("## R7 - paired bootstrap (B minus A, 1000 resamples, 95% interval)\n\n"
               + md_table(["A", "B", "metric", "B - A", "95% CI", "CI excludes 0"], rows))

    # ---- write everything -------------------------------------------------------------
    report = "\n\n".join(out) + "\n"
    (RESULTS_DIR / "retrieval_report.md").write_text(report, encoding="utf-8")
    per_question = [{"id": r["id"], "type": r["type"], "gold_pages": r["gold_pages"],
                     "scores": {name: per_q[i] for name, per_q in results.items()}}
                    for i, r in enumerate(records)]
    with open(RESULTS_DIR / "retrieval_per_question.json", "w", encoding="utf-8") as f:
        json.dump({"best_vector_weight": best["vector_weight"], "questions": per_question}, f, indent=1)
    print(report)
    print("wrote results/retrieval_report.md, retrieval_per_question.json, "
          "r2_weight_sweep.png, r3_context_size.png")


if __name__ == "__main__":
    main()