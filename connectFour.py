import sys
import random

# Constants defining the board size and empty cell symbol
ROWS = 6
COLUMNS = 7
EMPTY = 'O'

class ConnectFour:
    """
    Represents the state of a Connect Four game, including the board
    and current player. Provides methods to display the board, find legal moves,
    and apply moves to the board.
    """
    def __init__(self, board, current_player):
        """
        Initialize the Connect Four game with a given board state and player.
        """
        self.board = board  # 2D list representing the board (list of 6 rows, each with 7 columns)
        self.current_player = current_player  # 'R' (Red) or 'Y' (Yellow)

    def display(self):
        """
        Print the current state of the board to the console.
        """
        for row in self.board:
            print(''.join(row))

    def get_legal_moves(self):
        """
        Return a list of column indices (0-6) that are valid moves (i.e., not full).
        """
        legal = []
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:
                legal.append(col)
        return legal

    def apply_move(self, col):
        """
        Apply the current player's move to the board by dropping a piece in the specified column.
        Returns True if the move was applied, False if the column is full.
        """
        for row in reversed(range(ROWS)):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                return True
        return False  # Column was full


def load_board_from_file(filename):
    """
    Read the game configuration from a file.
    Format:
    Line 1: Algorithm name (e.g., UR)
    Line 2: Current player (R or Y)
    Lines 3-8: Board rows from top to bottom (7 characters per row)
    """
    with open(filename, 'r') as file:
        algorithm = file.readline().strip()
        current_player = file.readline().strip()
        board_lines = [file.readline().strip() for _ in range(ROWS)]
        board = [list(row) for row in board_lines]
    return algorithm, current_player, board


def main():
    """
    Entry point for running the Connect Four simulation.
    Accepts 3 command-line arguments:
    1. input_file: Path to the game board input file
    2. verbosity: Verbose | Brief | None (controls output)
    3. parameter: Extra parameter (not used in UR; should be 0)
    """
    if len(sys.argv) != 4:
        print("Usage: python connectFour.py <input_file> <verbosity> <parameter>")
        return

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    parameter = int(sys.argv[3])  # For UR, this should be 0

    algorithm, current_player, board = load_board_from_file(input_file)
    game = ConnectFour(board, current_player)

    if algorithm == 'UR':
        # Run a full game where both players choose moves uniformly at random
        if verbosity != "None":
            print("Starting Connect Four Game with Uniform Random strategy...")
            game.display()

        while True:
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                print("Game Over: Draw!")
                break

            selected_move = random.choice(legal_moves)
            game.apply_move(selected_move)

            if verbosity == "Verbose":
                print(f"\n{game.current_player} played column {selected_move + 1}")
                game.display()

            # Alternate player turn
            game.current_player = 'Y' if game.current_player == 'R' else 'R'

        print("FINAL Move selected:", selected_move + 1)
    else:
        print(f"Algorithm {algorithm} not implemented yet.")


if __name__ == "__main__":
    main()
