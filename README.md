# QTreeVine
Sparse linear algebra in [Vine](https://github.com/VineLang/vine)

# How to run

Explore options of ```run``` in [documentation](https://vine.dev/docs/tooling/cli). 

1. Use [official instructions](https://vine.dev/docs/starting/installation) to install ```vine```.
2. ```vine run src/tests.vi --lib src/lib``` to run all tests.
3. ```vine run src/run_BFS.vi --lib src/lib``` to run BFS example.
4. ```vine run src/run_SSSP.vi --lib src/lib``` to run SSSP example.
5. ```vine run src/run_TriangleCount.vi --lib src/lib``` to run TriangleCount example.

For semi-automatic run you can use ```run.py```. It allows you to run specific algorithm on specific matrix multiple times with different number of workers.
1. Set ```PROGRAM_FILE```. This file will be executed.
2. Configure range for ```workers```.
3. Configure range for ```run`` (number of runs with specific configuration).
4. Output will be placed in ```logs\``` directory. This directory will be created automatically if does not exists.
5. All logs for specific rum will be **added to the end** of the respective log file (if exists). So, do not forget to clean ```logs``` directory if necessary.
