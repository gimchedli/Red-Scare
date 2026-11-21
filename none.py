'''
None Return the length of a shortest s, t-path internally avoiding
R. To be precise, let P be the set of s, t-paths v1, . . . , vl such that
vi / ∈R if 1 < i < l. Let l(p) denote the length of a path p. Return
min{l(p) : p ∈P }. If no such path exists, return ‘-1’. Note that the
edge st, if it exists, is an s, t-path with l= 2. Thus, if st ∈E(G)
then the answer is 1, no matter the colour of s or t. In Gex, the
answer is 3 (because of the path 0, 1, 2, 3.)
'''

import sys
from collections import deque
from utils.parser import parse_input
from utils.test_runner_new import run_tests

def solve_none(input):
    '''
    BFS, where we ignore red vertices   
    '''

    parsed = parse_input(input)
    s,t,adj, R = parsed['s'], parsed['t'], parsed['adj'], parsed['R']

    dist = {s: 0}
    q = deque([s])

    while q:
        u = q.popleft()
        if u == t:
            #print(dist[u])
            return dist[u]

        for v in adj.get(u, []):
            if v in R and v != t:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return -1


# only run when executed directly, so utils/run_all.py can import solve_none
if __name__ == '__main__':
    run_tests(solve_none)