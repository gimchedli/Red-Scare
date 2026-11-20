def parse_input(input: list[str]):
    '''
    Pass the raw input (file.read().splitlines())
    The function returns all possible values needed to solve the tasks


    Every input file is of the following form:
	n m r
	s t
	<vertices>
	<edges>

    The integer `n` is the number of vertices.
    The integer `m` is the number of edges.
    The integer `r` is the cardinality of *R*.

    `<vertices>` is a list of vertex names, one per line. Each vertex name is a string from `[_a-z0-9]+`.
    The names of vertices in R are followed by “` *`”.

    `<edges>` is a list of edges of the form
    u -- v
    for the undirected edge between *u* and *v*, or
    u -> v
    for the directed arc from *u* to *v*.
    '''
    n,m,r = [int(x) for x in input[0].split()]
    s,t = input[1].split()
    
    vertices = [v.split()[0] for v in input[2:n+2]]

    R = {v[:-2] for v in input[2:n+2] if ' *' in v}

    edges = []
    adj = {}

    directed = m > 0 and '->' in input[n+2]
    
    for edge in input[n+2 : n+m+2]:
        if directed:
            u,v = edge.split(' -> ')
        else:
            #undirected; add both directions
            u,v = edge.split(' -- ')
            adj.setdefault(v, []).append(u)

        edges.append((u,v))
        adj.setdefault(u, []).append(v)

    assert(len(R) == r)

    return {
        'n': n, 'm': m, 'r': r,
        's': s, 't': t,
        'vertices': vertices,
        'R': R,
        'directed': directed,
        'edges': edges,
        'adj': adj,
    }