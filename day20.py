from collections import deque
from itertools import count
import math


def day20(inp):
    lines = inp.strip().splitlines()

    # parse data first then convert to appropriate data structures
    flipflop_labels = set()
    conjunction_labels = set()
    connections = {}
    for line in lines:
        head, tail = line.split(' -> ')
        targets = tail.split(', ')
        if head.startswith('%'):
            label = head[1:]
            flipflop_labels.add(label)
        elif head.startswith('&'):
            label = head[1:]
            conjunction_labels.add(label)
        else:
            # broadcaster
            bcast_targets = targets
            continue
        connections[label] = targets

    flipflops = {label: False for label in flipflop_labels}
    conjunctions = {label: {} for label in conjunction_labels}
    outputs = {}
    for source, targets in connections.items():
        for target in targets:
            if target in conjunctions:
                # register a connection
                conjunctions[target][source] = False
            elif target not in flipflops:
                # output channel
                outputs[target] = set()

    # prepare for part 2
    if 'rx' in outputs:
        # assume a single input connection to a single conjunction attached to output rx
        special_conjunction = next(label for label, targets in connections.items() if 'rx' in targets)
        assert special_conjunction in conjunctions
        # keep track of press when each input of the special conjuncion sends a high signal
        special_sources = set(conjunctions[special_conjunction])
        part2_periods = {}

    part1 = part2 = None
    low_pulses = high_pulses = 0
    for press in count(1):
        low_pulses += 1
        pipeline = deque(('broadcaster', target, False) for target in bcast_targets)
        while pipeline:
            source, target, signal = pipeline.popleft()
            if signal:
                high_pulses += 1
            else:
                low_pulses += 1

            # part 2 logic
            if 'rx' in outputs and target == special_conjunction and signal:
                # need to store the first high pulse for each input connection
                if source not in part2_periods:
                    part2_periods[source] = press
                if part2_periods.keys() == special_sources:
                    # we've got all covered
                    part2 = math.lcm(*part2_periods.values())
                    break

            # basic logic
            if target in flipflops:
                if signal:
                    # nothing happens
                    continue
                # flip and broadcast
                state = not flipflops[target]
                flipflops[target] = state
                output_signal = state
            elif target in conjunctions:
                conjunctions[target][source] = signal
                output_signal = not all(conjunctions[target].values())
            else:
                # output channel
                outputs[target].add(signal)
                continue
            pipeline.extend((target, other_target, output_signal) for other_target in connections[target])
        # part 1
        if press == 1000:
            part1 = low_pulses * high_pulses

        if part2 is not None or (part1 is not None and 'rx' not in outputs):
            # all done
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    testinp2 = open('day20.testinp2').read()
    print(*day20(testinp))
    print(*day20(testinp2))
    inp = open('day20.inp').read()
    print(*day20(inp))
