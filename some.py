'''
Some Return 'true' if there is a path from s to t that includes at least
one vertex from R. Otherwise, return 'false'. In Gex, the answer is
'yes' (in fact, two such paths exist: the path 0, 4, 3 and the path 0,
5, 6, 7, 3.
'''
from utils.parser import parse_input
from utils.test_runner import run_tests
from collections import deque


# Recursive DFS coloring for cycle detection - https://cp-algorithms.com/graph/finding-cycle.html
def has_cycle(s,t,adj, V):
    def BFS():
        ...

    colors = {'s' : 0}
    



def solve_some(input):
   inp = parse_input(input)
   s,t,R, adj, directed, V = inp['s'], inp['t'], inp['R'], inp['adj'], inp['directed'], inp['vertices']

   if directed:
        # check if acyclic, then BFS s -> any r -> t else return False
        if has_cycle(s,t,adj, V):
            # BFS: s -> any r -> t
            ...

        # On directed, cyclic graphs the problem is NP-Hard
        return False

    # Max-flow

    
    





run_tests(solve_some)