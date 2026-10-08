"""Offline rank fusion, written to give exactly the same order as the app.

The app uses langchain's EnsembleRetriever.weighted_reciprocal_rank:
    score(chunk) = sum over retrievers of  weight / (rank + c),   c = 60
A "hit" here is a dict: {"chunk_index": int, "page": int, "score": float, "dup_of": int}.
"dup_of" is the dedup key. The app dedups by chunk text, so two chunks with identical
text share one "dup_of" value (the smallest chunk_index that has that text).
"""
from collections import defaultdict

RRF_C = 60  # EnsembleRetriever default; the app does not override it


def weighted_rrf(ranked_lists, weights, c=RRF_C):
    """Fuse ranked lists of hits (best first) into one list (best first).

    Same three steps as the app: (1) add weight / (rank + c) for every appearance,
    (2) keep the first hit seen for each key, lists read in the given order,
    (3) sort by score, highest first. Python's sort is stable, so ties keep step-2 order.
    """
    scores = defaultdict(float)
    for hits, weight in zip(ranked_lists, weights):
        for rank, hit in enumerate(hits, start=1):
            scores[hit["dup_of"]] += weight / (rank + c)

    first_seen = {}
    for hits in ranked_lists:
        for hit in hits:
            if hit["dup_of"] not in first_seen:
                first_seen[hit["dup_of"]] = hit

    return sorted(first_seen.values(), key=lambda hit: scores[hit["dup_of"]], reverse=True)


def chunks_to_pages(hits):
    """Turn a chunk ranking into a page ranking: keep each page at its first appearance."""
    pages = []
    for hit in hits:
        if hit["page"] not in pages:
            pages.append(hit["page"])
    return pages