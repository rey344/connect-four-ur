import sys
import os
sys.path.append("..")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.monte_utils import simulate_random_game
from utils.file_utils import load_board_from_file
from connectFour import ConnectFour
import random
import copy


def run_pmcgs(board, current_player, verbosity="Brief", num_simulations=500):
    """
    Run Pure Monte Carlo Game Search from the current board.
    """
    legal_moves = [col for col in range(7) if board[0][col] == 'O']
    move_scores = {}
    simulations = {}

    for move in legal_moves:
        win_sum = 0
        count = 0
        for _ in range(num_simulations):
            game_copy = ConnectFour(copy.deepcopy(board), current_player)
            game_copy.apply_move(move)
            game_copy.current_player = 'Y' if current_player == 'R' else 'R'
            result = simulate_random_game(game_copy)

            win_sum += result
            count += 1

        avg = win_sum / count if count > 0 else 0
        move_scores[move] = avg
        simulations[move] = count

    # Print based on verbosity
    if verbosity == "Verbose" or verbosity == "Brief":
        for col in range(7):
            if col in move_scores:
                print(f"Column {col + 1}: {move_scores[col]:.2f}")
            else:
                print(f"Column {col + 1}: Null")

    # Select best move
    best_move = max(move_scores, key=move_scores.get)
    print("FINAL Move selected:", best_move + 1)
    return best_move

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python pmcgs.py <input_file> <verbosity> <num_simulations>")
        sys.exit(1)

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    num_simulations = int(sys.argv[3])

    from connectFour import load_board_from_file
    algorithm, current_player, board = load_board_from_file(input_file)
    run_pmcgs(board, current_player, verbosity, num_simulations)
