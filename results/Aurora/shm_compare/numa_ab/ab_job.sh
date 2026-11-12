#!/bin/bash -l
# One-off: same allocation, alternating runs, MPI window version versus /dev/shm mapping version.
#PBS -l filesystems=home:flare
#PBS -k doe
#PBS -j oe
set -u
ROOT=/lus/flare/projects/MPICH_MCS/kqi/mpich/Hierarchical-Allgather
DIR=$ROOT/results/Aurora/shm_compare/numa_ab
cd -- "$DIR" || exit 1
NNODES=$(wc -l < "$PBS_NODEFILE")
PPN=102
BIND="list:$(seq -s: 1 51):$(seq -s: 53 103)"
ARGS="nodes=$NNODES ppn=$PPN counts=64,8192,32768 radices=64 reps=20 warmup=3 diag=1"
for cycle in 1 2 3; do
  for variant in window mapping; do
    if [[ $variant == window ]]; then exe=$DIR/bench_window; else exe=$ROOT/bench_shm; fi
    echo "=== cycle $cycle $variant"
    mpiexec -n $(( NNODES * PPN )) -ppn "$PPN" --cpu-bind "$BIND" --env OMP_NUM_THREADS=1 "$exe" \
      $ARGS out="$DIR/${variant}_n${NNODES}_c${cycle}.csv" < /dev/null | grep -E 'allgather_shm|mpich_shar_tmp.*dirty=[0-9]{4,}|TIME_GUARD|SKIP'
  done
done
