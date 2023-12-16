import numpy as np


def day16(inp):
    board = np.array(list(map(list, inp.strip().splitlines())))
    
    deltas = {'r': [0, 1], 'l': [0, -1], 'd': [1, 0], 'u': [-1, 0]}

    part2 = 0
    initial_sources = [
        (np.arange(board.shape[0]), np.zeros(board.shape[0], dtype=int), 'r'),
        (np.arange(board.shape[0]), np.full(board.shape[0], fill_value=board.shape[1] - 1), 'l'),
        (np.zeros(board.shape[1], dtype=int), np.arange(board.shape[1]), 'd'),
        (np.full(board.shape[1], fill_value=board.shape[0] - 1), np.arange(board.shape[1]), 'u'),
    ]
    for initial_is, initial_js, initial_direction in initial_sources:
        for initial_source in zip(initial_is, initial_js):
            tiles_hit = set()  # (2d index, orientation letter) pairs
            sources = {(initial_source, initial_direction)}  # follow Fresnel principle
            while sources:
                source = index, direction = sources.pop()
                tiles_hit.add(source)
                kind = board[index]

                # handle passthrough cases
                if kind == '.' or (kind == '-' and direction in 'lr') or (kind == '|' and direction in 'ud'):
                    # just continue path
                    candidates = [(np.array(index) + deltas[direction], direction)]
                elif kind == '/':
                    next_direction = {'d': 'l', 'u': 'r', 'l': 'd', 'r': 'u'}[direction]
                    candidates = [(np.array(index) + deltas[next_direction], next_direction)]
                elif kind == '\\':
                    next_direction = {'d': 'r', 'u': 'l', 'l': 'u', 'r': 'd'}[direction]
                    candidates = [(np.array(index) + deltas[next_direction], next_direction)]
                elif kind == '|':
                    # only l/r case left here
                    candidates = [
                        (np.array(index) + deltas[next_direction], next_direction)
                        for next_direction in 'ud'
                    ]
                elif kind == '-':
                    # only u/d case left here
                    candidates = [
                        (np.array(index) + deltas[next_direction], next_direction)
                        for next_direction in 'lr'
                    ]

                for next_index, next_direction in candidates:
                    if (tuple(next_index), next_direction) in tiles_hit:
                        continue
                    if (0 <= next_index).all() and (next_index < board.shape).all():
                        sources.add((tuple(next_index), next_direction))

            energization = len({tile_data[0] for tile_data in tiles_hit})
            if initial_source == (0, 0) and initial_direction == 'r':
                part1 = energization
            part2 = max(part2, energization)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    print(*day16(testinp))
    inp = open('day16.inp').read()
    print(*day16(inp))
