import numpy as np


def day13(inp):
    blocks = inp.strip().split('\n\n')
    
    # find doubled rows/columns
    part1 = part2 = 0
    for block in blocks:
        arr = np.array(list(map(list, block.splitlines())))

        have_part1 = have_part2 = False
        for orientation, oriented_arr in enumerate([arr, arr.T.copy()]):
            # allow 1 error in two consecutive lines for part 2
            line_counts = ((oriented_arr[:-1] != oriented_arr[1:]).sum(-1) <= 1).nonzero()[0] + 1
            for line_count in line_counts:
                overlap_size = min(line_count, oriented_arr.shape[0] - line_count)
                if line_count == overlap_size:
                    # we need the whole first half
                    first_half = oriented_arr[line_count - 1 :: -1]
                else:
                    # non-negative range end works
                    first_half = oriented_arr[line_count - 1 : line_count - 1 - overlap_size : -1]
                second_half = oriented_arr[line_count : line_count + overlap_size]
                overlap_mask = first_half == second_half
                potential_score = line_count if orientation else 100 * line_count

                if overlap_mask.all():
                    # part 1 hit
                    part1 += potential_score
                    have_part1 = True

                if (~overlap_mask).sum() == 1:
                    # part 2 hit
                    part2 += potential_score
                    have_part2 = True

                if have_part1 and have_part2:
                    break
            else:
                continue
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day13.testinp').read()
    print(*day13(testinp))
    inp = open('day13.inp').read()
    print(*day13(inp))
