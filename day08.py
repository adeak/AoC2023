from itertools import cycle
import math


def day08(inp):
    path, rest = inp.strip().split('\n\n')

    indices = [0 if c == 'L' else 1 for c in path]
    graph = {}
    for line in rest.splitlines():
        key, rest = line.split(' = ')
        value = rest[1:-1].split(', ')
        graph[key] = value

    start = 'AAA'
    end = 'ZZZ'

    current = start
    for result, index in enumerate(cycle(indices), start=1):
        current = graph[current][index]

        if current == end:
            break

    return result


def day08b(inp):
    path, rest = inp.strip().split('\n\n')

    indices = [0 if c == 'L' else 1 for c in path]
    graph = {}
    for line in rest.splitlines():
        key, rest = line.split(' = ')
        value = rest[1:-1].split(', ')
        graph[key] = value

    starts = [key for key in graph if key.endswith('A')]

    # hypothesis: each channel is periodic
    periods = [None] * len(starts)
    currents = starts
    for step, index in enumerate(cycle(indices), start=1):
        currents = [graph[current][index] for current in currents]

        # mostly for the test case:
        if all(current.endswith('Z') for current in currents):
            result = step
            break

        # otherwise wait until we have all the periods
        for period_index, current in enumerate(currents):
            if current.endswith('Z') and periods[period_index] is None:
                periods[period_index] = step
        if all(period is not None for period in periods):
            # extrapolate
            result = math.lcm(*periods)
            break

    return result


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    testinp2 = open('day08.testinp2').read()
    print(day08(testinp), day08b(testinp2))
    inp = open('day08.inp').read()
    print(day08(inp), day08b(inp))
