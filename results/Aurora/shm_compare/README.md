# Aurora 上的共享内存 Allgather 对比数据

这些数据比较 `MPI_Allgather`、`Allgather_radix_batch`、`Allgather_shm` 和 `Allgather_shm_view` 四种实现，用的是 `benchmark_scripts/aurora_scripts/` 下的脚本和 `bench_shm`。结论见 PR 说明。

## 环境

| 项目 | 内容 |
|---|---|
| 时间 | 2026-11-04 到 11-05 |
| 机器 | Aurora，每节点 102 个进程，绑定核心 1 到 51、53 到 103 |
| MPI | 模块 `mpich/prd/5.0.0.aurora_test.87e2045`，`mpichversion` 显示 5.1.0a1，设备 ch4:ofi，没有另外设置 `MPIR_CVAR_*` |
| 其他模块 | gcc/14.3.0，oneapi/release/2026.1.0，libfabric/2.3.1，cray-pals/1.8.0 |

每个作业的完整环境变量、模块列表和节点列表在对应的 `*.meta` 文件里。

## 文件

| 文件 | 内容 |
|---|---|
| `n<节点数>_ppn102_<作业号>[_set<i>].csv` | 每次重复一行 |
| `*.log` | 运行进度；`job_*.log` 是作业脚本的输出 |
| `*.meta` | 作业环境、模块、节点列表 |
| `*.hosts` | 本次运行用到的节点 |
| `bench_args`、`node_sets` | 传给 `bench_shm` 的额外参数，以及同时运行的各组节点数 |
| `*_sanity_*.csv` | 小规模正确性检查，不参与汇总 |

CSV 各列的含义：

| 列 | 含义 |
|---|---|
| `algorithm`、`k` | 算法名（`mpi_allgather`、`radix_batch`、`node_shm`、`node_view`）和基数，后者只对 `radix_batch` 有意义 |
| `b` | 每组的进程数 |
| `send_count` | 每个进程发送的 `MPI_INT` 个数，字节数为它的 4 倍 |
| `rep` | 重复序号，热身不记录 |
| `time_barrier` | rank 0 的耗时，包含调用后的 barrier |
| `time_max` | 最慢进程的耗时，不含 barrier；汇总表用这一列 |
| `s1_max`、`s2_max`、`s3_max` | 三个阶段各自的最慢进程耗时，不能相加 |
| `s1_avg`、`s2_avg`、`s3_avg` | 三个阶段的平均耗时 |
| `is_correct` | 所有进程的结果都正确时为 1 |
| `read_max` | 只在 `view_*` 批次中出现：调用和一次 barrier 之后，最慢进程把整份结果求和一遍的耗时 |

重复次数：1024 个元素及以下 50 次，8192 个元素及以下 20 次，更大的 10 次。每种配置前有 3 次热身。

## 各批数据

| 文件夹 | 内容 | 作业 |
|---|---|---|
| `smoke_213419` | 最早的冒烟测试 | 9040104、9040106、9040107 |
| `compare_20261104` | MPI、Bruck、`Allgather_shm`，1 到 16 节点，4 B 到 128 KB，只算调用 | 9040142 到 9040146 |
| `numa_ab` | `Allgather_shm` 用 MPI 共享窗口和 `/dev/shm` 映射的对比，4 节点 | |
| `parallel_test` | 验证同一作业里同时跑多组 | 9040578 |
| `compare_big_20261104` | MPI、Bruck、`Allgather_shm`，16、32、64 节点同时跑 | 9040601 |
| `view_20261105` | 加入 `Allgather_shm_view` 和读取，1 到 16 节点；`job_test.log` 是 `test_shm_view` 的结果 | 9041335 到 9041338 |
| `view_nodes_20261105` | 加入 `Allgather_shm_view` 和读取，16、32、64 节点同时跑 | 9042156 |
| `view_largemsg_20261105` | 256 KB 到 1 MB，1 到 16 节点，Bruck 只跑基数 102 | 9042157、9042243 到 9042245 |

`numa_ab` 里的 `Allgather_shm_window.c` 是当时用 `MPI_Win_allocate_shared` 的 `Allgather_shm`，用它代替 `Allgather_shm.c` 编译出的 `bench_shm` 就是 `ab_job.sh` 里的 `bench_window`。可执行文件没有放进仓库，`ab_job.sh` 里的路径也是当时的路径。

## 汇总

`combined/` 里是按中位数汇总的结果：

- `all_runs_medians.csv`：五批主要测试的全部中位数，包含每个基数。
- `total_time_best.csv`：四种算法的总耗时（调用加读取）、调用耗时和比值。
- `total_time_tables.md`：其中 `MPI_Allgather`、`Allgather_radix_batch` 和 `Allgather_shm_view` 三种的总耗时表（英文）。
- `make_combined.py`：重新生成以上文件，在 `combined/` 目录里运行 `python3 make_combined.py`。

总耗时表的来源：1 到 16 节点用 `view_20261105`，32、64 节点用 `view_nodes_20261105`，256 KB 及以上用 `view_largemsg_20261105`。

## 注意

- **64 节点的 Bruck 数据异常。** `view_nodes_20261105` 里，64 节点的 `radix_batch` 在 32 B 到 512 B、32 KB 到 128 KB 比 `compare_big_20261104` 慢 20% 以上，128 KB 时最优调用耗时从 572 ms 变成 1429 ms。只有少数进程的第 3 阶段变慢，平均值几乎没变，原因未查明。这次的 64 个节点分散在 40 个机柜，上次在 4 个。
- **`MPI_Allgather` 的跳变。** 每种节点数下，都是整份结果（节点数 × 102 × 消息大小）达到 53.5 MB 时，调用耗时突然变慢 2.4 到 7.6 倍，`Allgather_shm` 没有这个现象。
- **同时运行的影响。** `view_nodes_20261105` 的 16 节点和 `view_20261105` 的 16 节点相比，8 KB 及以上相差不超过 3%。
