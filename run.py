#!/usr/bin/env python3
import subprocess, re, argparse
from pathlib import Path

ALGO_MAP = {
    "BFS":           "src/run_BFS.vi",
    "SSSP":          "src/run_SSSP.vi",
    "TriangleCount": "src/run_TriangleCount.vi",
}
LIB_PATH = "src/lib"

parser = argparse.ArgumentParser()
parser.add_argument("algo", choices=list(ALGO_MAP.keys()))
parser.add_argument("matrix", nargs="?", default=None)
parser.add_argument("-r", "--runs", type=int, default=1)
parser.add_argument("-w", "--workers", nargs=2, type=int, default=[4, 5])
parser.add_argument("-H", "--heap", type=int, default=None)
args = parser.parse_args()

PROGRAM_FILE = ALGO_MAP[args.algo]
LIB_PATH = "src/lib"

original_src = Path(PROGRAM_FILE).read_text()
original_matrix = None
m = re.search(r'const matrix_file:String\s*=\s*"([^"]+)"', original_src)
if m:
    original_matrix = m.group(1)

if args.matrix:
    new_src = re.sub(
        r'const matrix_file:String\s*=\s*"[^"]+"',
        f'const matrix_file:String = "{args.matrix}"',
        original_src
    )
    Path(PROGRAM_FILE).write_text(new_src)

matrix_suffix = Path(args.matrix).stem if args.matrix else ""
heap_bytes = args.heap * 1024**3 if args.heap else None
heap_suffix = f"_H{args.heap}G" if args.heap else ""
LOG_DIR = Path(f"logs_{args.algo}{('_' + matrix_suffix) if matrix_suffix else ''}")
LOG_DIR.mkdir(exist_ok=True)

matrix_file = args.matrix if args.matrix else original_matrix
if not matrix_file:
    raise RuntimeError(f"Could not find matrix_file in {PROGRAM_FILE}")

try:
    for workers in range(args.workers[0], args.workers[1]):
        out_file = LOG_DIR / f"{workers}{heap_suffix}.log"
        for run in range(1, args.runs + 1):
            with open(out_file, "a") as f:
                f.write(f"====== run={run}/{args.runs} | workers={workers} | heap={args.heap}G | {matrix_file} ======\n")
                print(f"STARTED: ITER {run}; WORKERS {workers}")
                result = subprocess.run(
                    ["vine", "run", f"-w{workers}"] + ([f"-H{heap_bytes}"] if heap_bytes else []) + [PROGRAM_FILE, "--lib", LIB_PATH],
                    stdout=f, stderr=subprocess.STDOUT
                )
            print(f"workers={workers} run={run} -> {out_file} [exit {result.returncode}]")
finally:
    if args.matrix:
        Path(PROGRAM_FILE).write_text(original_src)