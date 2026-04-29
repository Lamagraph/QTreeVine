#!/usr/bin/env python3
import json
import re
from pathlib import Path
from datetime import datetime

ALGO_MAP = {
    "BFS": "bfs",
    "SSSP": "sssp",
    "TriangleCount": "tc"
}

TOTAL_RE = re.compile(r'^\s+Total\s+([\d_]+)', re.MULTILINE)
TIME_RE = re.compile(r'^\s+Time\s+([\d_]+)\s+ms$', re.MULTILINE)

def parse_folder_name(name):
    if not name.startswith("logs_"):
        return None, None
    rest = name[5:]
    for algo_key, algo_val in ALGO_MAP.items():
        if rest.startswith(algo_key + "_"):
            matrix = rest[len(algo_key)+1:]
            return algo_val, matrix
        elif rest == algo_key:
            return algo_val, ""
    return None, None

def parse_log_file(filepath):
    text = Path(filepath).read_text()
    totals = TOTAL_RE.findall(text)
    times_ms = TIME_RE.findall(text)
    runs = []
    for total, time_ms in zip(totals, times_ms):
        ms = int(time_ms.replace('_', ''))
        runs.append(f"total interaction: {total}; time: {ms / 1000:.3f} s")
    return runs

def main():
    base = Path("/home/gsv/Projects/QTreeVine")
    result = {}

    for folder in base.iterdir():
        if not folder.is_dir() or not folder.name.startswith("logs_"):
            continue
        algo, matrix = parse_folder_name(folder.name)
        if algo is None:
            continue
        result.setdefault(algo, {}).setdefault(matrix, {})
        for logfile in folder.glob("*.log"):
            workers = logfile.stem.split('_')[0]
            runs = parse_log_file(logfile)
            result[algo][matrix].setdefault(workers, []).extend(runs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outpath = base / f"{timestamp}_vine.json"
    outpath.write_text(json.dumps(result, indent=2))
    print(f"Written to {outpath}")

if __name__ == "__main__":
    main()
