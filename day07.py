from collections import Counter
from itertools import count


def day07(inp, part2=False):
    lines = inp.strip().splitlines()
    hands_with_bids = [(line.split()[0], int(line.split()[1])) for line in lines]

    if part2:
        card_rank = dict(zip('AKQT98765432J'[::-1], count()))
        score = score_with_joker
    else:
        card_rank = dict(zip('AKQJT98765432'[::-1], count()))
        score = score_without_joker

    hands_bids_by_rank = sorted(
        hands_with_bids,
        key=lambda hand_with_bid: (
            score(hand_with_bid[0]),
            [card_rank[card] for card in hand_with_bid[0]]
        )
    )
    winnings = sum(rank * bid for rank, (_, bid) in enumerate(hands_bids_by_rank, start=1))

    return winnings


def score_without_joker(hand):
    """Compute the score of a hand."""
    counter = Counter(hand)

    counts = sorted(counter.values())
    if max(counter.values()) in {4, 5}:
        # 5 -> superpoker with score 6
        # 4 -> poker with score 5
        return max(counter.values()) + 1
    if counts == [2, 3]:
        # full house
        return 4
    if counts == [1, 1, 3]:
        # three of a kind
        return 3
    if counts == [1, 2, 2]:
        # two pair
        return 2
    if counts == [1, 1, 1, 2]:
        # one pair
        return 1
    return 0


def score_with_joker(hand):
    """Compute the score of a hand in joker mode."""
    if 'J' not in hand:
        return score_without_joker(hand)

    return max(score_without_joker(hand.replace('J', replacement)) for replacement in 'AKQT98765432')


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(day07(testinp), day07(testinp, part2=True))
    inp = open('day07.inp').read()
    print(day07(inp), day07(inp, part2=True))
