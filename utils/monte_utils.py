import random
from connectFour import ConnectFour
def simulate_random_game(game: ConnectFour):
    """
    Simulate a game to the end using random moves.
    Returns:
        1 -> Yellow (Max) win
       -1 -> Red (Min) win
        0 -> Draw
    """
    while True:
        winner = game.check_winner()
        if winner == 'R':
            return -1
        elif winner == 'Y':
            return 1
        elif winner == 'Draw':
            return 0
        legal_moves = game.get_legal_moves()
        move = random.choice(legal_moves)
        game.apply_move(move)
        game.current_player = 'Y' if game.current_player == 'R' else 'R'


def heuristic_move(game: ConnectFour):
    """
    Heuristic move preference function for rollouts.
    Prefers center column and moves closer to center.
    """
    legal = game.get_legal_moves()
    preferred_order = [3, 2, 4, 1, 5, 0, 6]  # Center-first heuristic
    for col in preferred_order:
        if col in legal:
            return col
    return random.choice(legal)


def simulate_heuristic_game(game: ConnectFour):
    """
    Simulate a game to the end using heuristic-guided rollouts.
    Returns:
        1 -> Yellow (Max) win
       -1 -> Red (Min) win
        0 -> Draw
    """
    while True:
        winner = game.check_winner()
        if winner == 'R':
            return -1
        elif winner == 'Y':
            return 1
        elif winner == 'Draw':
            return 0
        move = heuristic_move(game)
        game.apply_move(move)
        game.current_player = 'Y' if game.current_player == 'R' else 'R'

def basic_heuristic(game, move):
    """
    Simple heuristic function for UCT bias improvement.
    Returns a value based on the move's centrality (columns 3 and 4 are best).
    """
    center_preference = [3, 2, 2, 3, 2, 2, 1]  # Weights: columns 3 and 4 are most central
    return center_preference[move] / 3.0  # Normalize to [0, 1]
