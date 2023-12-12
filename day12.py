from functools import cache


def day12(inp, part2=False):
    lines = inp.strip().splitlines()

    result = 0
    for line in lines:
        single_data, contiguous_data = line.split()
        contiguous_counts = tuple(map(int, contiguous_data.split(',')))
        if part2:
            single_data = '?'.join([single_data] * 5)
            contiguous_counts *= 5

        contrib = possible_configuration_count(single_data, contiguous_counts)
        result += contrib

    return result


@cache
def possible_configuration_count(single_data, contiguous_counts):
    # try starting first contiguous block from each possible configuration, recurse
    if single_data.count('#') + single_data.count('?') < sum(contiguous_counts):
        # impossible state
        return 0
    if single_data.count('#') > sum(contiguous_counts):
        # impossible state
        return 0
    if not contiguous_counts:
        # valid configuration
        return 1

    count = 0
    contig_count, *contig_rest = contiguous_counts
    max_included_index = len(single_data) - contig_count
    if '#' in single_data:
        max_included_index = min(max_included_index, single_data.index('#'))
    for index in range(max_included_index + 1):
        state = single_data[index]
        if state == '.':
            continue

        can_fit = all(c in '?#' for c in single_data[index:index + contig_count])
        if not can_fit:
            continue

        can_have_bound = index + contig_count == len(single_data) or single_data[index + contig_count] in '?.'
        if not can_have_bound:
            continue

        count += possible_configuration_count(single_data[index + contig_count + 1:], tuple(contig_rest))

    return count


if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp), day12(testinp, part2=True))
    inp = open('day12.inp').read()
    print(day12(inp), day12(inp, part2=True))
