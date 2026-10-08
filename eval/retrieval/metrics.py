"""Retrieval metrics over a ranked list of pages, plus the paired bootstrap.

Every metric function scores ONE question:
    ranked_pages: page numbers, best first, no repeats
    gold_pages:   pages that contain the answer
The value reported for a configuration is the mean over all questions.
"""
import math

import numpy as np


def recall_at_k(ranked_pages, gold_pages, k):
    """Share of the gold pages that appear in the top k."""
    top_k = set(ranked_pages[:k])
    return sum(1 for page in gold_pages if page in top_k) / len(gold_pages)


def hit_at_k(ranked_pages, gold_pages, k):
    """1.0 if at least one gold page is in the top k, else 0.0."""
    top_k = set(ranked_pages[:k])
    return 1.0 if any(page in top_k for page in gold_pages) else 0.0


def reciprocal_rank_at_k(ranked_pages, gold_pages, k=10):
    """1 / rank of the first gold page; 0.0 if none is in the top k. Its mean is MRR@k."""
    for rank, page in enumerate(ranked_pages[:k], start=1):
        if page in gold_pages:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_pages, gold_pages, k=10):
    """DCG / ideal DCG with binary relevance (a page is gold or it is not).

    A gold page at rank r adds 1 / log2(r + 1). The ideal ranking puts all gold pages first.
    """
    dcg = sum(1.0 / math.log2(rank + 1)
              for rank, page in enumerate(ranked_pages[:k], start=1) if page in gold_pages)
    ideal_dcg = sum(1.0 / math.log2(rank + 1)
                    for rank in range(1, min(len(gold_pages), k) + 1))
    return dcg / ideal_dcg


def mean(values):
    return sum(values) / len(values)


def paired_bootstrap(values_a, values_b, n_resamples=1000, seed=0):
    """95% confidence interval for mean(values_b) - mean(values_a).

    values_a[i] and values_b[i] are the same metric on the same question i under two
    configurations. Each resample draws len(values) questions with replacement and takes
    the mean difference; the interval is the 2.5th..97.5th percentile of those means.
    Returns (observed_difference, ci_low, ci_high).
    """
    diffs = np.array(values_b, dtype=float) - np.array(values_a, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(diffs)
    resampled_means = [diffs[rng.integers(0, n, size=n)].mean() for _ in range(n_resamples)]
    ci_low, ci_high = np.percentile(resampled_means, [2.5, 97.5])
    return float(diffs.mean()), float(ci_low), float(ci_high)