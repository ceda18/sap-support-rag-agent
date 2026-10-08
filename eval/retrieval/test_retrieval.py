"""Hand-computed checks for fusion.py and metrics.py. No database, no LLM.

  docker compose exec -w /eval api python -m retrieval.test_retrieval
"""
import math

from retrieval.fusion import chunks_to_pages, weighted_rrf
from retrieval.metrics import (hit_at_k, mean, ndcg_at_k, paired_bootstrap,
                               recall_at_k, reciprocal_rank_at_k)


def close(a, b):
    return math.isclose(a, b, abs_tol=1e-4)


def hit(chunk_index, page=1, dup_of=None):
    return {"chunk_index": chunk_index, "page": page, "score": 0.0,
            "dup_of": chunk_index if dup_of is None else dup_of}


def order(hits):
    return [h["chunk_index"] for h in hits]


def test_metrics_one_gold_page():
    ranked, gold = [7, 3, 9, 4], [3]          # gold page is at rank 2
    assert recall_at_k(ranked, gold, 1) == 0.0
    assert recall_at_k(ranked, gold, 2) == 1.0
    assert hit_at_k(ranked, gold, 1) == 0.0 and hit_at_k(ranked, gold, 2) == 1.0
    assert reciprocal_rank_at_k(ranked, gold) == 0.5              # 1 / 2
    assert close(ndcg_at_k(ranked, gold), 0.6309)                 # (1 / log2(3)) / 1


def test_metrics_gold_outside_top_10():
    ranked, gold = list(range(100, 111)), [110]   # gold page is at rank 11
    assert reciprocal_rank_at_k(ranked, gold, k=10) == 0.0
    assert ndcg_at_k(ranked, gold, k=10) == 0.0
    assert recall_at_k(ranked, gold, 10) == 0.0
    assert recall_at_k(ranked, gold, 20) == 1.0


def test_metrics_two_gold_pages():
    ranked, gold = [3, 8, 4], [3, 4]          # gold pages at ranks 1 and 3
    assert recall_at_k(ranked, gold, 1) == 0.5
    assert recall_at_k(ranked, gold, 3) == 1.0
    assert reciprocal_rank_at_k(ranked, gold) == 1.0
    # DCG = 1/log2(2) + 1/log2(4) = 1.5 ; ideal = 1/log2(2) + 1/log2(3) = 1.6309
    assert close(ndcg_at_k(ranked, gold), 1.5 / 1.6309)
    assert close(ndcg_at_k([3, 4, 8], gold), 1.0)                 # ideal order


def test_metrics_nothing_retrieved():
    assert recall_at_k([], [3], 5) == 0.0
    assert reciprocal_rank_at_k([], [3]) == 0.0
    assert ndcg_at_k([], [3]) == 0.0


def test_fusion_hand_computed():
    A, B, C, D = hit(1), hit(2), hit(3), hit(4)
    bm25, vector = [A, B, C], [C, A, D]
    # weights 0.4 / 0.6:
    #   A = 0.4/61 + 0.6/62 = 0.016235    C = 0.4/63 + 0.6/61 = 0.016185
    #   D = 0.6/63          = 0.009524    B = 0.4/62          = 0.006452
    assert order(weighted_rrf([bm25, vector], [0.4, 0.6])) == [1, 3, 4, 2]
    # weights 0.5 / 0.5: B = 0.5/62 = 0.008065 now beats D = 0.5/63 = 0.007937
    assert order(weighted_rrf([bm25, vector], [0.5, 0.5])) == [1, 3, 2, 4]


def test_fusion_weights_reorder_but_never_change_the_set():
    bm25, vector = [hit(1), hit(2), hit(3)], [hit(3), hit(4), hit(5)]
    fused_a = weighted_rrf([bm25, vector], [0.4, 0.6])
    fused_b = weighted_rrf([bm25, vector], [0.9, 0.1])
    assert set(order(fused_a)) == set(order(fused_b)) == {1, 2, 3, 4, 5}
    assert order(fused_a) != order(fused_b)


def test_fusion_tie_keeps_first_list_first():
    # both score 0.5 / 61 -> tie -> the hit from the first list (BM25) stays first
    assert order(weighted_rrf([[hit(1)], [hit(2)]], [0.5, 0.5])) == [1, 2]


def test_fusion_zero_weight_list_goes_to_the_end():
    fused = weighted_rrf([[hit(1), hit(2)], [hit(3)]], [0.0, 1.0])
    assert order(fused) == [3, 1, 2]


def test_fusion_identical_text_is_merged():
    # chunk 9 has the same text as chunk 2 (dup_of=2): one entry, scores are added
    bm25, vector = [hit(1), hit(2)], [hit(9, dup_of=2)]
    # key 2 = 0.5/62 + 0.5/61 = 0.016262  beats  key 1 = 0.5/61 = 0.008197
    assert order(weighted_rrf([bm25, vector], [0.5, 0.5])) == [2, 1]


def test_chunks_to_pages():
    hits = [hit(1, page=5), hit(2, page=5), hit(3, page=7), hit(4, page=5), hit(5, page=9)]
    assert chunks_to_pages(hits) == [5, 7, 9]


def test_bootstrap():
    a = [0.0, 0.5, 1.0, 0.25, 1.0]
    assert paired_bootstrap(a, a) == (0.0, 0.0, 0.0)              # same config -> no difference
    diff, low, high = paired_bootstrap(a, [x + 0.1 for x in a])   # every question +0.1
    assert close(diff, 0.1) and close(low, 0.1) and close(high, 0.1)
    # b wins on 10 of 20 questions: difference 0.5, interval must sit clearly above 0
    a, b = [0.0] * 20, [1.0] * 10 + [0.0] * 10
    diff, low, high = paired_bootstrap(a, b)
    assert diff == 0.5 and 0.0 < low < 0.5 < high < 1.0
    assert paired_bootstrap(a, b) == (diff, low, high)            # fixed seed -> repeatable
    assert mean([1.0, 0.0, 0.5]) == 0.5


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]
    for name, fn in tests:
        fn()
        print("PASS", name)
    print(f"\nall {len(tests)} tests passed")