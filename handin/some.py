'''
Some Return 'true' if there is a path from s to t that includes at least
one vertex from R. Otherwise, return 'false.' In Gex, the answer is
'yes' (in fact, two such paths exist: the path 0, 4, 3 and the path 0,
5, 6, 7, 3.)
'''

from collections import deque
from parser import parse_input

# BFS reachability from a given source vertex,
# returns every vertex you can reach from 'src'.
def _reach(adj, src):
    seen, q = {src}, deque([src])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


# Cycle checking with Kahn's topological sort
def _is_dag(nodes, adj):
    # build incoming-degree map for the vertices
    indeg = {u: 0 for u in nodes}
    for u in nodes:
        for v in adj.get(u, []):
            if v in indeg: # needed since 'adj' may contain vertices outside of 'nodes'
                indeg[v] += 1

    # "remove" vertices with indeg 0 iteratively, and check if we can remove all vertices
    q = deque(u for u in nodes if indeg[u] == 0)
    removed = 0
    while q:
        u = q.popleft()
        removed += 1
        # foreach edge coming out of 'u', decrement the indegree of the target vertex 'v'
        for v in adj.get(u, []):
            if v in indeg:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
    return removed == len(nodes)


# Vertex-disjoint path test via unit-capacity max flow (Edmonds-Karp / augmenting paths) on a split graph
def _undirected_some(nodes, adj, s, t, reds):
    SINK = 'sink'
    cap = {} # cap[(u, v)] = capacity of edge (u, v)
    neighbors = {} # neighbors[u] = set of nodes u has an edge to (incl. reverse)

    def add(u, v, c):
        neighbors.setdefault(u, set()).add(v)
        cap[(u, v)] = cap.get((u, v), 0) + c
        # residual edge with capacity 0
        neighbors.setdefault(v, set()).add(u)
        cap.setdefault((v, u), 0)

    # we split vertices into 'in' and 'out' vertices to ensure vertex-disjointness
    # each vertex v is split into two nodes, (v,'in') -> (v,'out'), joined by an edge with capacity 1,
    # and all edges (u,v) are added as (u,'out') -> (v,'in') with capacity 1
    for v in nodes:
        add((v, 'in'), (v, 'out'), 1)
    for u in nodes:
        for v in adj.get(u, []):
            add((u, 'out'), (v, 'in'), 1)

    # add s_out/t_out --1-> sink
    add((s, 'out'), SINK, 1)
    add((t, 'out'), SINK, 1)

    for r in reds:
        c = dict(cap) # copy for each red vertex
        src = (r, 'out') # always start from r_out
        flow = 0
        
        # Try to send 2 units of flow from r: one must end at s, the other at t (each sink edge has capacity 1).
        # If both succeed, there are vertex-disjoint paths r->s and r->t, which form an s-t path through r.
        for _ in range(2):
            # BFS
            parent = {src: None}
            q = deque([src])
            while q and SINK not in parent:
                u = q.popleft()
                for v in neighbors.get(u, ()):
                    if c[(u, v)] > 0 and v not in parent:
                        parent[v] = u
                        q.append(v)
            if SINK not in parent: # BFS finished without reaching sink: try on a different red vertex
                break

            # walk backwards from the sink to the source along the path
            v = SINK
            while parent[v] is not None:
                u = parent[v]
                c[(u, v)] -= 1  # use up edge capacity
                c[(v, u)] += 1  # add residual capacity
                v = u
            flow += 1
        if flow == 2: # both r_out -> s_out -> sink and r_out -> t_out -> sink paths found
            return True
    return False

def solve_some(input):
    p = parse_input(input)
    s, t, adj, R, directed = p['s'], p['t'], p['adj'], p['R'], p['directed']

    if s == t:
        return 'true' if s in R else 'false'

    # Forward BFS from s to find reachable vertices
    fwd = _reach(adj, s)
    if t not in fwd:
        return 'false'
    if s in R or t in R:
        # trivially, if 't' is reachable from 's' (guaranteed by previous if branch)
        # and s ∈ R or t ∈ R, every path contains atleast 1 red vertex
        return 'true'
    
    # G is Directed case: backward reachability, red filter, and DAG check
    if directed:
        # Reverse adjacency dict for running BFS from 't'
        radj = {}
        for u in fwd:
            for v in adj.get(u, []):
                radj.setdefault(v, []).append(u)

        # 'bwd' = vertices in 'fwd' that can reach 't' (BFS from 't' on reversed edges),
        # so every vertex that could lie on some s-t path
        bwd = _reach(radj, t)

        if not any(r in bwd for r in R):
            return 'false'  # no red vertex lies on any s-t path        
        if _is_dag(bwd, adj): 
        # the s-t subgraph is acyclic, so s->r and r->t can't share a vertex, so joining them would give a simple path
            return 'true'
        
        return '?!' # for directed cyclic graphs, we cannot determine the answer in polynomial time (unless P=NP)

    # Undirected case: filter reachable red vertices and test via flow helper
    reds = [r for r in R if r in fwd]
    return 'true' if _undirected_some(fwd, adj, s, t, reds) else 'false'