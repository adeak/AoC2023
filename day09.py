import numpy as np


def day09(inp):
    lines = inp.strip().splitlines()

    part1 = part2 = 0
    for line in lines:
        dat = np.fromstring(line, sep=' ', dtype=int)
        heads = [dat[0]]
        tails = [dat[-1]]
        while True:
            diffs = np.diff(dat)
            heads.append(diffs[0])
            tails.append(diffs[-1])
            if np.unique(diffs).size == 1:
                # no need to go to all zeros
                break
            dat = diffs

        # part 1
        part1 += sum(tails)

        # part 2
        part2 += sum(head * (-1)**i for i, head in enumerate(heads))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(day09(testinp))
    inp = open('day09.inp').read()
    print(day09(inp))
