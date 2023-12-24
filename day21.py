from collections import defaultdict

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
        for pos, map_pos in edges:
            if pos not in edge_teleport:
                continue
            for neighb, map_delta in edge_teleport[pos]:
                neighb_edge = neighb, translate(map_pos, map_delta)
                if neighb_edge not in last_edges:
                    next_edges.add(neighb_edge)
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


def day21_part2hack(inp):
    board = np.array(list(map(list, inp.strip().splitlines())))
    start = tuple(np.array((board == 'S').nonzero()).ravel())
    board[start] = '.'

    steps = 26501365
    assert start[0] == start[1]
    assert board.shape == (2*start[0] + 1, 2*start[1] + 1)
    assert (steps - start[0]) % board.shape[0] == 0
    assert (steps - start[1]) % board.shape[1] == 0

    assert (board[0, :] == '.').all()
    assert (board[-1, :] == '.').all()
    assert (board[:, 0] == '.').all()
    assert (board[:, -1] == '.').all()
    assert (board[start[0], :] == '.').all()
    assert (board[:, start[1]] == '.').all()

    assert (steps - start[0]) % board.shape[0] == 0

    # 1. we always have an alternating checkerboard of tiles based on parity
    #    within the area that's been reached by the front of the walk
    # 2. we mostly progress along a circle in Manhattan metric -> a diamond
    # 3. for part 2 we need exactly 26501365 == 202300*131 + 65 steps, i.e.
    #    65 steps from center S to reach the edge of the 131-wide board, then
    #    202300 full board distances
    # 4. if it weren't for the caves on the map we could just count the even/odd
    #    parity garden tiles corresponding to the (202300 * 2 + 1)-width diamond
    #    but due to nooks and crannies we have to consider each corner of the
    #    small map and check which garden tiles are reachable in 131 steps from
    #    corners and edge centers
    #
    # 5. map blocks grow out like this:
    #
    #            *4*
    #           *434*
    #          *43234*
    #         *4321234*
    #         432101234
    #         *4321234*
    #          *43234*
    #           *434*
    #            *4*
    #
    # 6. so we have 4*202300 edge tiles, out of which 4 are one of each tile
    #    where we start from one of the edge centers (top, bottom, left or right)
    #    and take 130 steps, and 202299 edges each where we start from one of the
    #    corners and take 130 + 65 steps
    # 7. we also have 4*202300 edges (marked with asterisks above) that are
    #    202300 pieces each where we start from one of the corners and take 65
    #    steps.
    # 8. finally, we have 1 + 4*202299 + 4*((202298)*(202298 + 1)//2) == 81850175401
    #    full tiles but with alternating parities outside from the center...
    #
    #
    edge_size = 1
    evenodds = [0, edge_size]
    for step in range((steps - start[0]) // board.shape[0]):
        parity = step % 2
        if edge_size == 1:
            edge_size = 4
        else:
            edge_size += 4
        evenodds[parity] += edge_size
    evenodds[parity] -= edge_size

    # evenodds[1] are the full tiles of the same parity as the middle (starting) one
    # evenodds[0] are the full tiles with the opposite parity
    # edge_size are the number of "full" edge tiles (index 4 in the above graph)
    #    of parity parity (same as middle tile's parity for 202300 tile steps)
    # and there are also edge_size "corner" edge tiles (asterisks above)
    #    of parity (1 - parity) (opposite as middle tile's parity for 202300 tile steps)

    assert sum(evenodds) == 1 + 4*202299 + 4*((202298)*(202298 + 1)//2)
    assert edge_size == 4 * 202300
    assert parity == 1

    # actually, even better:
    #    1. simulate the above figure, i.e. 65 + 4*131 steps
    #    2. cut out the appropriate kinds of tiles to sum up their blinking counts
    #       (i.e. do the same as main part 2, with more accounting)

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

    # set up map to map jump info
    edge_teleport = defaultdict(set)  # pos -> (next pos, next map block delta)
    for i in range(board.shape[0]):
        edge_teleport[i, 0].add(((i, board.shape[1] - 1), 'L'))
        edge_teleport[i, board.shape[1] - 1].add(((i, 0), 'R'))
    for j in range(board.shape[1]):
        edge_teleport[0, j].add(((board.shape[0] - 1, j), 'U'))
        edge_teleport[board.shape[0] - 1, j].add(((0, j), 'D'))

    last_edges = set()
    edges = {(start, (0, 0))}  # position, map block position
    blinking_counts = defaultdict(lambda: [0, 0])
    blinking_counts[0, 0] = [0, 1]  # map index -> blinking count for each parity
    for step in range(steps):
        parity = step % 2

        # handle case where we stay within the same map
        next_edges = {
            (neighb, map_pos)
            for pos, map_pos in edges
            for neighb in connectivity[pos]
            if (neighb, map_pos) not in last_edges
        }

        # handle infinite boundary condition
        for pos, map_pos in edges:
            if pos not in edge_teleport:
                continue
            for neighb, map_delta in edge_teleport[pos]:
                neighb_edge = neighb, translate(map_pos, map_delta)
                if neighb_edge not in last_edges:
                    next_edges.add(neighb_edge)

        for _, map_pos in next_edges:
            blinking_counts[map_pos][parity] += 1

        last_edges = edges
        edges = next_edges

        if step == start[0] + 4 * board.shape[0] - 1:
            # sanity check
            assert len({tuple(blinking_counts[index]) for index in [(-1, -3), (-2, -2), (-3, -1)]}) == 1
            assert len({tuple(blinking_counts[index]) for index in [(-1, 3), (-2, 2), (-3, 1)]}) == 1
            assert len({tuple(blinking_counts[index]) for index in [(1, 3), (2, 2), (3, 1)]}) == 1
            assert len({tuple(blinking_counts[index]) for index in [(1, -3), (2, -2), (3, -1)]}) == 1
            assert len({tuple(blinking_counts[index]) for index in [(-1, -4), (-2, -3), (-3, -2), (-4, -1)]}) == 1
            assert blinking_counts[0, -2] == blinking_counts[0, 0] == blinking_counts[0, 2]
            assert blinking_counts[-1, -2] == blinking_counts[0, -3] == blinking_counts[1, 2]

            linear_tile_size = (steps - start[0]) // board.shape[0]  # 202300, same as edge_size//4

            part2 = (
                evenodds[1] * blinking_counts[0, 0][parity] +  # full tiles with same parity as start
                evenodds[0] * blinking_counts[0, 0][1 - parity] +  # full tiles with opposite parity
                blinking_counts[0, -4][parity] + blinking_counts[0, 4][parity] +  # horizontal diamond corners
                blinking_counts[-4, 0][parity] + blinking_counts[4, 0][parity] +  # vertical diamond corners
                (linear_tile_size - 1) * blinking_counts[-1, -3][parity] +  # top left "4" edge
                (linear_tile_size - 1) * blinking_counts[-1, 3][parity] +  # top right "4" edge
                (linear_tile_size - 1) * blinking_counts[1, 3][parity] +  # bottom right "4" edge
                (linear_tile_size - 1) * blinking_counts[1, -3][parity] +  # bottom left "4" edge
                linear_tile_size * blinking_counts[-1, -4][parity] +  # top left "*" edge
                linear_tile_size * blinking_counts[-1, 4][parity] +  # top right "*" edge
                linear_tile_size * blinking_counts[1, 4][parity] +  # bottom right "*" edge
                linear_tile_size * blinking_counts[1, -4][parity]  # bottom left "*" edge
            )
            break

    return part2


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp, steps=6), day21(testinp, part2=True, steps=10), day21(testinp, part2=True, steps=1000))
    inp = open('day21.inp').read()
    print(day21(inp), day21_part2hack(inp))
