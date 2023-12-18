from collections import defaultdict


def day18(inp, part2=False):
    lines = inp.strip().splitlines()

    pos = (0, 0)
    corners = [pos]
    for line in lines:
        direction, length, other_direction = line.split()
        if part2:
            fake_hex = other_direction[1:-1]
            direction = 'RDLU'[int(fake_hex[-1])]
            length = int(fake_hex[1:-1], 16)
        else:
            length = int(length)
        pos = translate(pos, direction, length)
        corners.append(pos)

    corner_inds_by_i = defaultdict(set)
    corner_inds_by_j = defaultdict(set)
    for index, corner in enumerate(corners):
        corner_inds_by_i[corner[0]].add(index)
        corner_inds_by_j[corner[1]].add(index)

    # pad unique corner coords to avoid fencepost errors later
    grid_i = sorted(corner_inds_by_i)
    grid_i = [grid_i[0] - 1] + grid_i + [grid_i[-1] + 1]
    grid_j = sorted(corner_inds_by_j)
    grid_j = [grid_j[0] - 1] + grid_j + [grid_j[-1] + 1]
    inside_count = 0
    # loop over each block in the grid of unique corner indices, check if inside/outside
    inside_by_ends = {}
    for i_from, i_to in zip(grid_i, grid_i[1:]):
        inside = False
        i_size = i_to - i_from  # i_to is exclusive
        for j_from, j_to in zip(grid_j, grid_j[1:]):
            # check if we have a vertical edge at j_from (j_to is exclusive)
            j_size = j_to - j_from
            have_edge = False
            potential_corners = corner_inds_by_j[j_from]
            potential_edges = []
            for index in potential_corners:
                # always check _next_ corner to get each edge exactly once
                if (index + 1) % len(corners) in potential_corners:
                    potential_edges.append(sorted([corners[index], corners[(index + 1) % len(corners)]]))
            for potential_edge in potential_edges:
                from_corner, to_corner = potential_edge
                if from_corner[0] <= i_from and to_corner[0] >= i_to:
                    have_edge = True
                    break
            # if no edge at j_from containing [i_from, i_to]: inside state is unchanged
            if have_edge:
                inside = not inside
            inside_by_ends[i_to, j_to] = inside
            if inside:
                inside_count += i_size * j_size
            elif have_edge:
                # account for edge at j_from in case we just flipped
                inside_count += i_size

            # account for edge at i_to (if present and we're outside)
            if inside:
                continue
            if (i_from, j_to) not in inside_by_ends:
                # first edge of the grid, no edge to the left
                continue
            if inside_by_ends[i_from, j_to]:
                # block on the left was inside, we're outside
                # need to add left edge due to right-exclusiveness
                inside_count += j_size

    # correct magical off-by-one error
    result = inside_count + 1

    return result


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


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp), day18(testinp, part2=True))
    inp = open('day18.inp').read()
    print(day18(inp), day18(inp, part2=True))
