"""Generate candidate synthetic questions for the golden dataset.

Smoke test (2 calls, prints only, writes nothing):
  docker compose exec -e PYTHONPATH=/app -w /eval api python -m dataset.make_synthetic --limit 2
Full run (writes candidates.jsonl, candidates_review.md, candidates_meta.json):
  docker compose exec -e PYTHONPATH=/app -w /eval api python -m dataset.make_synthetic
"""
import argparse
import json
import random
import re
from pathlib import Path

from langchain_anthropic import ChatAnthropic

from core.config import settings                    # app config (API key, chunks path)
from rag.generator import estimate_cost, extract_usage  # app's own usage / cost functions
from rag.retriever import load_chunks_from_json     # the same chunks BM25 is built from
from common.llm import message_text, parse_json_reply

HERE = Path(__file__).parent
QUESTION_MODEL = "claude-sonnet-5-5"   # not the app's generator model (claude-sonnet-5)
PROMPT_VERSION = "synq_v1"
SEED = 42
MIN_CHARS = 400                        # very short chunks rarely hold a full fact
SKIP_PAGES = {1, 2, 402, 403, 404}     # cover, table of contents, legal pages

PROMPT = """You are helping build a test set for a search system over the SAP Profitability and Performance Management (SAP PaPM) Application Help manual.

Below is one full PAGE of the manual and, inside it, one TARGET PASSAGE.

<page>
<<PAGE>>
</page>

<target_passage>
<<PASSAGE>>
</target_passage>

Write ONE question that a SAP PaPM consultant could realistically ask in a support chat, and that the TARGET PASSAGE answers.

Rules:
1. The answer must be stated in the target passage. The rest of the page is only there so you understand which feature the passage belongs to.
2. Paraphrase. Describe the need or the symptom in your own words; do not copy sentences or distinctive phrases from the passage. Product terms that a user would have to use anyway (for example the name of a function) are allowed.
3. The question must stand on its own. The person asking has not seen the manual: never write "according to the passage", "in this section", "the table above".
4. The question must be specific enough to have one clear answer in a 400-page manual. Name the feature or function it is about.
5. Also write a reference answer: 1-3 sentences, using only facts from the target passage.
6. If the target passage cannot support such a question (table fragment without context, example data only, navigation or boilerplate text), skip it.

Reply with a single JSON object and nothing else:
{"skip": false, "question": "...", "reference_answer": "..."}
or
{"skip": true, "reason": "..."}"""


def eligible_chunks(chunks):
    """Drop cover / TOC / legal pages and very short chunks."""
    return [c for c in chunks
            if c.metadata["page"] not in SKIP_PAGES and len(c.page_content) >= MIN_CHARS]


def sample_stratified(chunks, n, seed):
    """Cut the document into n equal slices and pick one random chunk from each slice."""
    rng = random.Random(seed)
    slice_size = len(chunks) / n
    return [rng.choice(chunks[int(i * slice_size):int((i + 1) * slice_size)]) for i in range(n)]


def build_prompt(chunk, all_chunks):
    page = chunk.metadata["page"]
    page_text = "\n".join(c.page_content for c in all_chunks if c.metadata["page"] == page)
    return PROMPT.replace("<<PAGE>>", page_text).replace("<<PASSAGE>>", chunk.page_content)


def lexical_overlap(question, passage):
    """Share of the question's longer words (4+ letters) that also occur in the passage."""
    words = lambda s: set(re.findall(r"[a-z0-9]{4,}", s.lower()))
    q_words = words(question)
    return round(len(q_words & words(passage)) / len(q_words), 2) if q_words else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=45, help="how many chunks to sample")
    parser.add_argument("--limit", type=int, default=None, help="smoke test: only the first N")
    parser.add_argument("--force", action="store_true", help="overwrite existing candidates")
    args = parser.parse_args()

    out_path = HERE / "candidates.jsonl"
    if args.limit is None and out_path.exists() and not args.force:
        raise SystemExit(f"{out_path} already exists. Use --force to overwrite it.")

    all_chunks = load_chunks_from_json(settings.CHUNKS_PATH)
    sample = sample_stratified(eligible_chunks(all_chunks), args.n, SEED)
    if args.limit:
        sample = sample[:args.limit]

    # max_tokens is generous because thinking tokens also count against it.
    llm = ChatAnthropic(model=QUESTION_MODEL, api_key=settings.ANTHROPIC_API_KEY, max_tokens=4096)
    prompts = [build_prompt(c, all_chunks) for c in sample]
    replies = llm.batch(prompts, config={"max_concurrency": 5}, return_exceptions=True)

    candidates, skipped, failed, cost = [], [], [], 0.0
    for i, (chunk, reply) in enumerate(zip(sample, replies), start=1):
        cid, page = f"syn-{i:02d}", chunk.metadata["page"]
        if isinstance(reply, Exception):
            failed.append((cid, page, repr(reply)))
            continue
        cost += estimate_cost(extract_usage(reply), QUESTION_MODEL)
        try:
            data = parse_json_reply(message_text(reply))
            if data.get("skip"):
                skipped.append((cid, page, data.get("reason", "")))
                continue
            question, answer = data["question"].strip(), data["reference_answer"].strip()
        except (ValueError, KeyError, AttributeError) as e:
            stop = reply.response_metadata.get("stop_reason")
            failed.append((cid, page, f"{e!r} (stop_reason={stop})"))
            continue
        candidates.append({
            "id": cid,
            "question": question,
            "type": "synthetic",
            "subtype": None,
            "gold_pages": [page],
            "reference_answer": answer,
            "source_chunk_index": chunk.metadata["chunk_index"],
        })

    print(f"generated={len(candidates)} skipped={len(skipped)} failed={len(failed)} "
          f"cost_usd={cost:.4f}")
    for cid, page, why in skipped:
        print(f"  SKIP {cid} p.{page}: {why}")
    for cid, page, why in failed:
        print(f"  FAIL {cid} p.{page}: {why}")

    if args.limit:  # smoke test: show the result, write nothing
        for c in candidates:
            print(json.dumps(c, ensure_ascii=False, indent=2))
        return

    with open(out_path, "w", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # Human-readable file for the manual review: question next to its source passage.
    passages = {c.metadata["chunk_index"]: c.page_content for c in sample}
    with open(HERE / "candidates_review.md", "w", encoding="utf-8") as f:
        for c in candidates:
            passage = passages[c["source_chunk_index"]]
            f.write(f"## {c['id']} | page {c['gold_pages'][0]} | "
                    f"lexical overlap {lexical_overlap(c['question'], passage)}\n\n"
                    f"**Q:** {c['question']}\n\n**A:** {c['reference_answer']}\n\n"
                    f"```\n{passage}\n```\n\n")

    meta = {"model": QUESTION_MODEL, "prompt_version": PROMPT_VERSION, "seed": SEED,
            "n_sampled": len(sample), "n_generated": len(candidates),
            "n_skipped": len(skipped), "n_failed": len(failed), "cost_usd": round(cost, 4)}
    with open(HERE / "candidates_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"wrote {out_path.name}, candidates_review.md, candidates_meta.json")


if __name__ == "__main__":
    main()