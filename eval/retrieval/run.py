"""Snapshot retrieval for every question: top-100 from BM25 and top-100 from the vector store.

All fusion variants and metrics are later computed offline from this one file.

  docker compose exec -e PYTHONPATH=/app -e GIT_COMMIT=$(git rev-parse --short HEAD) \
      -w /eval api python -m retrieval.run
"""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np

from core.config import settings
from common.app_adapter import bm25_top, build_dup_map, get_components, vector_top
from dataset.validate import QUESTIONS_PATH, load_questions
from retrieval.fusion import RRF_C, weighted_rrf

DEPTH = 100
RUN_PATH = Path(__file__).parent.parent / "runs" / "retrieval.json"
PACKAGES = ["langchain-classic", "langchain-community", "langchain-postgres",
            "langchain-huggingface", "rank-bm25", "sentence-transformers"]


def main():
    questions = load_questions()
    ensemble, bm25, store = get_components()
    dup_map = build_dup_map(bm25)
    app_weights = [settings.BM25_WEIGHT, settings.VECTOR_WEIGHT]

    vector_top(store, "warm-up query", 5, dup_map)   # first call is slow; keep it out of timings

    records, mismatches = [], []
    for q in questions:
        bm25_hits, bm25_ms = bm25_top(bm25, q["question"], DEPTH, dup_map)
        vector_hits, embed_ms, search_ms = vector_top(store, q["question"], DEPTH, dup_map)

        # Parity: what the real app retrieves vs. our offline fusion of the two top-K lists.
        start = time.perf_counter()
        app_docs = ensemble.invoke(q["question"])
        app_ms = (time.perf_counter() - start) * 1000
        app_order = [d.metadata["chunk_index"] for d in app_docs]
        offline = weighted_rrf([bm25_hits[:settings.TOP_K], vector_hits[:settings.TOP_K]],
                               app_weights)
        offline_order = [h["chunk_index"] for h in offline]
        if app_order != offline_order:
            mismatches.append((q["id"], app_order, offline_order))

        records.append({
            "id": q["id"], "type": q["type"], "subtype": q["subtype"],
            "question": q["question"], "gold_pages": q["gold_pages"],
            "bm25": bm25_hits, "vector": vector_hits,
            "app_context": app_order,
            "timing_ms": {"bm25": round(bm25_ms, 2), "embed_query": round(embed_ms, 2),
                          "vector_search": round(search_ms, 2), "app_hybrid": round(app_ms, 2)},
        })

    meta = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": os.environ.get("GIT_COMMIT", "unknown"),
        "questions_sha256": hashlib.sha256(QUESTIONS_PATH.read_bytes()).hexdigest()[:12],
        "n_questions": len(questions),
        "depth": DEPTH,
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "app_config": {"top_k": settings.TOP_K, "bm25_weight": settings.BM25_WEIGHT,
                       "vector_weight": settings.VECTOR_WEIGHT, "rrf_c": RRF_C},
        "n_chunks": len(bm25.docs),
        "chunks_ingested_at": bm25.docs[0].metadata.get("ingested_at"),
        "score_meaning": {"bm25": "BM25Okapi score, higher is better",
                          "vector": "cosine distance, lower is better"},
        "parity_ok": len(questions) - len(mismatches),
        "versions": {name: version(name) for name in PACKAGES},
    }
    RUN_PATH.parent.mkdir(exist_ok=True)
    with open(RUN_PATH, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "questions": records}, f)

    # Summary for a quick sanity check (no quality metrics here - those come from report.py).
    print(f"questions: {len(questions)} | depth: {DEPTH} | app config: TOP_K={settings.TOP_K}, "
          f"weights {settings.BM25_WEIGHT}/{settings.VECTOR_WEIGHT}")
    print(f"parity (offline fusion == app): {meta['parity_ok']}/{len(questions)}")
    for qid, app_order, offline_order in mismatches:
        print(f"  MISMATCH {qid}\n    app:     {app_order}\n    offline: {offline_order}")
    sizes = [len(r["app_context"]) for r in records]
    print(f"context size as deployed (chunks): min {min(sizes)}, "
          f"mean {sum(sizes) / len(sizes):.1f}, max {max(sizes)}")
    print("latency ms (p50 / p95):")
    for stage in ["bm25", "embed_query", "vector_search", "app_hybrid"]:
        values = [r["timing_ms"][stage] for r in records]
        print(f"  {stage:14s} {np.percentile(values, 50):7.1f} / {np.percentile(values, 95):7.1f}")
    print(f"wrote {RUN_PATH}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()