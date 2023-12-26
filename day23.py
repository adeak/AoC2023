from collections import defaultdict
from functools import cache

import numpy as np

valid_directions = dict(zip('><v^', 'rldu'))
reverses = dict(zip('rldu', 'lrud'))


def day23(inp, part2=False):
    board = np.array(list(map(list, inp.strip().splitlines())))

    start_j = (board[0, :] == '.').nonzero()[0].item()
    end_j = (board[-1, :] == '.').nonzero()[0].item()
    start = 0, start_j
    end = board.shape[0] - 1, end_j

    start_edge = start, 'd'
    paths = {start_edge}  # start position and orientation
    sections = defaultdict(dict)  # (start pos, direction) -> ((end pos, direction) ->  number of steps))
    seens = set(start_edge)  # set of (pos, direction) pairs for good measure
    while paths:
        start, direction = paths.pop()
        section_length = 0

        pos = start
        heading = direction
        while True:
            pos = translate(pos, heading)
            section_length += 1
            if (pos, heading) in seens:
                # already been here
                if part2:
                    break
            seens.add((pos, heading))

            next_edges = set()
            for next_heading in set('lrdu') - {reverses[heading]}:
                next_pos = translate(pos, next_heading)
                next_pos_arr = np.array(next_pos)
                if (next_pos_arr < 0).any() or (next_pos_arr >= board.shape).any():
                    # out of bounds; should only happen at end
                    continue
                next_tile = board[next_pos]
                if next_tile == '#':
                    # wall that way
                    continue
                if not part2:
                    if next_tile in valid_directions and valid_directions[next_tile] != next_heading:
                        # we can't go that way either
                        continue
                next_edges.add((next_pos, next_heading))

            if not next_edges:
                # we've run into a dead end (potentially due to a steep slope), end path
                sections[start, direction][pos, heading] = section_length
                break

            if len(next_edges) == 1:
                # no fork
                heading = next_edges.pop()[1]
                continue

            # otherwise we have a fork, stop this path and start new ones
            section_length += 1
            for next_pos, next_heading in next_edges:
                sections[start, direction][next_pos, next_heading] = section_length
                paths.add((next_pos, next_heading))
            break

    # now for each pair of sections generate crossing info (only for part 2)
    if part2:
        crossings = defaultdict(lambda: defaultdict(set))  # start -> (end -> set of crossing (start, end) pairs)
        for section_start, end_dict in sections.items():
            for section_end in end_dict:
                section_tiles = generate_path_from_section(section_start, section_end, board)
                for other_section_start, other_end_dict in sections.items():
                    if other_section_start == section_start or other_section_start == section_end:
                        continue
                    for other_section_end in other_end_dict:
                        if other_section_end == section_start or other_section_end == section_end:
                            continue
                        other_section_tiles = generate_path_from_section(other_section_start, other_section_end, board)
                        if section_tiles & other_section_tiles:
                            # we have an overlap
                            crossings[section_start][section_end].add((other_section_start, other_section_end))
                            crossings[other_section_start][other_section_end].add((section_start, section_end))

    metapaths = [(start_edge,)]
    longest = 0
    while metapaths:
        metapath = metapaths.pop()
        last_edge = last_pos, last_direction = metapath[-1]
        if last_pos == end:
            # we might have a winner
            path_length = sum(
                sections[first][second]
                for first, second in zip(metapath, metapath[1:])
            )
            longest = max(longest, path_length)
            continue

        for candidate in sections[last_edge]:
            # try to find a next stop
            if candidate in metapath:
                continue
            next_metapath = metapath + (candidate,)
            if part2:
                # check for self-intersections
                for first, second in zip(metapath, metapath[1:]):
                    if (metapath[-1], candidate) in crossings[first][second]:
                        # we'd have an intersection
                        break
                else:
                    # no intersection
                    metapaths.append(next_metapath)
            else:
                # we can't have intersections
                metapaths.append(next_metapath)

    return longest


@cache
def translate(pos, direction):
    """Step a 2-index position tuple in a given direction."""
    if direction == 'l':
        return pos[0], pos[1] - 1
    if direction == 'r':
        return pos[0], pos[1] + 1
    if direction == 'd':
        return pos[0] + 1, pos[1]
    if direction == 'u':
        return pos[0] - 1, pos[1]


def is_metapath_intersecting(metapath, board):
    seens = set()
    for start, end in zip(metapath, metapath[1:]):
        next_seens = generate_path_from_section(start, end)
        next_seens.discard(end[0])
        if seens & next_seens:
            return True
        seens.update(next_seens)
    return False


def generate_path_from_section(start, end, board, memo={}):
    # no @cache because board is not hashable
    # "path" is a lie, just generate seen tiles
    if (start, end) in memo:
        return memo[start, end]

    pos, direction = start
    seens = {pos}
    heading = direction
    while True:
        pos = translate(pos, heading)
        if pos in seens:
            raise AssertionError('wtf')
        seens.add(pos)
        if pos == end[0]:
            if heading != end[1]:
                # we'd self-intersect at 'end' later (unlikely but possible?)
                raise AssertionError('wtf')
            # we've covered the start -> end section
            memo[start, end] = seens
            return seens

        next_edges = set()
        for next_heading in set('lrdu') - {reverses[heading]}:
            next_pos = translate(pos, next_heading)
            next_pos_arr = np.array(next_pos)
            if (next_pos_arr < 0).any() or (next_pos_arr >= board.shape).any():
                # out of bounds; should only happen at end
                continue
            next_tile = board[next_pos]
            if next_tile == '#':
                # wall that way
                continue
            next_edges.add((next_pos, next_heading))

        if not next_edges:
            # we've run into a dead end, shouldn't happen
            raise AssertionError('wtf')

        if len(next_edges) == 1:
            # no fork
            heading = next_edges.pop()[1]
            continue

        # otherwise we have a fork, we need the direction corresponding to "end"
        heading = next(next_edge[1] for next_edge in next_edges if next_edge == end)


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp), day23(testinp, part2=True))
    inp = open('day23.inp').read()
    print(day23(inp), day23(inp, part2=True))
