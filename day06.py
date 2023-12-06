import math


def day06(inp, part2=False):
    if part2:
        inp = inp.replace(' ', '')

    lines = inp.strip().splitlines()
    times, distances = (list(map(int, line.split(':')[1].strip().split())) for line in lines)

    result = 1
    for time, record in zip(times, distances):
        # n speed <-> time - n time to move
        # d = n * (time - n)
        # n*(time - n) > record
        # -n**2 + n*time - record > 0
        # n_{1,2} = (-time +- sqrt(time**2 - 4*record)) / -2
        #         = (time +- sqrt(time**2 - 4*record)) / 2
        # so we need ceil(n_1), floor(n_2) unless this is equal to the record cases
        # so go with floor(n_1 + 1), ceil(n_2 - 1)
        discriminant = (time**2 - 4*record)**0.5
        nmin, nmax = math.floor((time - discriminant) / 2 + 1), math.ceil((time + discriminant) / 2 - 1)
        result *= nmax - nmin + 1

    return result


if __name__ == "__main__":
    testinp = open('day06.testinp').read()
    print(day06(testinp), day06(testinp, part2=True))
    inp = open('day06.inp').read()
    print(day06(inp), day06(inp, part2=True))
