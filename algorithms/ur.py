import sys
import random
import copy
from connectFour import ConnectFour
from utils.file_utils import load_board_from_file

def run_ur(board, current_player, verbosity="Brief", parameter=0):
    """
    Run a full game using Uniform Random strategy for both players.
    """
    game = ConnectFour(copy.deepcopy(board), current_player)

    if verbosity != "None":
        print("Starting Connect Four game with Uniform Random strategy...")
        game.display()
    
    move_count = 0
    result = None

    while True:
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            result = "Draw"
            break

        selected_move = random.choice(legal_moves)
        game.apply_move(selected_move)
        move_count += 1

        if game.check_winner() in ['R', 'Y']:
            result = f"{game.check_winner()} wins"
            break

        if verbosity == "Verbose":
            print(f"\n{game.current_player} played column {selected_move + 1}")
            game.display()
        
        game.current_player = 'Y' if game.current_player == 'R' else 'R'

    print("FINAL Move selected:", selected_move + 1)
    print(f"Total moves played: {move_count}")
    print(f"Final result: {result}")
    return selected_move

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ur.py <input_file> <verbosity> <parameter>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    parameter = int(sys.argv[3])

    algorithm, current_player, board = load_board_from_file(input_file)
    run_ur(board, current_player, verbosity, parameter)

