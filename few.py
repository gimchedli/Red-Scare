"""
Few Return the minimum number of red vertices on any path from s
to t. To be precise, let P be the set of s, t-paths and let r(p) denote
red scare! 2
the number of red vertices on a path p. Return min{r(p): p ∈ P }.
If no path from s to t exists, return '-1'. In Gex, the answer is 0
(because of the path 0, 1, 2, 3.)

"""

from collections import deque
from utils.parser import parse_input
from utils.test_runner import run_tests


def solve_few(input):
    """
    0-1 BFS, where we give red vertices a weight of 1
    Dijkstras would also work, but 0-1 BFS is optimal for 0 or 1 weights
    https://cp-algorithms.com/graph/01_bfs.html
    """
    parsed = parse_input(input)
    s, t, adj, R = parsed["s"], parsed["t"], parsed["adj"], parsed["R"]

    # deque instead of 2 queues, normal vertices get pushed to the left,
    # red ones to the right; we always pop from left
    q = deque([s])

    # we need to use a dict instead of list to handle string vertices
    dist = {s: 1 if s in R else 0}

    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            d = 1 if v in R else 0
            if dist.get(u, 0) + d < dist.get(v, float("inf")):
                dist[v] = dist[u] + d
                if d == 0:
                    q.appendleft(v)
                else:
                    q.append(v)
    return dist.get(t, -1)


if __name__ == "__main__":
    run_tests(solve_few)
