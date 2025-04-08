def load_board_from_file(filename):
    """
    Load board and player from a file.
    Returns:
        algorithms (str), current_player (str), board (list of lists)
    """
    with open(filename, 'r') as file:
        algorithms = file.readline().strip()
        current_player = file.readline().strip()
        board_lines = [file.readline().strip() for _ in range(6)]
        board = [list(row) for row in board_lines]
    return algorithms, current_player, board