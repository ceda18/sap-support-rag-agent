"""Thin access to the objects the app itself uses for retrieval.

Nothing here ranks anything on its own: BM25 scores come from the app's BM25 index and
vector distances from the app's PGVector store. The only addition is that scores are
returned too (the app's retrievers return documents without scores).
"""
import time

import numpy as np
from langchain_community.retrievers import BM25Retriever

from rag.chain import get_retriever


def get_components():
    """Return (ensemble, bm25_retriever, vector_store) exactly as built by the app."""
    ensemble = get_retriever()
    bm25, vector_retriever = ensemble.retrievers      # order set in app/rag/retriever.py
    assert isinstance(bm25, BM25Retriever), "expected BM25 as the first retriever"
    return ensemble, bm25, vector_retriever.vectorstore


def build_dup_map(bm25):
    """chunk text -> smallest chunk_index with that text (the app dedups by text)."""
    first_index = {}
    for doc in bm25.docs:                              # docs are in chunk_index order
        first_index.setdefault(doc.page_content, doc.metadata["chunk_index"])
    return first_index


def to_hit(doc, score, dup_map):
    if doc.page_content not in dup_map:
        raise RuntimeError(f"chunk {doc.metadata.get('chunk_index')} from the database is not "
                           "in chunks.json - the database and the JSON file are out of sync")
    return {"chunk_index": doc.metadata["chunk_index"], "page": doc.metadata["page"],
            "score": round(float(score), 6), "dup_of": dup_map[doc.page_content]}


def bm25_top(bm25, query, k, dup_map):
    """Top-k BM25 hits with scores (higher = better), plus elapsed milliseconds.

    Same steps as BM25Retriever._get_relevant_documents and rank_bm25's get_top_n;
    the only difference is that the scores are kept.
    """
    start = time.perf_counter()
    tokens = bm25.preprocess_func(query)
    scores = bm25.vectorizer.get_scores(tokens)
    top = np.argsort(scores)[::-1][:k]
    elapsed_ms = (time.perf_counter() - start) * 1000
    return [to_hit(bm25.docs[i], scores[i], dup_map) for i in top], elapsed_ms


def vector_top(store, query, k, dup_map):
    """Top-k vector hits with cosine distance (lower = better), plus embed and search ms.

    Same two calls PGVector.similarity_search_with_score makes, timed separately.
    """
    start = time.perf_counter()
    embedding = store.embeddings.embed_query(query)
    embedded = time.perf_counter()
    results = store.similarity_search_with_score_by_vector(embedding, k=k)
    done = time.perf_counter()
    hits = [to_hit(doc, distance, dup_map) for doc, distance in results]
    return hits, (embedded - start) * 1000, (done - embedded) * 1000