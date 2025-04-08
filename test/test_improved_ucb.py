import subprocess
import re
import csv
import os

def run_game(board_path, num_simulations=500):
    """
    Run a single game on the given board using Improved UCT.
    """
    args = ['python3', 'connectFour.py', board_path, 'Verbose', str(num_simulations)]
    result = subprocess.run(args, stdout=subprocess.PIPE, text=True)
    output = result.stdout.splitlines()

    move_count = 0
    terminal_values = []
    v_lines = []

    for line in output:
        if line.startswith("Move selected"):
            move_count += 1
        elif line.startswith("TERMINAL NODE VALUE:"):
            val = int(line.split(":")[1].strip())
            terminal_values.append(val)
        elif re.match(r'^V\d:', line):
            v_lines.append(line)

    result_sum = sum(terminal_values)
    result_label = "Win" if result_sum > 0 else "Loss" if result_sum < 0 else "Draw"

    if v_lines:
        last_v = v_lines[-1]
        v_values = [float(num) for num in re.findall(r"[-+]?\d*\.\d+|\d+", last_v)]
        avg_v = round(sum(v_values) / len(v_values), 3)
    else:
        avg_v = None

    return {
        "board": os.path.basename(board_path),
        "moves": move_count,
        "result": result_label,
        "avg_v": avg_v
    }

def run_batch_tests():
    """
    Run tests on all 'improved' board files and save results.
    """
    board_folder = "boards"
    board_files = [f for f in os.listdir(board_folder) if f.endswith(".txt") and "improved" in f]

    results = []

    for board_file in board_files:
        board_path = os.path.join(board_folder, board_file)
        stats = run_game(board_path)
        results.append(stats)
        print(f"{stats['board']}: {stats['moves']} moves, {stats['result']}, Avg V={stats['avg_v']}")

    with open("test/improved_ucb_results.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["board", "moves", "result", "avg_v"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    run_batch_tests()
