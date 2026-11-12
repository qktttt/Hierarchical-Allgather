files: 5, metric: time_max, wrong results: 0 of 600 repetitions

## 1 nodes
| elements | bytes/rank | MPI_Allgather | radix_batch best (k) | node_shm | shm/MPI | shm/radix |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 34.90 ms | 31.05 ms (k=102) | 12.11 ms | 0.35 | 0.39 |
| 131072 | 524288 | 266.23 ms | 62.18 ms (k=102) | 25.15 ms | 0.09 | 0.40 |
| 262144 | 1048576 | 538.71 ms | 117.90 ms (k=102) | 44.44 ms | 0.08 | 0.38 |

Slowest rank in each stage (radix_batch at its best k, then node_shm):
| elements | radix s1 | radix s2 | radix s3 | shm s1 | shm s2 | shm s3 |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 11.48 ms | 4.87 ms | 28.95 ms | 248.4 us | 15.2 us | 11.90 ms |
| 131072 | 24.79 ms | 10.02 ms | 59.89 ms | 476.1 us | 20.2 us | 24.62 ms |
| 262144 | 51.28 ms | 11.30 ms | 115.20 ms | 2.52 ms | 6.3 us | 42.34 ms |

node_view: the call alone, then the call plus one read of the whole result:
| elements | bytes/rank | radix best | node_shm | node_view | view/radix | view/shm | read radix | read shm | read view | radix+read | shm+read | view+read | view/radix | view/shm |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 31.05 ms | 12.11 ms | 1.35 ms | 0.04 | 0.11 | 5.84 ms | 6.71 ms | 6.95 ms | 36.91 ms | 18.81 ms | 8.29 ms | 0.22 | 0.44 |
| 131072 | 524288 | 62.18 ms | 25.15 ms | 2.63 ms | 0.04 | 0.10 | 11.15 ms | 12.03 ms | 14.99 ms | 73.58 ms | 37.46 ms | 17.67 ms | 0.24 | 0.47 |
| 262144 | 1048576 | 117.90 ms | 44.44 ms | 4.01 ms | 0.03 | 0.09 | 21.85 ms | 22.95 ms | 31.05 ms | 141.42 ms | 67.53 ms | 35.08 ms | 0.25 | 0.52 |

## 2 nodes
| elements | bytes/rank | MPI_Allgather | radix_batch best (k) | node_shm | shm/MPI | shm/radix |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 158.55 ms | 48.49 ms (k=102) | 24.98 ms | 0.16 | 0.52 |
| 131072 | 524288 | 326.37 ms | 93.49 ms (k=102) | 46.29 ms | 0.14 | 0.50 |
| 262144 | 1048576 | 638.12 ms | 175.52 ms (k=102) | 93.27 ms | 0.15 | 0.53 |

Slowest rank in each stage (radix_batch at its best k, then node_shm):
| elements | radix s1 | radix s2 | radix s3 | shm s1 | shm s2 | shm s3 |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 13.09 ms | 19.42 ms | 47.98 ms | 411.6 us | 1.82 ms | 24.74 ms |
| 131072 | 27.12 ms | 42.17 ms | 91.39 ms | 1.69 ms | 4.81 ms | 44.56 ms |
| 262144 | 55.16 ms | 74.07 ms | 166.62 ms | 2.03 ms | 7.91 ms | 92.01 ms |

node_view: the call alone, then the call plus one read of the whole result:
| elements | bytes/rank | radix best | node_shm | node_view | view/radix | view/shm | read radix | read shm | read view | radix+read | shm+read | view+read | view/radix | view/shm |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 48.49 ms | 24.98 ms | 3.41 ms | 0.07 | 0.14 | 11.28 ms | 11.98 ms | 14.22 ms | 59.81 ms | 36.85 ms | 17.79 ms | 0.30 | 0.48 |
| 131072 | 524288 | 93.49 ms | 46.29 ms | 6.51 ms | 0.07 | 0.14 | 24.45 ms | 22.76 ms | 29.14 ms | 119.23 ms | 69.01 ms | 35.65 ms | 0.30 | 0.52 |
| 262144 | 1048576 | 175.52 ms | 93.27 ms | 9.46 ms | 0.05 | 0.10 | 48.03 ms | 44.93 ms | 60.02 ms | 225.29 ms | 137.89 ms | 69.63 ms | 0.31 | 0.50 |

## 4 nodes
| elements | bytes/rank | MPI_Allgather | radix_batch best (k) | node_shm | shm/MPI | shm/radix |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 233.40 ms | 71.65 ms (k=102) | 46.70 ms | 0.20 | 0.65 |
| 131072 | 524288 | 470.92 ms | 155.43 ms (k=102) | 94.72 ms | 0.20 | 0.61 |
| 262144 | 1048576 | 950.75 ms | 274.74 ms (k=102) | 185.90 ms | 0.20 | 0.68 |

Slowest rank in each stage (radix_batch at its best k, then node_shm):
| elements | radix s1 | radix s2 | radix s3 | shm s1 | shm s2 | shm s3 |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 14.06 ms | 22.56 ms | 70.83 ms | 975.2 us | 4.39 ms | 45.75 ms |
| 131072 | 31.31 ms | 54.31 ms | 148.55 ms | 1.55 ms | 8.32 ms | 94.18 ms |
| 262144 | 64.05 ms | 127.38 ms | 262.10 ms | 1.70 ms | 14.86 ms | 185.03 ms |

node_view: the call alone, then the call plus one read of the whole result:
| elements | bytes/rank | radix best | node_shm | node_view | view/radix | view/shm | read radix | read shm | read view | radix+read | shm+read | view+read | view/radix | view/shm |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 71.65 ms | 46.70 ms | 5.86 ms | 0.08 | 0.13 | 22.91 ms | 22.51 ms | 30.54 ms | 94.88 ms | 68.96 ms | 36.46 ms | 0.38 | 0.53 |
| 131072 | 524288 | 155.43 ms | 94.72 ms | 9.32 ms | 0.06 | 0.10 | 45.31 ms | 44.20 ms | 60.95 ms | 200.57 ms | 138.71 ms | 70.32 ms | 0.35 | 0.51 |
| 262144 | 1048576 | 274.74 ms | 185.90 ms | 16.14 ms | 0.06 | 0.09 | 88.66 ms | 84.15 ms | 128.80 ms | 364.50 ms | 270.59 ms | 144.94 ms | 0.40 | 0.54 |

## 8 nodes
| elements | bytes/rank | MPI_Allgather | radix_batch best (k) | node_shm | shm/MPI | shm/radix |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 401.06 ms | 128.06 ms (k=102) | 94.57 ms | 0.24 | 0.74 |
| 131072 | 524288 | 838.18 ms | 265.18 ms (k=102) | 189.42 ms | 0.23 | 0.71 |
| 262144 | 1048576 | 1.610 s | 450.98 ms (k=102) | 366.19 ms | 0.23 | 0.81 |

Slowest rank in each stage (radix_batch at its best k, then node_shm):
| elements | radix s1 | radix s2 | radix s3 | shm s1 | shm s2 | shm s3 |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 17.05 ms | 32.94 ms | 124.91 ms | 776.3 us | 8.35 ms | 94.34 ms |
| 131072 | 36.35 ms | 71.70 ms | 255.81 ms | 973.9 us | 16.34 ms | 188.80 ms |
| 262144 | 48.55 ms | 90.46 ms | 441.52 ms | 1.14 ms | 31.35 ms | 365.28 ms |

node_view: the call alone, then the call plus one read of the whole result:
| elements | bytes/rank | radix best | node_shm | node_view | view/radix | view/shm | read radix | read shm | read view | radix+read | shm+read | view+read | view/radix | view/shm |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 128.06 ms | 94.57 ms | 9.28 ms | 0.07 | 0.10 | 47.10 ms | 44.63 ms | 61.51 ms | 175.48 ms | 139.30 ms | 70.61 ms | 0.40 | 0.51 |
| 131072 | 524288 | 265.18 ms | 189.42 ms | 17.56 ms | 0.07 | 0.09 | 87.53 ms | 84.44 ms | 130.13 ms | 355.92 ms | 273.87 ms | 147.57 ms | 0.41 | 0.54 |
| 262144 | 1048576 | 450.98 ms | 366.19 ms | 35.43 ms | 0.08 | 0.10 | 175.20 ms | 170.17 ms | 261.74 ms | 627.42 ms | 536.09 ms | 297.08 ms | 0.47 | 0.55 |

## 16 nodes
| elements | bytes/rank | MPI_Allgather | radix_batch best (k) | node_shm | shm/MPI | shm/radix |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 778.70 ms | 238.50 ms (k=102) | 204.79 ms | 0.26 | 0.86 |
| 131072 | 524288 | 1.504 s | 504.36 ms (k=102) | 405.53 ms | 0.27 | 0.80 |
| 262144 | 1048576 | 2.988 s | 915.65 ms (k=102) | 835.73 ms | 0.28 | 0.91 |

Slowest rank in each stage (radix_batch at its best k, then node_shm):
| elements | radix s1 | radix s2 | radix s3 | shm s1 | shm s2 | shm s3 |
|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 19.75 ms | 58.14 ms | 223.00 ms | 715.8 us | 34.38 ms | 204.55 ms |
| 131072 | 44.39 ms | 113.57 ms | 482.72 ms | 886.4 us | 74.56 ms | 405.08 ms |
| 262144 | 80.17 ms | 234.34 ms | 890.00 ms | 1.33 ms | 153.42 ms | 834.79 ms |

node_view: the call alone, then the call plus one read of the whole result:
| elements | bytes/rank | radix best | node_shm | node_view | view/radix | view/shm | read radix | read shm | read view | radix+read | shm+read | view+read | view/radix | view/shm |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 65536 | 262144 | 238.50 ms | 204.79 ms | 35.73 ms | 0.15 | 0.17 | 93.44 ms | 84.65 ms | 134.95 ms | 332.47 ms | 289.76 ms | 172.31 ms | 0.52 | 0.59 |
| 131072 | 524288 | 504.36 ms | 405.53 ms | 75.25 ms | 0.15 | 0.19 | 184.97 ms | 171.30 ms | 260.16 ms | 694.94 ms | 576.90 ms | 334.36 ms | 0.48 | 0.58 |
| 262144 | 1048576 | 915.65 ms | 835.73 ms | 151.45 ms | 0.17 | 0.18 | 385.70 ms | 402.38 ms | 482.13 ms | 1.296 s | 1.234 s | 634.71 ms | 0.49 | 0.51 |
