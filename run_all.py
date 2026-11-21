'''
Runs all five solvers on every instance in data/ and writes results.txt.

Usage:
    python3 run_all.py

Output: a tab-separated table, one row per instance, sorted naturally
(common-1-20 before common-1-100), with the columns
    instance  n  A  F  M  N  S
for Alternate, Few, Many, None and Some. A cell holds the answer, '?!' if the
problem is NP-hard for that graph, or 'ERROR' if the solver crashed.
'''

import os
import sys
import time

# make this work no matter which folder it is run from:
# put the repo root (the folder this file is in) on the import path and use it
# as the working directory, so `utils.*`, the solver files and data/ are all found
# OLD (when this file lived in utils/, the root was one folder up):
# ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from utils.test_runner_new import natural_key

from alternate import solve_alternate
from few import solve_few
from many import solve_many
from none import solve_none
from some import solve_some

DATA_DIR = 'data'
OUTPUT_FILE = 'results.txt'

SOLVERS = [
    ('A', solve_alternate),
    ('F', solve_few),
    #('M', solve_many),
    ('N', solve_none),
    #('S', solve_some),
]


def run_all():
    files = sorted(
        (f for f in os.listdir(DATA_DIR) if f.endswith('.txt')),
        key=natural_key,
    )

    rows = [['instance', 'n'] + [name for name, _ in SOLVERS]]
    total_start = time.perf_counter()

    for fileName in files:
        with open(os.path.join(DATA_DIR, fileName)) as file:
            lines = file.read().splitlines()

        instance = fileName.removesuffix('.txt')
        n = lines[0].split()[0]
        row = [instance, n]

        for name, solver in SOLVERS:
            start = time.perf_counter()
            try:
                result = solver(lines)
            except Exception as e:
                print(f'Error: {name} on {instance}: {e}', file=sys.stderr)
                result = 'ERROR'
            elapsed = time.perf_counter() - start
            if elapsed > 10:
                print(f'Slow: {name} on {instance} took {elapsed:.1f} s', file=sys.stderr)
            row.append(str(result))

        rows.append(row)
        print('\t'.join(row))

    with open(OUTPUT_FILE, 'w') as out:
        for row in rows:
            out.write('\t'.join(row) + '\n')

    total = time.perf_counter() - total_start
    print(f'\nWrote {len(rows) - 1} instances to {OUTPUT_FILE} in {total:.1f} s', file=sys.stderr)


if __name__ == '__main__':
    run_all()
