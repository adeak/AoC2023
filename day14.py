from itertools import count

import numpy as np


def day14(inp):
    board = np.array(list(map(list, inp.strip().splitlines())))

    load_by_cycle = [None]  # cycle index -> total load
    cycle_by_configuration = {}  # rock/wall configuration -> cycle
    for cycle in count(1):
        for direction_index in range(4):
            size = board.shape[0]
            load = 0
            tipped_board = np.full_like(board, fill_value='.')
            for j, col in enumerate(board.T):
                tipped_col = tipped_board[:, j]
                tipped_col[col == '#'] = '#'
                last_wall_index = -1  # as in: before row 0
                for interesting_index in (col != '.').nonzero()[0]:
                    if col[interesting_index] == '#':
                        last_wall_index = interesting_index
                        continue
                    # rest are all 'O'
                    for tipped_index in range(last_wall_index + 1, interesting_index + 1):
                        if tipped_col[tipped_index] == '.':
                            # at worst this will be true at index interesting_index
                            tipped_col[tipped_index] = 'O'
                            break

            if cycle == 1 and direction_index == 0:
                rock_inds = (tipped_board == 'O').nonzero()[0]
                # this is only the load on the _north_ support beam when direction_index == 0
                load += (size - rock_inds).sum()
                part1 = load

            # rotate map instead of tipping logic
            board = np.rot90(tipped_board, -1)

        # store loads keyed on configuration to identify cycle
        configuration = ''.join(board.ravel())
        if configuration in cycle_by_configuration:
            # we're also done with part 2
            cycle_start = cycle_by_configuration[configuration]
            cycle_length = cycle - cycle_start
            remainder = (1000_000_000 - cycle_start) % cycle_length
            load = load_by_cycle[cycle_start + remainder]
            part2 = load
            break

        # after 4 tippings recompute load on north support beam (last tipping is to east)
        load = (size - (board == 'O').nonzero()[0]).sum()
        load_by_cycle.append(load)
        cycle_by_configuration[configuration] = cycle
    
    return part1, part2


if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(*day14(testinp))
    inp = open('day14.inp').read()
    print(*day14(inp))
