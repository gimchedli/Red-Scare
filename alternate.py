'''
Alternate Return ‘true’ if there is a path from s to t that alternates
between red and non-red vertices. To be precise, a path v1, . . . , vl is
alternating if for each i ∈{1, . . . , l−1}, exactly one endpoint of the
edge vi vi+1 is red. Otherwise, return ‘false.’ In Gex, the answer is
‘yes’ (because of the path 0, 5, 6, 7, 3.)
'''

import sys
from collections import deque
from utils.parser import parse_input
from utils.test_runner_new import run_tests


def solve_alternate(input):
    '''
    BFS, where we ignore edges between two red vertices or two non-red vertices'''
    parsed = parse_input(input)
    s,t,adj, R = parsed['s'], parsed['t'], parsed['adj'], parsed['R']

    # we need to use a dict instead of list to handle string vertices
    dist = {s: 0}
    q = deque([s])

    while q:
        u = q.popleft()
        if u == t:
            return 'true'

        for v in adj.get(u, []):
            if (u in R) == (v in R):
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return 'false'

# only run when executed directly, so utils/run_all.py can import solve_alternate
if __name__ == '__main__':
    run_tests(solve_alternate)