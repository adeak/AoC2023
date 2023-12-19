from collections import defaultdict
import json
import math


def day19(inp):
    workflows_block, ratings_block = inp.strip().split('\n\n')

    parts = [
        json.loads(rating.replace('x=', '"x":').replace('m=', '"m":').replace('a=', '"a":').replace('s=', '"s":'))
        for rating in ratings_block.splitlines()
    ]

    workflows_part1 = {}
    workflows_part2 = {}
    for workflow_str in workflows_block.splitlines():
        label, _, code = workflow_str[:-1].partition('{')
        steps = code.split(',')
        def workflow_part1(part, steps=steps):
            """Take a specific part and return output label.

            Parameters
            ----------
            part : dict
                Dict with keys in 'xmas' and integer values.

            Returns
            -------
            str
                The label (or verdict) as the output of this workflow.
            """
            for step in steps:
                if ':' not in step:
                    # 'A' or 'R'
                    return step
                condition, _, result = step.partition(':')
                if eval(f'part["{condition[0]}"]{condition[1:]}', {'part': part}):
                    return result
        workflows_part1[label] = workflow_part1

        def workflow_part2(part_ranges, steps=steps):
            """Take a part range specification and return output labels and ranges.

            Parameters
            ----------
            part_ranges : dict
                Dict with keys in 'xmas' and (from, to) integer ranges as values.

            Returns
            -------
            dict[list[dict]]
                For each output label a list of dicts like ``part_ranges`` specifying
                what falls there. (Sometimes labels, especially 'R' and 'A', repeat
                within the same workflow.)
            """
            part_ranges = part_ranges.copy()
            output = defaultdict(list)
            for step in steps:
                if ':' not in step:
                    # if we're here we need to forward what's left of part_ranges
                    output[step].append(part_ranges)
                    continue
                condition, _, result = step.partition(':')
                feature, relation = condition[:2]
                edge = int(condition[2:])
                feature_range = part_ranges[feature]
                if relation == '<':
                    if feature_range[0] >= edge:
                        # no value is inside
                        continue
                    forwarded_range = feature_range[0], min(feature_range[1], edge)
                    forwarded_part_ranges = part_ranges.copy()
                    forwarded_part_ranges[feature] = forwarded_range
                    output[result].append(forwarded_part_ranges)

                    # check if we have anything left outside to continue
                    if feature_range[1] >= edge + 1:
                        part_ranges[feature] = edge, feature_range[1]
                        continue
                    # otherwise no need to continue logic
                    break
                if relation == '>':
                    if feature_range[1] <= edge + 1:
                        # no value is inside
                        continue
                    forwarded_range = max(feature_range[0], edge + 1), feature_range[1]
                    forwarded_part_ranges = part_ranges.copy()
                    forwarded_part_ranges[feature] = forwarded_range
                    output[result].append(forwarded_part_ranges)

                    # check if we have anything left outside to continue
                    if feature_range[0] <= edge:
                        part_ranges[feature] = feature_range[0], edge + 1
                        continue
                    # otherwise no need to continue logic
                    break
            return output

        workflows_part2[label] = workflow_part2

    part1 = 0
    for part in parts:
        workflow_label = 'in'
        while True:
            workflow_label = workflows_part1[workflow_label](part)
            if workflow_label in 'RA':
                verdict = workflow_label
                break
        if verdict == 'R':
            continue
        part1 += sum(part.values())

    part2 = 0
    part_ranges_by_workflow = defaultdict(list)
    part_ranges_by_workflow['in'].append(dict.fromkeys('xmas', (1, 4001)))
    while any(lst for lst in part_ranges_by_workflow.values()):
        workflow_label, part_ranges_for_label = next(item for item in part_ranges_by_workflow.items() if item[1])
        part_ranges = part_ranges_for_label.pop()
        for next_workflow_label, new_part_ranges_lst in workflows_part2[workflow_label](part_ranges).items():
            if next_workflow_label == 'R':
                continue
            if next_workflow_label == 'A':
                part2 += sum(
                    math.prod(
                        len(range(*edges)) for edges in new_part_ranges.values()
                    )
                    for new_part_ranges in new_part_ranges_lst
                )
                continue
            part_ranges_by_workflow[next_workflow_label].extend(new_part_ranges_lst)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day19.testinp').read()
    print(*day19(testinp))
    inp = open('day19.inp').read()
    print(*day19(inp))
