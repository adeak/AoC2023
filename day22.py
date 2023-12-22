from collections import defaultdict
import copy
from graphlib import TopologicalSorter
from itertools import product


def day22(inp):
    lines = inp.strip().splitlines()

    minx = miny = float('inf')
    maxx = maxy = -float('inf')
    bricks = []
    for line in lines:
        start, _, end = line.partition('~')
        start, end = (tuple(map(int, s.split(','))) for s in [start, end])
        assert start <= end
        assert start[-1] > 0
        minx = min(minx, start[0], end[0])
        miny = min(miny, start[1], end[1])
        maxx = max(maxx, start[0], end[0])
        maxy = max(maxy, start[1], end[1])

        brick = (start, end)
        bricks.append(brick)

    # gather bricks by xy for overlap info
    bricks_by_xy = defaultdict(set)
    for index, brick in enumerate(bricks):
        start, end = brick
        for x, y in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1)):
            bricks_by_xy[x, y].add(index)

    # sort bricks by falling order
    toposorter = TopologicalSorter()
    for bricks_now in bricks_by_xy.values():
        # sort by decreasing z_min -> predecessors come later
        sorted_bricks = sorted(bricks_now, key=lambda index: -bricks[index][0][-1])
        for run_start in range(len(sorted_bricks)):
            toposorter.add(*sorted_bricks[run_start:])

    # define floor height
    floor_height = dict.fromkeys(
        product(range(minx, maxx + 1), range(miny, maxy + 1)),
        0,
    )

    # for each falling brick check how much we can move them down
    fixed_bricks = {}
    for index in toposorter.static_order():
        brick = start, end = bricks[index]
        zmin = start[-1]
        room_below = min(
            zmin - floor_height[xy] - 1
            for xy in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1))
        )
        new_zmin = zmin - room_below
        new_zmax = end[-1] - room_below
        start = start[:-1] + (new_zmin,)
        end = end[:-1] + (new_zmax,)
        for xy in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1)):
            floor_height[xy] = new_zmax

        fixed_bricks[index] = (start, end)

    # part 1: find which bricks are necessary
    important_bricks = set()
    supporting_bricks = defaultdict(set)  # brick index -> supporting brick indices
    supported_bricks = defaultdict(set)  # brick index -> supported brick indices
    for index, brick in fixed_bricks.items():
        start, end = brick
        other_indices = {
            other_index
            for xy in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1))
            for other_index in bricks_by_xy[xy]
        }
        supporting_indices = supporting_bricks[index]
        for other_index in other_indices:
            other_end = fixed_bricks[other_index][1]
            if other_end[-1] == start[-1] - 1:
                supporting_indices.add(other_index)
                supported_bricks[other_index].add(index)

        if len(supporting_indices) == 1:
            # the one supporting brick is important
            important_bricks.add(next(iter(supporting_indices)))

    # plot final state
    # import pyvista as pv
    # mesh = pv.MultiBlock()
    # for index, (start, end) in fixed_bricks.items():
    #     for xyz in product(
    #         range(start[0], end[0] + 1),
    #         range(start[1], end[1] + 1),
    #         range(start[2], end[2] + 1),
    #     ):
    #         cube = pv.Cube(center=xyz)
    #         cube.cell_data['index'] = [index] * cube.n_cells
    #         mesh.append(cube)
    # mesh.plot()

    part1 = len(fixed_bricks) - len(important_bricks)

    # part 2: try to pull out one brick
    part2 = 0
    for important_brick in important_bricks:
        removed_bricks = {important_brick}
        remaining_supported_bricks = copy.deepcopy(supported_bricks)
        dependents = remaining_supported_bricks.pop(important_brick, set())
        while dependents:
            dependent = dependents.pop()
            if supporting_bricks[dependent] <= removed_bricks:
                # remove this brick as well
                removed_bricks.add(dependent)
                part2 += 1
                dependents.update(remaining_supported_bricks.pop(dependent, set()))

    return part1, part2


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(*day22(testinp))
    inp = open('day22.inp').read()
    print(*day22(inp))
