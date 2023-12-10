from collections import defaultdict
from itertools import count, repeat

import numpy as np


def day10(inp):
    sketch = np.array([list(line) for line in inp.strip().splitlines()])
    start = np.array([arr.item() for arr in (sketch == 'S').nonzero()])

    # a given pipe always means a step along current heading
    # and an optional heading change

    deltas = {
        'd': [1, 0],
        'u': [-1, 0],
        'l': [0, -1],
        'r': [0, 1],
    }
    new_headings = {
        '|': {'d': 'd', 'u': 'u'},
        '-': {'r': 'r', 'l': 'l'},
        'L': {'d': 'r', 'l': 'u'},
        'J': {'d': 'l', 'r': 'u'},
        '7': {'u': 'l', 'r': 'd'},
        'F': {'u': 'r', 'l': 'd'},
    }
    left_turns = defaultdict(int)
    left_turns.update({
        ('d', 'r'): 1,
        ('d', 'l'): -1,
        ('u', 'l'): 1,
        ('u', 'r'): -1,
        ('r', 'u'): 1,
        ('r', 'd'): -1,
        ('l', 'd'): 1,
        ('l', 'u'): -1,
    })

    # assume that S is only connected in one direction (no ambiguity at start)
    for heading in 'dulr':
        next_pos = start + deltas[heading]
        if (next_pos < 0).any() or (next_pos >= sketch.shape).any():
            # can't go that way
            continue
        next_tile = sketch[tuple(next_pos)]
        if heading in new_headings[next_tile]:
            # we have a valid connection
            break
    else:
        raise ValueError('No valid initial heading found...')

    # so we start from the start with known heading, walk the pipe
    pos = start.copy()
    initial_heading = heading
    loop_tiles = {tuple(pos)}  # tile positions that are in the loop
    rotations = 0  # number of 90 degree left turns
    for loop_length in count(1):
        pos += deltas[heading]
        next_tile = sketch[tuple(pos)]
        if next_tile == 'S':
            # we're done
            break

        loop_tiles.add(tuple(pos))
        new_heading = new_headings[next_tile][heading]
        # keep track of rotations for loop orientation
        rotations += left_turns[heading, new_heading]

        heading = new_heading

    # fill in 'S' tile to close loop
    rotations += left_turns[heading, initial_heading]
    # rotations == 4 for a left-turning loop, -4 for right-turning loop, starting with initial_heading
    lefty = rotations // 4 == 1

    part1 = loop_length // 2

    # part 2: check tiles on the "inside" side of the loop and flood fill
    pos = start.copy()
    heading = initial_heading
    inside_seeds = set()
    while True:
        pos += deltas[heading]
        next_tile = sketch[tuple(pos)]
        if next_tile == 'S':
            # we're done
            break

        seed_poses = []
        if next_tile == '|':
            if (heading == 'd' and lefty) or (heading == 'u' and not lefty):
                # O|I
                seed_poses = [pos + [0, 1]]
            else:
                # I|O
                seed_poses = [pos + [0, -1]]
        elif next_tile == '-':
            if (heading == 'r' and lefty) or (heading == 'l' and not lefty):
                # I
                # -
                # O
                seed_poses = [pos + [-1, 0]]
            else:
                # O
                # -
                # I
                seed_poses = [pos + [1, 0]]
        elif next_tile == 'L':
            if (heading == 'd' and lefty) or (heading == 'l' and not lefty):
                #
                # O L
                # O O
                pass
            else:
                #
                # I L
                # I I
                seed_poses = [pos + [1, 0], pos + [0, -1], pos + [1, -1]]
        elif next_tile == 'J':
            if (heading == 'r' and lefty) or (heading == 'd' and not lefty):
                #
                # J O
                # O O
                pass
            else:
                #
                # J I
                # I I
                seed_poses = [pos + [1, 0], pos + [0, 1], pos + [1, 1]]
        elif next_tile == '7':
            if (heading == 'u' and lefty) or (heading == 'r' and not lefty):
                #
                # O O
                # 7 O
                pass
            else:
                #
                # I I
                # 7 I
                seed_poses = [pos + [-1, 0], pos + [0, 1], pos + [-1, 1]]
        elif next_tile == 'F':
            if (heading == 'l' and lefty) or (heading == 'u' and not lefty):
                #
                # O O
                # O F
                pass
            else:
                #
                # I I
                # I F
                seed_poses = [pos + [-1, 0], pos + [0, -1], pos + [-1, -1]]
        for seed_pos in map(tuple, seed_poses):
            if seed_pos not in loop_tiles:
                # seed_pos is inside the loop
                # (no chance for out of bounds indices here)
                inside_seeds.add(seed_pos)

        heading = new_headings[next_tile][heading]

    # now flood fill indices starting from inside seeds
    inside_inds = set()
    while inside_seeds:
        seed = inside_seeds.pop()
        inside_inds.add(seed)
        for delta in deltas.values():
            neighb = tuple(seed + np.array(delta))
            if neighb in loop_tiles | inside_inds:
                # hit the loop or already visited inside tile
                continue
            inside_seeds.add(neighb)
    part2 = len(inside_inds)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day10.testinp').read()
    testinp2 = open('day10.testinp2').read()
    print(day10(testinp)[0], day10(testinp2)[1])
    inp = open('day10.inp').read()
    print(*day10(inp))
