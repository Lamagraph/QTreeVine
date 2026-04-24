# QTreeVine
Sparse linear algebra in [Vine](https://github.com/VineLang/vine)

# How to run

Explore options of ```run``` in [documentation](https://vine.dev/docs/tooling/cli). 

1. Use [official instructions](https://vine.dev/docs/starting/installation) to install ```vine```.
2. ```vine run src/tests.vi --lib src/lib``` to run all tests.
3. ```vine run src/run_BFS.vi --lib src/lib``` to run BFS example.
4. ```vine run src/run_SSSP.vi --lib src/lib``` to run SSSP example.
5. ```vine run src/run_TriangleCount.vi --lib src/lib``` to run TriangleCount example.

For semi-automatic run you can use ```run.py```:

```bash
python3 run.py {BFS,SSSP,TriangleCount} [matrix_file]
               [-r RUNS] [-w WORKERS_START WORKERS_END] [-H HEAP_GB]
```

- `{BFS,SSSP,TriangleCount}` — algorithm to run (required)
- `matrix_file` — path to .mtx file (optional; overrides value in source)
- `-r RUNS` — number of runs per configuration (default: 1)
- `-w WORKERS_START WORKERS_END` — worker range (end is exclusive) (default: 4 5)
- `-H HEAP_GB` — heap size in GB, converted to bytes and passed to vine (optional; default: vine's built-in limit)

Logs are placed in `logs_{algo}[_{matrix_stem}]/` with files named `{workers}[_H{heap}G].log`. Run output is **appended** to the respective log file. The source file is temporarily modified to set `matrix_file` if a matrix override is given, and restored after all runs.
