#!/usr/bin/env python3
"""Rebuild the combined tables from the raw CSV files of each run. Run from this folder (combined/)."""
import collections
import csv
import glob
import os
import statistics as st

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RUNS = ["compare_20261104", "compare_big_20261104", "view_20261105", "view_nodes_20261105", "view_largemsg_20261105"]
# Which run supplies each node count in the total-time tables.
VIEW_RUNS = {1: "view_20261105", 2: "view_20261105", 4: "view_20261105", 8: "view_20261105", 16: "view_20261105",
             32: "view_nodes_20261105", 64: "view_nodes_20261105"}


def load():
    rows = collections.defaultdict(list)
    for run in RUNS:
        for path in glob.glob(os.path.join(DATA, run, "n*_ppn102_*.csv")):
            if "_sanity_" in path:
                continue
            with open(path, newline="") as stream:
                for r in csv.DictReader(stream):
                    key = (run, int(r["nodes"]), int(r["send_count"]) * 4, r["algorithm"], int(r["k"]))
                    rows[key].append(r)
    return rows


def med(group, column):
    return st.median(float(r[column]) for r in group)


def total(group):
    return st.median(float(r["time_max"]) + float(r.get("read_max") or 0) for r in group)


def has_read(group):
    return bool(group[0].get("read_max"))


def fmt(seconds):
    if seconds < 1e-3:
        return "%.1f µs" % (seconds * 1e6)
    return "%.2f ms" % (seconds * 1e3)


def size_name(b):
    if b < 1024:
        return "%d B" % b
    if b < 1048576:
        return "%d KB" % (b // 1024)
    return "%d MB" % (b // 1048576)


rows = load()
with open("all_runs_medians.csv", "w", newline="") as stream:
    w = csv.writer(stream)
    w.writerow(["run", "nodes", "ppn", "bytes_per_rank", "result_bytes_per_rank", "algorithm", "k", "reps", "wrong",
                "call_median_s", "read_median_s", "call_plus_read_median_s",
                "s1_max_median_s", "s2_max_median_s", "s3_max_median_s", "s3_avg_median_s"])
    for key in sorted(rows):
        run, n, b, alg, k = key
        g = rows[key]
        w.writerow([run, n, 102, b, n * 102 * b, alg, k, len(g), sum(r["is_correct"] != "1" for r in g),
                    med(g, "time_max"), med(g, "read_max") if has_read(g) else "", total(g) if has_read(g) else "",
                    med(g, "s1_max"), med(g, "s2_max"), med(g, "s3_max"), med(g, "s3_avg")])

best = []
for n, run in sorted(VIEW_RUNS.items()):
    for source in (run, "view_largemsg_20261105"):
        for b in sorted({k[2] for k in rows if k[0] == source and k[1] == n}):
            get = lambda a: rows[(source, n, b, a, 0)]
            radix = {k[4]: v for k, v in rows.items() if k[:4] == (source, n, b, "radix_batch")}
            kb = min(radix, key=lambda k: total(radix[k]))
            kc = min(radix, key=lambda k: med(radix[k], "time_max"))
            old = {k[4]: v for k, v in rows.items() if k[:4] == ("compare_big_20261104", n, b, "radix_batch")} if n == 64 else {}
            slower = None
            if old:
                slower = med(radix[kc], "time_max") / min(med(v, "time_max") for v in old.values())
            best.append(dict(source=source, nodes=n, bytes=b, result_bytes=n * 102 * b,
                             mpi_call=med(get("mpi_allgather"), "time_max"), bruck_call=med(radix[kc], "time_max"),
                             shm_call=med(get("node_shm"), "time_max"), view_call=med(get("node_view"), "time_max"),
                             mpi=total(get("mpi_allgather")), bruck=total(radix[kb]), bruck_k=kb,
                             shm=total(get("node_shm")), view=total(get("node_view")),
                             shm_read=med(get("node_shm"), "read_max"), view_read=med(get("node_view"), "read_max"),
                             bruck_vs_earlier_run=slower))

with open("total_time_best.csv", "w", newline="") as stream:
    fields = list(best[0]) + ["view_over_shm", "view_over_bruck", "view_over_mpi", "fastest"]
    w = csv.DictWriter(stream, fieldnames=fields)
    w.writeheader()
    for r in best:
        w.writerow(dict(r, view_over_shm=r["view"] / r["shm"], view_over_bruck=r["view"] / r["bruck"],
                        view_over_mpi=r["view"] / r["mpi"],
                        fastest=min(("mpi", "bruck", "shm", "view"), key=lambda a: r[a])))

with open("total_time_tables.md", "w") as out:
    out.write("# 总耗时表\n\n总耗时 = 一次调用 + 所有进程把整份结果读一遍，每次重复相加后取中位数。"
              "每个大小下 Bruck 取总耗时最短的基数；256 KB 及以上只跑了基数 102。加粗表示四种算法中最快。\n"
              "† 表示这个 Bruck 数据的调用耗时比 compare_big_20261104 慢 20% 以上，不要直接用。\n")
    for n in sorted(VIEW_RUNS):
        out.write("\n## %d 节点\n\n| 消息 | 整份结果 | MPI_Allgather | Bruck 最优 | 旧版 | 新版 | 新版/旧版 | 新版/Bruck | 新版/MPI |\n"
                  "|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n" % n)
        for r in (x for x in best if x["nodes"] == n):
            win = min(("mpi", "bruck", "shm", "view"), key=lambda a: r[a])
            cell = lambda a: ("**%s**" % fmt(r[a])) if a == win else fmt(r[a])
            mark = " †" if r["bruck_vs_earlier_run"] and r["bruck_vs_earlier_run"] >= 1.2 else ""
            out.write("| %s | %.2f MB | %s | %s (k=%d)%s | %s | %s | %.2f | %.2f | %.2f |\n" % (
                size_name(r["bytes"]), r["result_bytes"] / 1e6, cell("mpi"), cell("bruck"), r["bruck_k"], mark,
                cell("shm"), cell("view"), r["view"] / r["shm"], r["view"] / r["bruck"], r["view"] / r["mpi"]))
