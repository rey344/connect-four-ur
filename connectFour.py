import sys
from utils.file_utils import load_board_from_file

# Constants
ROWS = 6
COLUMNS = 7
EMPTY = 'O'

class ConnectFour:
    """
    Core Connect Four game logic: board state, move rules, and win detection.
    """
    def __init__(self, board, current_player):
        self.board = board  # 6x7 matrix
        self.current_player = current_player  # 'R' or 'Y'

    def display(self):
        for row in self.board:
            print(''.join(row))

    def get_legal_moves(self):
        return [col for col in range(COLUMNS) if self.board[0][col] == EMPTY]

    def apply_move(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                return True
        return False

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # horiz, vert, diag down, diag up
        for row in reversed(range(ROWS)):
            for col in range(COLUMNS):
                player = self.board[row][col]
                if player == EMPTY:
                    continue
                for dr, dc in directions:
                    count = 0
                    r, c = row, col
                    while (0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == player):
                        count += 1
                        if count == 4:
                            return player
                        r += dr
                        c += dc
        return 'Draw' if not self.get_legal_moves() else None

def main():
    """
    Entry point for running the Connect Four simulation.
    Dispatches control to the appropriate algorithm module
    """
    if len(sys.argv) != 4:
        print("Usage: python connectFour.py <input_file> <verbosity> <parameter>")
        return

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    parameter = int(sys.argv[3])  # For UR, this should be 0

    algorithm, current_player, board = load_board_from_file(input_file)

    if algorithm == 'UR':
        from algorithms.ur import run_ur
        run_ur(board, current_player, verbosity, parameter)
    elif algorithm == 'PMCGS':
        from algorithms.pmcgs import run_pmcgs
        run_pmcgs(board, current_player, verbosity, parameter)
    elif algorithm == 'UCT':
        from algorithms.uct import uct_search
        uct_search(board, current_player, verbosity, parameter)
    elif algorithm == 'Improved_UCT_Heuristic':
        from algorithms.improved_uct_heuristic import uct_search
        uct_search(board, current_player, verbosity, parameter)
    elif algorithm == 'Improved_UCT_UCB':
        from algorithms.improved_uct_ucb import uct_search
        uct_search(board, current_player, verbosity, parameter)
    else:
        print(f"Algorithm '{algorithm}' not implemented.")

if __name__ == "__main__":
    main()
