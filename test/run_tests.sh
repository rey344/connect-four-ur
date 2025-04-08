#!/bin/bash

echo "Running test1 with UR (Verbose)..."
python3 ../connectFour.py ../boards/test1.txt Verbose 0 > results/test1_ur_verbose.out

echo "Running test2 with PMCGS..."
python3 ../connectFour.py ../boards/test2.txt Verbose 100 > results/test2_pmcgs_verbose.out

echo "Running test3 with UCT (Verbose, 100 simulations)..."
python3 ../connectFour.py ../boards/test3.txt Verbose 100 > results/test3_uct_verbose.out

echo "All tests completed."
