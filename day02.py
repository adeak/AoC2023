from collections import defaultdict
import math


def day02(inp, part2=False):
    lines = inp.strip().splitlines()

    cube_limits = {'r': 12, 'g': 13, 'b': 14}

    part1 = part2 = 0
    for line in lines:
        head, tail = line.split(': ')
        index = int(head.split()[1])
        rounds = tail.split('; ')
        # part 1: use dumb bool flag to have both parts in one function (no for-else)
        valid_round = True
        # part 2: keep track of minima
        minimum_counts = defaultdict(int)
        for r in rounds:
            groups = r.split(', ')
            for count_string, color in map(str.split, groups):
                count = int(count_string)
                color_code = color[0]
                minimum_counts[color_code] = max(count, minimum_counts[color_code])
                if count > cube_limits[color_code]:
                    # invalid group
                    valid_round = False
        if valid_round:
            part1 += index
        power = math.prod(minimum_counts.values())
        part2 += power

    return part1, part2


if __name__ == "__main__":
    testinp = open('day02.testinp').read()
    print(day02(testinp))
    inp = open('day02.inp').read()
    print(day02(inp))
