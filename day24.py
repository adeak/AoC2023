from fractions import Fraction
from itertools import combinations, count, product
import math


def day24(inp, test=False):
    lines = inp.strip().splitlines()

    data = []
    for line in lines:
        pos_s, _, speed_s = line.partition(' @ ')
        pos = list(map(int, pos_s.split(', ')))
        speed = list(map(int, speed_s.split(', ')))
        data.append((pos, speed))

    if test:
        bounds = (7, 27)  # inclusive
    else:
        bounds = (200000000000000, 400000000000000)

    # part 1: ignore z
    part1 = 0
    for first, second in combinations(range(len(data)), 2):
        pos_first, speed_first = data[first]
        pos_second, speed_second = data[second]
        #if speed_first[0] / speed_second[0] == speed_first[1] / speed_second[1]:
        #    # parallel or antiparallel trajectories
        #    continue
        # intersection of trajectories is unique (if exists) in 2d:
        #     pos1[0] + t1*speed1[0] == pos2[0] + t2*speed2[0]
        #     pos1[1] + t1*speed1[1] == pos2[1] + t2*speed2[1]
        #
        #     [ speed1[0]    -speed2[0] ] [ t1 ]   [ pos2[0] - pos1[0] ]
        #     |                         | |    | = |                   |
        #     [ speed1[1]    -speed2[1] ] [ t2 ]   [ pos2[1] - pos1[1] ]
        #
        # and the determinant is D = (speed1[1] speed2[0] - speed1[0] speed2[1]) which is nonzero
        # when we have non-(anti)parallel trajectories, so we can use Cramer's formula
        a1 = speed_first[0]
        a2 = speed_first[1]
        b1 = -speed_second[0]
        b2 = -speed_second[1]
        c1 = pos_second[0] - pos_first[0]
        c2 = pos_second[1] - pos_first[1]
        D = a1*b2 - b1*a2
        if D == 0:
            # parallel/antiparallel trajectories
            continue

        # t1 = (c1*b2 - b1*c2) / D
        # t2 = (a1*c2 - c1*a2) / D
        if (c1*b2 - b1*c2) / D < 0 or (a1*c2 - c1*a2) / D < 0:
            # no chance for collision in future
            continue

        assert pos_first[0]*D + (c1*b2 - b1*c2)*speed_first[0] == pos_second[0]*D + (a1*c2 - c1*a2)*speed_second[0]
        assert pos_first[1]*D + (c1*b2 - b1*c2)*speed_first[1] == pos_second[1]*D + (a1*c2 - c1*a2)*speed_second[1]

        # to avoid float issues:
        #     bounds[0] <= pos1[i] + t1 * speed1[i] <= bounds[1]
        #     bounds[0] * |D| <= |D|*pos1[i] + (c1*b2 - b1*c2) * speed1[i] * sign(D) <= |D|*bounds[1]
        #
        d = abs(D)
        sign = round(D / abs(D))
        if all(bounds[0] * d <= d*pos_first[i] + (c1*b2 - b1*c2)*speed_first[i]*sign <= d*bounds[1] for i in range(2)):
            part1 += 1

    # part 2: find straight line
    for vx, vy, vz in half_cube_generator():
        if not all([vx, vy, vz]):
            # suspect this will not be the case
            continue

        # reduce speed by integer factor, we're only looking for directions now
        fac = math.gcd(vx, vy, vz)
        if fac > 1:
            continue

        # try to check if this speed intersects all the trajectories:
        #     1. start from the first hailstone with this velocity
        #     2. shift position along first hailstone's speed (trajectory) to intersect second hailstone
        #     3. check if all the other hailstones are intersecting now
        pos1 = data[0][0]
        delta = data[0][1]  # along which to translate initial pos1
        v1 = vx, vy, vz

        pos2, v2 = data[1]

        # pos1 + q*delta + t1*v1 == pos2 + t2*v2  # 3 unknowns, 3 linear equations, as expected
        #
        # [ delta[0]   v1[0]   -v2[0] ] [  q ]   [ pos2[0] - pos1[0] ]
        # | delta[1]   v1[1]   -v2[1] | | t1 | = | pos2[1] - pos1[1] |
        # [ delta[2]   v1[2]   -v2[2] ] [ t2 ]   [ pos2[2] - pos1[2] ]

        # q = ||pos2 - pos1, v1, -v2|| / ||delta, v1, -v2||
        #
        # to avoid floats again: it's enough to check that each hailstone gives the same q
        # and v2 -> -v2 flips the sign of both determinants, leaving q unchanged (as expected)
        last_q = None
        for pos2, v2 in data[1:]:
            delta_pos = pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2]
            try:
                q = Fraction(determinant_3d(delta_pos, v1, v2), determinant_3d(delta, v1, v2))
            except ZeroDivisionError:
                # singular determinant(s), probably parallel speed with some hailstone
                break

            if last_q is None:
                last_q = q
            if q != last_q:
                # we can't win with this v1
                break
        else:
            # we've matched all hailstones

            # empirical evidence:
            assert q.denominator == 1
            q = q.numerator

            rock_speed_direction = v1
            rock_pos_reference = tuple(
                pos1[i] + delta[i] * q
                for i in range(3)
            )
            break

    # we throw the rock along rock_speed_direction from
    #     rock_pos_reference + t0 * rock_speed_direction
    #     (or rock_pos_reference + t0 * fac * rock_speed_direction)
    # so we have 2 scalar parameters: fac (speed factor) and t0 (initial position along trajectory)
    # and rock_pos_reference is the intersection point of the rock with the first hailstone
    # and we intersect the first hailstone's trajectory at pos1 + q*delta
    # so we hit the first hailstone at time q*delta[0] / data[0][1] == q
    # so we must have
    #     rock_start = rock_pos_reference - q * rock_speed
    # so that
    #     rock_pos(q) = rock_pos_reference - q * rock_speed + q * rock_speed = rock_pos_reference
    #
    # so we have
    #     rock_speed = fac * rock_speed_direction
    #     rock_start = rock_pos_reference - q * fac * rock_speed_direction
    # and unfortunately we need another intersection to pin own the speed
    #
    # we can use the last hailstone from the last loop iteration above: 
    #     rock_pos_reference + t1*v1 == pos2 + t2*v2
    # we need t1 time with reference v1 speed for collision starting from "first" intersection
    # we need t1/fac time with actual rock_speed speed for collision
    # and we hit the last hailstone at t2 time starting from rock_pos_reference
    # (watch out for omitted minus sign from -v2)
    t1 = Fraction(determinant_3d(delta, delta_pos, v2), determinant_3d(delta, v1, v2))
    t2 = Fraction(determinant_3d(delta, v1, delta_pos), determinant_3d(delta, v1, v2)) * -1
    assert t1.denominator == 1
    assert t2.denominator == 1
    t1 = t1.numerator
    t2 = t2.numerator

    # t1 * v1 = t_actual * fac * v1
    # t_actual = t1 / fac
    # and q + t_actual == t2
    # so fac = t1 / (t2 - q)
    fac, rem = divmod(t1, t2 - q)
    assert rem == 0

    rock_start = tuple(
        rock_pos_reference[i] - q * fac * rock_speed_direction[i]
        for i in range(3)
    )
    part2 = sum(rock_start)

    return part1, part2


def half_cube_generator(initial_length=1):
    """Yield vectors in the z > 0 half space."""
    for length in count(initial_length):
        # top (plane parallel to xy)
        yield from product(range(-length, length + 1), range(-length, length + 1), [length])
        # left and right (planes parallel to yz)
        yield from product([-length], range(-length, length + 1), range(1, length))
        yield from product([length], range(-length, length + 1), range(1, length))
        # back and front (planes parallel to xy)
        yield from product(range(-length + 1, length), [-length], range(1, length))
        yield from product(range(-length + 1, length), [length], range(1, length))


def determinant_3d(*columns):
    a, b, c = columns
    return (
        a[0]*b[1]*c[2] + a[1]*b[2]*c[0] + a[2]*b[0]*c[1]
        - a[0]*b[2]*c[1] - a[1]*b[0]*c[2] - a[2]*b[1]*c[0]
    )


if __name__ == "__main__":
    testinp = open('day24.testinp').read()
    print(*day24(testinp, test=True))
    inp = open('day24.inp').read()
    print(*day24(inp))
