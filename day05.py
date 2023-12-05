def day05(inp, part2=False):
    blocks = inp.strip().split('\n\n')

    seed_line, blocks = blocks[0], blocks[1:]
    seeds = list(map(int, seed_line.strip().split(': ')[1].split()))

    if part2:
        # seeds are actually [pos, length] pairs
        raw_ranges = list(zip(*[iter(seeds)]*2))
    else:
        # length 1 ranges
        raw_ranges = [(seed, 1) for seed in seeds]
    ranges = {(start, start + length - 1) for start, length in raw_ranges}
    # (all ranges are inclusive)

    for i, block in enumerate(blocks):
        lines = block.splitlines()[1:]
        # converted_new_ranges gathers ranges _inside_ known map ranges
        # raw_new_ranges gathers work-in-progress split lines that might be split later
        converted_new_ranges = set()
        for line in lines:
            dest_start, source_start, length = map(int, line.split())
            source_end = source_start + length - 1
            offset = dest_start - source_start  # dest = source + offset

            raw_new_ranges = set()
            to_check = ranges
            while to_check:
                range_start, range_end = rng = to_check.pop()
                if range_end < source_start or range_start > source_end:
                    # no overlap with this range
                    raw_new_ranges.add(rng)
                    continue
                # else split up and convert range
                if range_start < source_start:
                    outside_range = range_start, min(range_end, source_start - 1)
                    raw_new_ranges.add(outside_range)
                if range_end > source_end:
                    outside_range = max(source_end + 1, range_start), range_end
                    raw_new_ranges.add(outside_range)
                inside_range = max(source_start, range_start), min(source_end, range_end)
                inside_range = inside_range[0] + offset, inside_range[1] + offset
                # don't let other map lines in this block handle this post-transform
                converted_new_ranges.add(inside_range)
            ranges = raw_new_ranges
        # add up already converted (transformed) ranges for next block
        ranges.update(converted_new_ranges)

    return min(rng[0] for rng in ranges)


if __name__ == "__main__":
    testinp = open('day05.testinp').read()
    print(day05(testinp), day05(testinp, part2=True))
    inp = open('day05.inp').read()
    print(day05(inp), day05(inp, part2=True))
