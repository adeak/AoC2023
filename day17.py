import numpy as np


def day17(inp, part2=False):
    board = np.array(list(map(list, inp.strip().splitlines()))).astype(int)

    if part2:
        min_run_length = 4
        max_run_length = 10
    else:
        min_run_length = 1
        max_run_length = 3

    reverses = {'l': 'r', 'r': 'l', 'd': 'u', 'u': 'd'}

    # try A* after multiple dumber failures
    start = (0, 0)
    end = board.shape[0] - 1, board.shape[1] - 1
    edge = (start, ())  # states are (position, turn history) pairs
    edges = {edge}
    comefrom = {}
    best_cost_to = {edge: 0}
    best_guess_cost_from = {edge: cost_heuristic(start, end)}
    while edges:
        edge = min(edges, key=lambda edge: best_guess_cost_from.get(edge, float('inf')))
        pos, history = edge
        edges.remove(edge)

        if pos == end:
            # we're done (but not quite)
            result = best_cost_to[edge]
            break

        # generate new neighbours
        next_dirs = set('rldu')

        if history:
            # can't go back
            last_dir = history[-1]
            reverse = reverses[last_dir]
            next_dirs.discard(reverse)

        if len(history) >= max_run_length and len(set(history[-max_run_length:])) == 1:
            # can't go further in that direction
            last_dir = history[-1]
            next_dirs.discard(last_dir)

        for next_dir in next_dirs:
            if not history or last_dir != next_dir:
                # might need to take a minimum number of steps at least
                num_steps = min_run_length
            else:
                num_steps = 1

            # check if we can take as many steps
            if pos[0] < num_steps and next_dir == 'u':
                continue
            if pos[0] > end[0] - num_steps and next_dir == 'd':
                continue
            if pos[1] < num_steps and next_dir == 'l':
                continue
            if pos[1] > end[1] - num_steps and next_dir == 'r':
                continue

            next_pos = pos
            next_weight = 0
            next_history = history
            for _ in range(num_steps):
                next_pos = translate(next_pos, next_dir)
                next_weight += board[next_pos]
                next_history = next_history[-9:] + (next_dir,)
            next_edge = next_pos, next_history
            tentative_best_cost_to = best_cost_to[edge] + next_weight
            if tentative_best_cost_to < best_cost_to.get(next_edge, float('inf')):
                # new best step
                comefrom[next_edge] = edge
                best_cost_to[next_edge] = tentative_best_cost_to
                best_guess_cost_from[next_edge] = tentative_best_cost_to + cost_heuristic(next_pos, end)
                edges.add(next_edge)

    return result


def cost_heuristic(pos, end):
    return end[0] - pos[0] + end[1] - pos[1]


def translate(pos, direction):
    """Step a 2-index position tuple in a given direction."""
    if direction == 'l':
        return pos[0], pos[1] - 1
    if direction == 'r':
        return pos[0], pos[1] + 1
    if direction == 'd':
        return pos[0] + 1, pos[1]
    if direction == 'u':
        return pos[0] - 1, pos[1]


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    testinp2 = open('day17.testinp2').read()
    print(day17(testinp))
    print(day17(testinp, part2=True))
    print(day17(testinp2, part2=True))
    inp = open('day17.inp').read()
    print(day17(inp), day17(inp=True))
