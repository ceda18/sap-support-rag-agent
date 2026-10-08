# Retrieval report

Snapshot: commit `7e9f2cb`, 40 answerable questions, unit of relevance = page, fusion depth = 100 per retriever.

## R1 - ranker quality

| config | recall@5 | recall@10 | recall@20 | mrr@10 | ndcg@10 |
|---|---|---|---|---|---|
| BM25 only | 0.575 | 0.750 | 0.775 | 0.452 | 0.520 |
| Vector only | 0.850 | 0.875 | 0.925 | 0.601 | 0.669 |
| Hybrid 0.4/0.6 (app weights) | 0.812 | 0.875 | 0.925 | 0.571 | 0.646 |
| RRF 0.5/0.5 | 0.812 | 0.863 | 0.900 | 0.533 | 0.612 |

Duplicate-text check: in 2 of 40 questions a chunk whose text repeats inside one list reached the hybrid top 10 with a summed score.

## App as deployed (TOP_K=5 per retriever, no cut after fusion)

| gold page in context | mean chunks | mean pages | est. tokens |
|---|---|---|---|
| 0.950 | 8.5 | 7.4 | 1781 |

Tokens are estimated as chunk characters / 4.

## R2 - vector weight sweep

| vector weight | mrr@10 | recall@5 |
|---|---|---|
| 0.0 | 0.452 | 0.575 |
| 0.1 | 0.481 | 0.700 |
| 0.2 | 0.498 | 0.675 |
| 0.3 | 0.513 | 0.750 |
| 0.4 | 0.490 | 0.775 |
| 0.5 | 0.533 | 0.812 |
| 0.6 | 0.571 | 0.812 |
| 0.7 | 0.548 | 0.787 |
| 0.8 | 0.546 | 0.775 |
| 0.9 | 0.580 | 0.825 |
| 1.0 | 0.585 | 0.850 |

Highest MRR@10 at vector weight 1.0 (app uses 0.6). Chosen on the same questions it is measured on.

## R3 - gold page in context vs. context size

| TOP_K | gold page in context | mean chunks | est. tokens |
|---|---|---|---|
| 1 | 0.600 | 1.8 | 379 |
| 2 | 0.800 | 3.4 | 714 |
| 3 | 0.850 | 5.0 | 1059 |
| 4 | 0.900 | 6.7 | 1418 |
| 5 | 0.950 | 8.5 | 1781 |
| 6 | 0.950 | 10.1 | 2111 |
| 7 | 0.950 | 11.9 | 2475 |
| 8 | 0.950 | 13.6 | 2826 |
| 9 | 0.950 | 15.1 | 3144 |
| 10 | 0.950 | 16.8 | 3485 |
| 11 | 0.950 | 18.5 | 3847 |
| 12 | 0.950 | 20.2 | 4214 |
| 13 | 0.950 | 21.9 | 4568 |
| 14 | 0.950 | 23.6 | 4916 |
| 15 | 0.950 | 25.3 | 5254 |
| 16 | 0.950 | 27.0 | 5629 |
| 17 | 0.950 | 28.8 | 5995 |
| 18 | 0.950 | 30.5 | 6340 |
| 19 | 0.950 | 32.2 | 6697 |
| 20 | 0.950 | 34.0 | 7063 |

TOP_K is per retriever; the context is the fused union of both lists.

## R5 - by question type

| config | type | n | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|
| BM25 only | synthetic | 30 | 0.600 | 0.800 | 0.474 |
| BM25 only | manual | 10 | 0.500 | 0.600 | 0.387 |
| Vector only | synthetic | 30 | 0.900 | 0.933 | 0.667 |
| Vector only | manual | 10 | 0.700 | 0.700 | 0.403 |
| Hybrid 0.4/0.6 (app weights) | synthetic | 30 | 0.867 | 0.900 | 0.609 |
| Hybrid 0.4/0.6 (app weights) | manual | 10 | 0.650 | 0.800 | 0.456 |
| RRF 0.5/0.5 | synthetic | 30 | 0.833 | 0.900 | 0.576 |
| RRF 0.5/0.5 | manual | 10 | 0.750 | 0.750 | 0.403 |

## R7 - paired bootstrap (B minus A, 1000 resamples, 95% interval)

| A | B | metric | B - A | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|
| BM25 only | Vector only | mrr@10 | +0.149 | [-0.009, +0.318] | no |
| BM25 only | Vector only | recall@5 | +0.275 | [+0.075, +0.475] | yes |
| BM25 only | Vector only | ndcg@10 | +0.150 | [+0.003, +0.305] | yes |
| BM25 only | Hybrid 0.4/0.6 (app weights) | mrr@10 | +0.118 | [+0.021, +0.226] | yes |
| BM25 only | Hybrid 0.4/0.6 (app weights) | recall@5 | +0.237 | [+0.100, +0.388] | yes |
| BM25 only | Hybrid 0.4/0.6 (app weights) | ndcg@10 | +0.126 | [+0.043, +0.221] | yes |
| Vector only | Hybrid 0.4/0.6 (app weights) | mrr@10 | -0.031 | [-0.157, +0.086] | no |
| Vector only | Hybrid 0.4/0.6 (app weights) | recall@5 | -0.037 | [-0.163, +0.100] | no |
| Vector only | Hybrid 0.4/0.6 (app weights) | ndcg@10 | -0.024 | [-0.136, +0.081] | no |
| Hybrid 0.4/0.6 (app weights) | RRF 0.5/0.5 | mrr@10 | -0.038 | [-0.087, +0.009] | no |
| Hybrid 0.4/0.6 (app weights) | RRF 0.5/0.5 | recall@5 | +0.000 | [-0.075, +0.075] | no |
| Hybrid 0.4/0.6 (app weights) | RRF 0.5/0.5 | ndcg@10 | -0.034 | [-0.071, +0.003] | no |
| Hybrid 0.4/0.6 (app weights) | Best sweep weight (1.0) | mrr@10 | +0.014 | [-0.097, +0.133] | no |
| Hybrid 0.4/0.6 (app weights) | Best sweep weight (1.0) | recall@5 | +0.037 | [-0.100, +0.163] | no |
| Hybrid 0.4/0.6 (app weights) | Best sweep weight (1.0) | ndcg@10 | +0.011 | [-0.088, +0.117] | no |
