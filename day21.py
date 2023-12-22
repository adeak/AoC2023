from collections import defaultdict, deque

import numpy as np


def day21(inp, steps=None, part2=False):
    board = np.array(list(map(list, inp.strip().splitlines())))

    start = tuple(np.array((board == 'S').nonzero()).ravel())
    board[start] = '.'

    # pre-process adjacency
    connectivity = defaultdict(set)
    for i, j in np.indices(board.shape).reshape(2, -1).T:
        pos = i, j
        if board[pos] == '#':
            # can't start from rock
            continue
        for direction in 'RD':
            neighb = translate(pos, direction)
            neighb_arr = np.array(neighb)
            if (neighb_arr < 0).any() or (neighb_arr >= board.shape).any():
                # out of bounds
                continue
            if board[neighb] == '#':
                # rock
                continue
            connectivity[pos].add(neighb)
            connectivity[neighb].add(pos)

    if part2:
        if steps is None:
            steps = 26501365

        # prepare for infinite boundary condition
        assert (board[0, :] == '.').all()
        assert (board[-1, :] == '.').all()
        assert (board[:, 0] == '.').all()
        assert (board[:, -1] == '.').all()

        edge_teleport = defaultdict(set)  # pos -> (next pos, next map block delta)
        for i in range(board.shape[0]):
            edge_teleport[i, 0].add(((i, board.shape[1] - 1), 'L'))
            edge_teleport[i, board.shape[1] - 1].add(((i, 0), 'R'))
        for j in range(board.shape[1]):
            edge_teleport[0, j].add(((board.shape[0] - 1, j), 'U'))
            edge_teleport[board.shape[0] - 1, j].add(((0, j), 'D'))

    else:
        if steps is None:
            steps = 64

    last_edges = set()
    edges = {(start, (0, 0))}  # position, map block position
    blinking_counts = [0, 1]  # one for each parity
    for step in range(steps):
        parity = step % 2

        # handle case where we stay within the same map
        next_edges = {
            (neighb, map_pos)
            for pos, map_pos in edges
            for neighb in connectivity[pos]
            if (neighb, map_pos) not in last_edges
        }
        if not part2:
            blinking_counts[parity] += len(next_edges)
            last_edges = edges
            edges = next_edges
            continue

        # handle infinite boundary condition
        next_teleporting_edges = set()
        for pos, map_pos in edges:
            if pos not in edge_teleport:
                continue
            for neighb, map_delta in edge_teleport[pos]:
                neighb_edge = neighb, translate(map_pos, map_delta)
                if neighb_edge not in last_edges:
                    next_teleporting_edges.add(neighb_edge)
        next_edges |= next_teleporting_edges
        blinking_counts[parity] += len(next_edges)

        last_edges = edges
        edges = next_edges

    return blinking_counts[parity]


def translate(pos, direction, length=1):
    """Step a 2-index position tuple in a given direction."""
    if direction == 'L':
        return pos[0], pos[1] - length
    if direction == 'R':
        return pos[0], pos[1] + length
    if direction == 'D':
        return pos[0] + length, pos[1]
    if direction == 'U':
        return pos[0] - length, pos[1]


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp, steps=6), day21(testinp, part2=True, steps=10), day21(testinp, part2=True, steps=1000))
    inp = open('day21.inp').read()
    print(day21(inp), day21(inp, part2=True))
