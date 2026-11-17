import os
import time
from collections.abc import Callable

def run_tests(solver: Callable[[list[str]], int] ):
    for fileName in os.listdir('data/'):
        with open(f'data/{fileName}', 'r') as file:
            try:
                if fileName == 'README.md':
                    continue

                start = time.perf_counter()
                result = solver(file.read().splitlines())
                end = time.perf_counter()

                print(f'Testfile {fileName} result: {result} - took: {(end - start) * 1e6:.1f} ms')
            except Exception as e:
                print(f"Error while running testfile: {fileName}")
                print(e)