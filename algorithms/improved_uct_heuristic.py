import sys
import os
import math
import random
import copy

# Ensure access to parent directory for module imports
sys.path.append("..")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connectFour import ConnectFour
from utils.monte_utils import simulate_heuristic_game
from utils.file_utils import load_board_from_file

class Node:
    """
    Represents a node in the UCT tree.
    Each node tracks wins (wi), simulations (ni), and its children.
    """
    def __init__(self, parent=None, move=None):
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0
        self.ni = 0

    def ucb1(self, total_simulations, exploration_const=math.sqrt(2)):
        """
        Calculate the UCB1 value used for node selection.
        """
        if self.ni == 0:
            return float('inf')
        return (self.wi / self.ni) + exploration_const * math.sqrt(math.log(total_simulations) / self.ni)

def select(node, game, player, verbosity):
    """
    Traverse the tree from the root to a leaf node using UCB1.
    """
    path = [node]
    current_node = node

    while True:
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            break

        unvisited = [move for move in legal_moves if move not in current_node.children]
        if unvisited:
            break  # Stop at an unvisited node

        if verbosity == "Verbose":
            for move, child in current_node.children.items():
                val = child.ucb1(current_node.ni)
                print(f"V{move + 1}: {val:.2f}")

        best_move = max(current_node.children, key=lambda m: current_node.children[m].ucb1(current_node.ni))
        game.apply_move(best_move)
        current_node = current_node.children[best_move]
        path.append(current_node)
        game.current_player = 'Y' if game.current_player == 'R' else 'R'

    return current_node, path

def expand(node, game):
    """
    Add a new child node to the tree based on the first unvisited legal move.
    """
    legal_moves = game.get_legal_moves()
    for move in legal_moves:
        if move not in node.children:
            new_node = Node(parent=node, move=move)
            node.children[move] = new_node
            game.apply_move(move)
            return new_node, move
    return None, None

def backpropagate(path, result):
    """
    Propagate the result of a simulation back up the tree.
    """
    for node in reversed(path):
        node.wi += result
        node.ni += 1
        result = -result  # Flip result for the opponent's perspective

def uct_search(board, current_player, verbosity="Brief", num_simulations=500):
    """
    Perform UCT search to find the best move from the current board state.
    """
    root = Node()
    move_stats = {i: Node(parent=root, move=i) for i in range(7)}
    for move in move_stats:
        root.children[move] = move_stats[move]

    for _ in range(num_simulations):
        game = ConnectFour(copy.deepcopy(board), current_player)
        selected_node, path = select(root, game, current_player, verbosity)

        if verbosity == "Verbose" and selected_node != root:
            print(f"Move selected: {selected_node.move + 1}")

        new_node, move_played = expand(selected_node, game)
        if new_node:
            if verbosity == "Verbose":
                print("NODE ADDED")

            path.append(new_node)
            game.current_player = 'Y' if game.current_player == 'R' else 'R'
            result = simulate_heuristic_game(game)

            if verbosity == "Verbose":
                print(f"TERMINAL NODE VALUE: {result}")

            backpropagate(path, result)

    if verbosity in ["Verbose", "Brief"]:
        for col in range(7):
            node = root.children.get(col)
            if node and node.ni > 0:
                val = (node.wi / node.ni) * (-1 if current_player == 'R' else 1)
                print(f"Column {col + 1}: {val:.2f}")
            else:
                print(f"Column {col + 1}: Null")

    best_move = max(
        ((col, node) for col, node in root.children.items() if node.ni > 0),
        key=lambda item: (item[1].wi / item[1].ni) * (-1 if current_player == 'R' else 1)
    )[0]

    print("FINAL Move selected:", best_move + 1)
    return best_move

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python uct.py <input_file> <verbosity> <num_simulations>")
        sys.exit(1)

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    num_simulations = int(sys.argv[3])

    algorithm, current_player, board = load_board_from_file(input_file)
    uct_search(board, current_player, verbosity, num_simulations)
