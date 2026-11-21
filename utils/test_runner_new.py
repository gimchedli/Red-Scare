import os
import re
import time
from collections.abc import Callable

def run_tests(solver: Callable[[list[str]], int] ):
    answers = {}
    for fileName in os.listdir('data/'):
        with open(f'data/{fileName}', 'r') as file:
            try:
                if fileName == 'README.md':
                    continue

                start = time.perf_counter()
                result = solver(file.read().splitlines())
                end = time.perf_counter()

                #print(f'Testfile {fileName} result: {result} - took: {(end - start) * 1e6:.1f} ms')
                #print(f'{fileName} {result}')
                answers[fileName] = result
            except Exception as e:
                print(f"Error while running testfile: {fileName}")
                print(e)
                answers[fileName] = f"Error: {e}"

        # OLD: plain string sort puts "common-1-1000" before "common-1-20" and
        # uppercase ("G-ex", "P3") before lowercase; it also re-sorted every iteration
        # sorted_answers = dict(sorted(answers.items(), key=lambda item: item[0]))

    # NEW: natural sort - compare digit runs as numbers, ignore case
    sorted_answers = dict(sorted(answers.items(), key=lambda item: natural_key(item[0])))
    for fileName, result in sorted_answers.items():
        print(fileName, result)



def natural_key(name: str):
    # "common-1-20.txt" -> ['common-', 1, '-', 20, '.txt']
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', name)]