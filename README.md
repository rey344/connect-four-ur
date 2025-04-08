# Connect Four Game AI and Tournament

This repository implements a Connect Four game with multiple AI strategies and a tournament simulation framework. It supports several algorithms to determine moves, including:

- **Uniform Random (UR) Strategy**
- **Pure Monte Carlo Game Search (PMCGS)**
- **Upper Confidence Trees (UCT)**
- **Improved UCT with Heuristic Rollouts**
- **Improved UCT with UCB Bias**

---

## Overview

The project simulates a full game of Connect Four on a standard 7×6 board. AI agents take turns playing, applying legal moves until a win, loss, or draw is reached. The project not only provides individual algorithm implementations but also includes:
- A command-line interface for game simulation.
- A tournament engine to pit different strategies against each other.
- A suite of test files and testing scripts for evaluation.

---
## Project Directory Overview

Here is a quick overview of the key directories and files in our project:

```plaintext
UR
R
0000000
0000000
0000000
0000000
0000000
0000000
```


---

## How to Run the Game

To run a single game simulation, use the following command:

```bash
python connectFour.py <input_file> <verbosity> <parameter>
```
- &lt;input_file&gt;: Path to a board configuration file (e.g., boards/test1.txt).
- &lt;verbosity&gt;: Output detail level (options: None, Brief, Verbose).
- &lt;parameter&gt;: A parameter value specific to the selected algorithm (e.g., number of simulations).

---

## How to Run the Tournament

The tournament script run_tournament.py runs a series of match-ups between different AI strategies. It simulates multiple games between each pair of agents and outputs a win matrix along with win rates.

To run the tournament, execute:
```bash
python run_tournament.py
```
---

## Running Tests

A test suite is provided in the test/ directory. For example, to run the tests for the Improved UCT UCB strategy, use:
```bash
python test/test_improved_ucb.py
```
---

## Dependencies

Python 3.x
Standard libraries such as sys, math, random, copy, subprocess, etc.

---

Enjoy experimenting with the Connect Four AI strategies and feel free to contribute improvements!

