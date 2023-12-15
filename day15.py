from collections import defaultdict


def day15(inp):
    steps = inp.strip().split(',')
    all_lenses = defaultdict(list)  # box -> [lens label, focal length] pairs

    part1 = 0
    for step in steps:
        value = 0
        for index, c in enumerate(step):
            if c in '=-':
                label = step[:index]
                # box index: label hash
                label_hash = value
            value += ord(c)
            value = (value * 17) % 256

        # part 1: full string hash
        part1 += value

        # part 2: juggle lenses
        box = label_hash
        lenses = all_lenses[box]
        if '-' in step:
            for lens_data in lenses:
                if lens_data[0] == label:
                    break
            else:
                continue
            lenses.remove(lens_data)
        else:
            focal_length = int(step.split('=')[-1])
            for lens_data in lenses:
                if lens_data[0] == label:
                    lens_data[1] = focal_length
                    break
            else:
                lenses.append([label, focal_length])

    part2 = 0
    for box, lenses in all_lenses.items():
        for slot, (_, focal_length) in enumerate(lenses, start=1):
            part2 += (box + 1) * slot * focal_length

    return part1, part2


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(*day15(testinp))
    inp = open('day15.inp').read()
    print(*day15(inp))
