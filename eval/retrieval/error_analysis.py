"""Retrieval error analysis: where is the gold page for every question, and why was it missed?

Prints one line per answerable question and writes a detailed section for every miss
to results/error_analysis.md (to be read and categorised by hand).

  docker compose exec -e PYTHONPATH=/app -w /eval api python -m retrieval.error_analysis
"""
import json
import re
from pathlib import Path

from core.config import settings
from rag.retriever import load_chunks_from_json
from dataset.validate import load_questions
from retrieval.fusion import chunks_to_pages
from retrieval.report import fuse, md_table

EVAL_DIR = Path(__file__).parent.parent
RUN_PATH = EVAL_DIR / "runs" / "retrieval.json"
RERANK_PATH = EVAL_DIR / "runs" / "rerank.json"
OUT_PATH = EVAL_DIR / "results" / "error_analysis.md"
MISS_RANK = 5      # a question is a "miss" if no gold page is in the hybrid top 5 pages
CATEGORIES = ("chunk boundary | terminology / synonyms | table | answer spans several pages | "
              "ambiguous question | wrong label | other")


def first_gold_rank(hits, gold_pages):
    """Rank (1 = best) of the first gold page in the page ranking, or None if absent."""
    for rank, page in enumerate(chunks_to_pages(hits), start=1):
        if page in gold_pages:
            return rank
    return None


def chunk_rank(hits, chunk_index):
    """Rank of one chunk inside a list of hits, or None."""
    for rank, hit in enumerate(hits, start=1):
        if hit["chunk_index"] == chunk_index:
            return rank
    return None


def show(rank):
    return "-" if rank is None else str(rank)


def snippet(text, length=220):
    return " ".join(text.split())[:length]


def main():
    with open(RUN_PATH, encoding="utf-8") as f:
        run = json.load(f)
    app = run["meta"]["app_config"]
    bm25_w, vector_w, top_k, depth = (app["bm25_weight"], app["vector_weight"],
                                      app["top_k"], run["meta"]["depth"])
    questions = {q["id"]: q for q in load_questions()}
    chunks = load_chunks_from_json(settings.CHUNKS_PATH)
    chunk_text = {c.metadata["chunk_index"]: c.page_content for c in chunks}
    chunks_on_page = {}
    for c in chunks:
        chunks_on_page.setdefault(c.metadata["page"], []).append(c.metadata["chunk_index"])
    reranked = {}
    if RERANK_PATH.exists():
        with open(RERANK_PATH, encoding="utf-8") as f:
            reranked = {r["id"]: r["reranked"] for r in json.load(f)["questions"]}

    print(f"{'id':8s} {'type':10s} {'gold':10s} {'bm25':>5s} {'vector':>6s} {'hybrid':>6s} "
          f"{'rerank':>6s}  in deployed context")
    sections, table_rows, n_miss = [], [], 0
    sections, n_miss = [], 0
    for record in run["questions"]:
        if record["type"] == "unanswerable":
            continue
        q = questions[record["id"]]
        gold = q["gold_pages"]
        hybrid = fuse(record, bm25_w, vector_w, depth)
        context = fuse(record, bm25_w, vector_w, top_k)             # what the app sends to the LLM
        ranks = {"bm25": first_gold_rank(record["bm25"], gold),
                 "vector": first_gold_rank(record["vector"], gold),
                 "hybrid": first_gold_rank(hybrid, gold),
                 "rerank": first_gold_rank(reranked[q["id"]], gold) if reranked else None}
        in_context = bool(set(gold) & {h["page"] for h in context})
        print(f"{q['id']:8s} {q['type']:10s} {str(gold):10s} {show(ranks['bm25']):>5s} "
              f"{show(ranks['vector']):>6s} {show(ranks['hybrid']):>6s} {show(ranks['rerank']):>6s}  "
              f"{'yes' if in_context else 'NO'}")

        is_miss = ranks["hybrid"] is None or ranks["hybrid"] > MISS_RANK or not in_context
        table_rows.append([q["id"], q["type"], gold, show(ranks["bm25"]), show(ranks["vector"]),
                           show(ranks["hybrid"]), show(ranks["rerank"]),
                           "yes" if in_context else "NO", "MISS" if is_miss else ""])
        
        if not is_miss:
            continue
        n_miss += 1

        # Which question words does the app's BM25 tokenizer (plain text.split()) fail to match?
        gold_text = " ".join(chunk_text[i] for page in gold for i in chunks_on_page.get(page, []))
        gold_tokens = set(gold_text.split())
        gold_normalised = set(re.findall(r"[a-z0-9]+", gold_text.lower()))
        exact = [t for t in q["question"].split() if t in gold_tokens]
        only_normalised = [t for t in q["question"].split() if t not in gold_tokens
                           and re.sub(r"[^a-z0-9]", "", t.lower()) in gold_normalised]

        lines = [f"## {q['id']} ({q['type']}) - gold pages {gold}",
                 f"**Question:** {q['question']}",
                 f"**Reference answer:** {q['reference_answer']}",
                 f"**Rank of first gold page** (pages, 1 = best, - = not in top {depth} chunks): "
                 f"BM25 {show(ranks['bm25'])} | vector {show(ranks['vector'])} | "
                 f"hybrid {show(ranks['hybrid'])} | reranked {show(ranks['rerank'])} | "
                 f"in deployed context: {'yes' if in_context else 'NO'}",
                 f"**BM25 token match with the gold page:** exact: {exact} | "
                 f"only after lowercasing / stripping punctuation: {only_normalised}",
                 "**Chunks on the gold page(s):**"]
        for page in gold:
            for index in chunks_on_page.get(page, []):
                lines.append(f"- p.{page} chunk {index}: BM25 rank {show(chunk_rank(record['bm25'], index))}, "
                             f"vector rank {show(chunk_rank(record['vector'], index))} - "
                             f"`{snippet(chunk_text[index])}`")
        lines.append("**Top 5 pages the hybrid ranking returned instead:**")
        seen_pages = []
        for hit in hybrid:
            if hit["page"] not in seen_pages:
                seen_pages.append(hit["page"])
                lines.append(f"- p.{hit['page']} (chunk {hit['chunk_index']}): "
                             f"`{snippet(chunk_text[hit['chunk_index']])}`")
            if len(seen_pages) == 5:
                break
        lines.append(f"**Category** ({CATEGORIES}): \n\n**Note:** ")
        sections.append("\n\n".join(lines))

    header = (f"# Retrieval error analysis\n\n{n_miss} misses: no gold page in the hybrid top "
              f"{MISS_RANK} pages, or no gold page in the deployed context.")
    table_rows.sort(key=lambda row: row[-1] != "MISS")              # misses first, rest in order
    table = md_table(["id", "type", "gold pages", "BM25", "vector", "hybrid", "reranked",
                      "in deployed context", "miss"], table_rows)
    overview = (header + "\n\nRank of the first gold page per ranking (1 = best, - = not in the "
                f"top {depth} chunks).\n\n" + table)
    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text("\n\n---\n\n".join([overview] + sections) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()