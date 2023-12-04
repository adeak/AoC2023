from collections import defaultdict


def day04(inp):
    cards = {}
    card_graph = {}  # id -> set of avalanching ids

    part1 = 0
    for line in inp.strip().splitlines():
        # parse
        head, tail = line.split(': ')
        card_id = int(head.split()[-1])
        winner_part, nums_part = tail.split(' | ')
        winners = set(map(int, winner_part.split()))
        nums = set(map(int, nums_part.split()))
        cards[card_id] = winners, nums

        # part 1
        winner_count = len(nums & winners)
        if winner_count:
            part1 += 2 ** (winner_count - 1)

        # for part 2
        card_graph[card_id] = set(range(card_id + 1, card_id + winner_count + 1))

    # part 2: unravel graph from leaf ends
    card_counts = dict.fromkeys(cards, 1)  # id -> recursively won card count
    while True:
        leaves = {
            card_id
            for card_id, dependencies in card_graph.items()
            if not dependencies
        }
        for leaf in leaves:
            # bump up each dependent's card count with ours
            for card_id, dependencies in card_graph.items():
                if leaf in dependencies:
                    dependencies.remove(leaf)
                    card_counts[card_id] += card_counts[leaf]
            del card_graph[leaf]

        if not card_graph:
            break

    part2 = sum(card_counts.values())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day04.testinp').read()
    print(day04(testinp))
    inp = open('day04.inp').read()
    print(day04(inp))
