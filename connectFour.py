import sys
import random

ROWS = 6
COLUMNS = 7
EMPTY = 'O'

class ConnectFour:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player  # 'R' or 'Y'

    def display(self):
        for row in self.board:
            print(''.join(row))

    def get_legal_moves(self):
        legal = []
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:
                legal.append(col)
        return legal

    def apply_move(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                return True
        return False


def load_board_from_file(filename):
    with open(filename, 'r') as file:
        algorithm = file.readline().strip()
        current_player = file.readline().strip()
        board_lines = [file.readline().strip() for _ in range(ROWS)]
        board = [list(row) for row in board_lines]
    return algorithm, current_player, board


def main():
    if len(sys.argv) != 4:
        print("Usage: python connectFour.py <input_file> <verbosity> <parameter>")
        return

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    parameter = int(sys.argv[3])  # For UR, this should be 0

    algorithm, current_player, board = load_board_from_file(input_file)
    game = ConnectFour(board, current_player)

    if algorithm == 'UR':
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

            game.current_player = 'Y' if game.current_player == 'R' else 'R'

        print("FINAL Move selected:", selected_move + 1)
    else:
        print(f"Algorithm {algorithm} not implemented yet.")


if __name__ == "__main__":
    main()
