'''
Many Return the maximum number of red vertices on any path from
s to t. To be precise, let P be the set of s,t-paths and let r(p) denote
the number of red vertices on a path p. Return max{r(p): p ∈ P}.
If no path from s to t exists, return '-1'. In Gex, the answer is '2'
(because of the path 0, 5, 6, 7, 3.)
'''

from collections import deque
from utils.parser import parse_input
from utils.test_runner_new import run_tests


# Iterative backtracking DFS over simple paths from s to t, maximizing count in R within a step budget
def _exact_many(sub, s, t, R, budget=50_000_000):
    best = -1
    steps = 0
    visited = {s}
    stack = [(s, iter(sub[s]), int(s in R))]
    while stack:
        u, it, cnt = stack[-1]
        if u == t:
            best = max(best, cnt)
            visited.discard(u)
            stack.pop()
            continue
        for v in it:
            if v not in visited:
                steps += 1
                if steps > budget:
                    return None
                visited.add(v)
                stack.append((v, iter(sub[v]), cnt + int(v in R)))
                break
        else:
            visited.discard(u)
            stack.pop()
    return best


def solve_many(input):
    
    #1 - Input reading and base case handling
    p = parse_input(input)
    s, t, adj, R, directed = p['s'], p['t'], p['adj'], p['R'], p['directed']

    if s == t:
        return int(s in R)

    #2 - BFS from s to find reachable vertices
    reach, q = {s}, deque([s])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in reach:
                reach.add(v)
                q.append(v)
    if t not in reach:
        return -1

    #3 - source pruning
    sub = {u: ([] if u == t else [v for v in adj.get(u, []) if v in reach and v != s])
           for u in reach}

    #4 - reverse BFS from t to find useful vertices and prune dead ends
    radj = {}
    for u in sub:
        for v in sub[u]:
            radj.setdefault(v, []).append(u)
    useful, q = {t}, deque([t])
    while q:
        v = q.popleft()
        for u in radj.get(v, []):
            if u not in useful:
                useful.add(u)
                q.append(u)
    sub = {u: [v for v in sub[u] if v in useful] for u in useful}

    #5 - Topological sort (Kahn's algorithm) for directed graphs; fallback if undirected or cyclic
    order = []
    if directed:
        indeg = {u: 0 for u in useful}
        for u in useful:
            for v in sub[u]:
                indeg[v] += 1
        q = deque(u for u in useful if indeg[u] == 0)
        while q:
            u = q.popleft()
            order.append(u)
            for v in sub[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

    if not directed or len(order) < len(useful):
        res = _exact_many(sub, s, t, R)
        return '?!' if res is None else res

    #6 - DAG DP in reverse topological order: best[u] = max nodes in R on a path from u to t
    NEG = float('-inf')
    best = {u: NEG for u in useful}
    best[t] = int(t in R)
    for u in reversed(order):
        if u != t:
            m = max((best[v] for v in sub[u]), default=NEG)
            if m > NEG:
                best[u] = m + int(u in R)
    return best[s]


if __name__ == '__main__':
    run_tests(solve_many)