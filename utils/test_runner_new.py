import os
import re
from collections.abc import Callable


def run_tests(solver: Callable[[list[str]], int]):
    answers = {}
    for fileName in os.listdir("data/"):
        with open(f"data/{fileName}", "r") as file:
            try:
                if fileName == "README.md":
                    continue

                result = solver(file.read().splitlines())
                answers[fileName] = result
            except Exception as e:
                print(f"Error while running testfile: {fileName}")
                print(e)
                answers[fileName] = f"Error: {e}"
    sorted_answers = dict(
        sorted(answers.items(), key=lambda item: natural_key(item[0]))
    )
    for fileName, result in sorted_answers.items():
        print(fileName, result)


def natural_key(name: str):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", name)
    ]
