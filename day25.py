from collections import defaultdict
from copy import deepcopy
from itertools import count


def day25(inp):
    lines = inp.strip().splitlines()

    connections = defaultdict(set)
    for line in lines:
        source, _, targets = line.partition(': ')
        targets = targets.split()
        connections[source].update(targets)
        for target in targets:
            connections[target].add(source)

    # do BFS to find longest distance
    longest = 0
    for start in connections:
        edges = set(connections[start])
        seens = set()
        for distance in count(1):
            next_edges = set()
            for edge in edges:
                longest_pair = {start, edge}
                seens.add(edge)
                for next_edge in connections[edge]:
                    if next_edge not in seens:
                        next_edges.add(next_edge)
            edges = next_edges
            if not edges:
                break

    # hope that the longest distance is between the two eventual islands -> one bridge is on path
    # find longest path, try to cut each link
    # unfortunately cutting any of the links won't increase the path length, so we'll have to
    # consider each link in the path to be cut
    longest_path = find_path(*longest_pair, connections)

    # dumb but foolproof: break a link, find new longest path, break another link...
    # after depth 3 we'll end up with a configuration where the two ends are disconnected
    for link_start, link_end in zip(longest_path, longest_path[1:]):
        connections_cut = deepcopy(connections)
        connections_cut[link_start].remove(link_end)
        connections_cut[link_end].remove(link_start)
        next_longest_path = find_path(*longest_pair, connections_cut)
        next_longest = len(next_longest_path) - 1
        for next_link_start, next_link_end in zip(next_longest_path, next_longest_path[1:]):
            connections_cut2 = deepcopy(connections_cut)
            connections_cut2[next_link_start].remove(next_link_end)
            connections_cut2[next_link_end].remove(next_link_start)
            next2_longest_path = find_path(*longest_pair, connections_cut2)
            next2_longest = len(next2_longest_path) - 1
            for next2_link_start, next2_link_end in zip(next2_longest_path, next2_longest_path[1:]):
                connections_cut3 = deepcopy(connections_cut2)
                connections_cut3[next2_link_start].remove(next2_link_end)
                connections_cut3[next2_link_end].remove(next2_link_start)
                next2_longest_path = find_path(*longest_pair, connections_cut3)
                if next2_longest_path is None:
                    # done
                    seens = set()
                    edges = {next(iter(longest_pair))}
                    while edges:
                        seens.update(edges)
                        edges = set.union(*[connections_cut3[edge] for edge in edges]) - seens
                        if not edges:
                            return len(seens) * (len(connections) - len(seens))


def find_path(start, end, connections):
    edges = {start}
    seens = set()
    comefrom = {}
    while True:
        next_edges = set()
        seens.update(edges)
        for edge in edges:
            for next_edge in connections[edge]:
                if next_edge in seens:
                    continue
                next_edges.add(next_edge)
                comefrom[next_edge] = edge

                if next_edge == end:
                    # reconstruct path, orientation is irrelevant
                    path = [end]
                    while path[-1] in comefrom:
                        path.append(comefrom[path[-1]])
                    return path
        edges = next_edges
        if not edges:
            # no path exists!
            return None


if __name__ == "__main__":
    testinp = open('day25.testinp').read()
    print(day25(testinp))
    inp = open('day25.inp').read()
    print(day25(inp))
