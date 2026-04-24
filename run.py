#!/usr/bin/env python3
import subprocess, re
from pathlib import Path

PROGRAM_FILE = "src/run_BFS.vi"
LIB_PATH     = "src/lib"
LOG_DIR      = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

matrix_file = None
for line in Path(PROGRAM_FILE).read_text().splitlines():
    m = re.search(r'const matrix_file:String\s*=\s*"([^"]+)"', line)
    if m:
        matrix_file = m.group(1)
        break
if not matrix_file:
    raise RuntimeError(f"Could not find matrix_file in {PROGRAM_FILE}")

for workers in range(9):    
    out_file = LOG_DIR / f"{workers}_bfs.log"
    for run in range(1, 4):
        with open(out_file, "a") as f:
            f.write(f"====== run={run}/3 | workers={workers} | {matrix_file} ======\n")
            print(f"STARTED: ITER {run}; WORKERS {workers}")
            result = subprocess.run(
                ["vine", "run", f"-w{workers}", PROGRAM_FILE, "--lib", LIB_PATH],
                stdout=f, stderr=subprocess.STDOUT
            )
        print(f"workers={workers} run={run}/3 -> {out_file} [exit {result.returncode}]")