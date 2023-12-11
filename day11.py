import numpy as np
from scipy.spatial.distance import pdist


def day11(inp, part2=False, part2_expansion_factor=1000_000):
    sky = np.array([list(line) for line in inp.strip().splitlines()]) == '#'

    if part2:
        expansion_factor = part2_expansion_factor
    else:
        expansion_factor = 2

    starting_positions = np.array(sky.nonzero()).T  # shape (n_galaxies, 2)
    # gather galaxy positions by row and column index
    galaxies_by_row = {
        i: [pos for pos in starting_positions if pos[0] == i]
        for i in range(sky.shape[0])
    }
    galaxies_by_col = {
        j: [pos for pos in starting_positions if pos[1] == j]
        for j in range(sky.shape[1])
    }

    # get row and column indices to expand
    expanding_rows = (~sky.any(1)).nonzero()[0]
    expanding_cols = (~sky.any(0)).nonzero()[0]

    # along both axes bump up all row/column indices that come after expanding ones
    axes = [0, 1]
    expanding_indiceses = [expanding_rows, expanding_cols]
    galaxies_by_axis = [galaxies_by_row, galaxies_by_col]
    for axis, expanding_indices, galaxies in zip(axes, expanding_indiceses, galaxies_by_axis):
        for expanding_index in expanding_indices:
            for index in range(expanding_index + 1, len(galaxies)):
                for pos in galaxies[index]:
                    pos[axis] += expansion_factor - 1

    galaxy_positions = [pos for poses in galaxies_by_row.values() for pos in poses]
    total_distance = pdist(galaxy_positions, 'cityblock').sum().astype(int)

    return total_distance


if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(day11(testinp), day11(testinp, part2=True, part2_expansion_factor=100))
    inp = open('day11.inp').read()
    print(day11(inp), day11(inp, part2=True))
