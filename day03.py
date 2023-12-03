from collections import defaultdict
import string

import numpy as np
import scipy.ndimage as ndi


def day03(inp):
    schematic = np.array(list(map(list, inp.strip().splitlines())))
    # prettier printing
    schematic[schematic == '.'] = ' '

    digit_chars = string.digits
    filled = schematic != ' '
    digits = np.logical_or.reduce([
        schematic == digit
        for digit in digit_chars
    ])
    symbols = filled ^ digits

    # store 2d index of each maybe-gear
    maybe_gears = schematic == '*'
    maybe_gear_inds = set(zip(*maybe_gears.nonzero()))

    # part 1: dilate numbers and find ones that overlap with symbols
    labels, n_numbers = ndi.label(digits)

    part1 = 0
    gear_to_nums = defaultdict(list)
    for label in range(1, n_numbers + 1):
        num_mask = labels == label
        dilated_mask = ndi.binary_dilation(num_mask, structure=np.full((3, 3), fill_value=True))
        num_valid = (dilated_mask & symbols).any()
        if not num_valid:
            # number irrelevant both for part 1 and part 2
            continue

        # part 1
        num = int(''.join(schematic[num_mask]))
        part1 += num

        # part 2: be gear-specific
        might_have_gear = '*' in schematic[dilated_mask]
        if not might_have_gear:
            continue

        # store numbers for each maybe-gear, find ones with 2 numbers at the end
        gear_indices = [
            gear_index
            for gear_index in maybe_gear_inds
            if dilated_mask[gear_index]
        ]
        for gear_index in gear_indices:
            gear_to_nums[gear_index].append(num)

    part2 = sum(
        nums[0] * nums[1]
        for nums in gear_to_nums.values()
        if len(nums) == 2
    )

    return part1, part2


if __name__ == "__main__":
    testinp = open('day03.testinp').read()
    print(day03(testinp))
    inp = open('day03.inp').read()
    print(day03(inp))
