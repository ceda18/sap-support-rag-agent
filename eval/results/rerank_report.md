# R4 - cross-encoder reranker

Model `cross-encoder/ms-marco-MiniLM-L-6-v2` on CPU, reordering the top 30 chunks of the hybrid ranking (0.4/0.6). 40 answerable questions.

Gold page somewhere in the pool (ceiling for the reranker): 0.950

## Ranking quality

| metric | hybrid | hybrid + reranker | difference | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|
| recall@5 | 0.812 | 0.875 | +0.062 | [-0.025, +0.175] | no |
| recall@10 | 0.875 | 0.950 | +0.075 | [+0.000, +0.175] | no |
| mrr@10 | 0.571 | 0.734 | +0.164 | [+0.036, +0.302] | yes |
| ndcg@10 | 0.646 | 0.788 | +0.142 | [+0.039, +0.256] | yes |

## Gold page in context when only the top N chunks are sent

| top N chunks | hybrid | hybrid + reranker | est. tokens (reranked) |
|---|---|---|---|
| 3 | 0.675 | 0.850 | 636 |
| 5 | 0.775 | 0.875 | 1069 |
| 8 | 0.875 | 0.950 | 1709 |
| 10 | 0.875 | 0.950 | 2122 |

## Added latency

Reranking 30 chunks per question on CPU: p50 613 ms, p95 1206 ms (over 50 questions).
