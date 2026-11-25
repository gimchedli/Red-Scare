'''
Some Return 'true' if there is a path from s to t that includes at least
one vertex from R. Otherwise, return 'false.' In Gex, the answer is
'yes' (in fact, two such paths exist: the path 0, 4, 3 and the path 0,
5, 6, 7, 3.)
'''

from collections import deque
from utils.parser import parse_input
from utils.test_runner import run_tests


# BFS reachability from a given source vertex
def _reach(adj, src):
    seen, q = {src}, deque([src])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


# Cycle check via Kahn's topological sort on a given vertex subset
def _is_dag(nodes, adj):
    indeg = {u: 0 for u in nodes}
    for u in nodes:
        for v in adj.get(u, []):
            if v in indeg:
                indeg[v] += 1
    q = deque(u for u in nodes if indeg[u] == 0)
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj.get(u, []):
            if v in indeg:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
    return seen == len(nodes)


# Vertex-disjoint path test via unit-capacity max flow (Edmonds-Karp / augmenting paths) on a split graph
def _undirected_some(nodes, adj, s, t, reds):
    
    nodes = list(nodes)
    idx = {v: i for i, v in enumerate(nodes)}
    N = len(nodes)
    z = 2 * N
    to, cap = [], []
    g = [[] for _ in range(2 * N + 1)]

    def add(u, v, c):
        g[u].append(len(to)); to.append(v); cap.append(c)
        g[v].append(len(to)); to.append(u); cap.append(0)

    # Node splitting (v_in -> v_out) to enforce vertex-disjointness
    for v in nodes:
        add(2 * idx[v], 2 * idx[v] + 1, 1)              
    for u in nodes:
        for v in adj.get(u, []):
            add(2 * idx[u] + 1, 2 * idx[v], 1)           
    add(2 * idx[s] + 1, z, 1)
    add(2 * idx[t] + 1, z, 1)
    orig = cap[:]

    for r in reds:
        src = 2 * idx[r] + 1
        changed = []
        flow = 0
        for _ in range(2):
            par = {src: -1}
            q = deque([src])
            while q and z not in par:
                u = q.popleft()
                for e in g[u]:
                    v = to[e]
                    if cap[e] > 0 and v not in par:
                        par[v] = e
                        q.append(v)
            if z not in par:
                break
            v = z
            while par[v] != -1:
                e = par[v]
                cap[e] -= 1
                cap[e ^ 1] += 1
                changed.append(e)
                v = to[e ^ 1]
            flow += 1
        for e in changed:
            cap[e] = orig[e]
            cap[e ^ 1] = orig[e ^ 1]
        if flow == 2:
            return True
    return False


def solve_some(input):
    #1 - Input reading and base case handling
    p = parse_input(input)
    s, t, adj, R, directed = p['s'], p['t'], p['adj'], p['R'], p['directed']

    if s == t:
        return 'true' if s in R else 'false'

    #2 - Forward BFS from s to find reachable vertices
    fwd = _reach(adj, s)
    if t not in fwd:
        return 'false'
    if s in R or t in R:
        return 'true'       
    
    #3 - Directed case: backward reachability, red filter, and DAG check
    if directed:
        radj = {}
        for u in fwd:
            for v in adj.get(u, []):
                radj.setdefault(v, []).append(u)
        bwd = _reach(radj, t)
        between = fwd & bwd
        if not any(r in between for r in R):
            return 'false'
        if _is_dag(between, adj):
            return 'true'
        return '?!'

    #4 - Undirected case: filter reachable red vertices and test via flow helper
    reds = [r for r in R if r in fwd]
    return 'true' if _undirected_some(fwd, adj, s, t, reds) else 'false'


if __name__ == '__main__':
    run_tests(solve_some)