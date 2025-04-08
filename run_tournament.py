import subprocess
from collections import defaultdict
import concurrent.futures

# List of agents with (algorithm_name, parameter)
agents = [
    ("UR", 0),
    ("PMCGS", 500),
    ("PMCGS", 10000),
    ("UCT", 500),
    ("UCT", 10000),
    ("Improved_UCT_Heuristic", 500),
    ("Improved_UCT_UCB", 500)
]

# Create friendly names for output matrix
agent_names = [f"{name}({param})" for name, param in agents]

# Dictionary to store win results
results = defaultdict(lambda: defaultdict(int))

# Set number of games for each matchup
GAMES_PER_MATCHUP = 20

def play_game(player1_algo, player2_algo):
    """
    Plays a game between two algorithms.
    player1 plays as 'R', player2 plays as 'Y'.
    Returns 'R', 'Y', or 'Draw'
    """
    input_file = "boards/empty.txt"

    result = subprocess.run(
        ["python3", "connectFour.py", input_file, "None", str(player1_algo[1])],
        capture_output=True,
        text=True
    )
    out = result.stdout
    if "Final result: R wins" in out:
        return "R"
    elif "Final result: Y wins" in out:
        return "Y"
    elif "Final result: Draw" in out:
        return "Draw"
    return "Unknown"

def play_matchup(player1, player2, agent_names, i, j):
    """
    Plays GAMES_PER_MATCHUP games between two agents in parallel.
    """
    wins = {"R": 0, "Y": 0}

    def single_game(_):
        return play_game(player1, player2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results_list = list(executor.map(single_game, range(GAMES_PER_MATCHUP)))

    for result in results_list:
        if result == "R":
            results[agent_names[i]][agent_names[j]] += 1
        elif result == "Y":
            results[agent_names[j]][agent_names[i]] += 1

# Run tournament
for i, player1 in enumerate(agents):
    for j, player2 in enumerate(agents):
        if i == j:
            continue
        print(f"Running: {agent_names[i]} vs {agent_names[j]}")
        play_matchup(player1, player2, agent_names, i, j)

# Display matrix
print("\nTournament Win Matrix (out of", GAMES_PER_MATCHUP, "games):")
print("\t" + "\t".join(agent_names))
for row_name in agent_names:
    row = [row_name]
    for col_name in agent_names:
        win_count = results[row_name][col_name]
        row.append(str(win_count))
    print("\t".join(row))

# Special: Compare Improved UCT variants vs UCT(10000)
uct_10000_name = "UCT(10000)"
for improved in ["Improved_UCT_Heuristic(500)", "Improved_UCT_UCB(500)"]:
    wins = results[improved][uct_10000_name]
    print(f"{improved} vs {uct_10000_name}: {wins} wins / {GAMES_PER_MATCHUP} games ({(wins / GAMES_PER_MATCHUP) * 100:.1f}% win rate)")
