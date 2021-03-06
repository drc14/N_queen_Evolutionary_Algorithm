"""Evolutionary algorithm for the N Queen problem

This file uses evolutionary algorithms to solve the N Queen Problem

Arguments:
	(int) board size
	(int) random seed (optional)

Example:
	$ python3 ec.py 8 1504886928
	Iteration: 	55
	Random Seed:	1504886928
	|   |   |   | Q |   |   |   |   |
	---------------------------------
	|   | Q |   |   |   |   |   |   |
	---------------------------------
	|   |   |   |   |   |   | Q |   |
	---------------------------------
	|   |   | Q |   |   |   |   |   |
	---------------------------------
	|   |   |   |   |   | Q |   |   |
	---------------------------------
	|   |   |   |   |   |   |   | Q |
	---------------------------------
	| Q |   |   |   |   |   |   |   |
	---------------------------------
	|   |   |   |   | Q |   |   |   |
	---------------------------------

	Valid queens: 	8



The following variables can be tweaked to improve the EA:
	population_size = 10
	probability_of_mutation = 50
	max_iterations = 10000

The permutation algorithm used is that there is a random pivot point,
child 1 takes on the qualities of parent 1 from 0 to pivot point, and the
remainder is from parent 2. Vice versa for child 2. Out of the entire
population, only the two best parents produce children.

The mutation algorithm used is that a random row is selected. Inside this
row, a queen is placed in a random column, replacing the old queen in that
row. Every queen in the population has a probability_of_mutation chance
of being mutated during each iteration.

Random is seeded with time since epoch. A second command line argument can
be given to specify the the random seed
"""

from queen import Queen
import sys
import random
import signal
from time import time
from copy import deepcopy

def signal_handler(signal, frame):
	"""Handle ctrl+c by printing current best state and exiting
	"""
	print('You pressed Ctrl+C!')
	print_info()
	sys.exit(0)

def permutation(board_1, board_2, n):
	"""Create two children from two parents, taking a portion from both

	Select a random pivot point between [0, n). From 0 to pivot point
	child 1 takes the properties from parent 1. From pivot point on, child 1
	takes on parent 2. Vice versa for child two.

	Returns:
		Queen, Queen: Child 1 and child 2
	"""
	child_1 = deepcopy(board_1)
	child_2 = deepcopy(board_2)

	pivot = random.randrange(n)

	for i in range(pivot, n):
		child_1.board[i] = board_2.board[i]
		child_2.board[i] = board_1.board[i]

	child_1.update_valid_queens()
	child_2.update_valid_queens()

	return child_1, child_2

def mutation(board, n):
	"""Mutates a random queen to a random column

	Randomly select a row. Randomly move that row's queen to a column.
	"""
	point = random.randrange(n)
	board.board[point] = random.randrange(n)
	board.update_valid_queens()

def print_info():
	"""Print current state
	Print the last iteration, random seed, board state, and the number of
	valid queens.
	"""
	print("Iteration: 	" + str(current_iteration))
	print("Random Seed:	" + str(random_seed))
	population[0].print_board()
	print("Valid queens: 	" + str(population[0].valid_queens))

# Program requires an argument, the board size
if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("Takes one or two argument(s): the board size and random seed.")
	quit()

# Set board size to first argument
n = int(sys.argv[1])

# If board size is less than 4, warn user, quit.
if n < 4:
	print("Board size must be 4 or greater!")
	quit()

# Seed the random number generator with either the second argument
# or with time since epoch
random_seed = 0
if len(sys.argv) == 3:
	random_seed = int(sys.argv[2])
else:
	random_seed = int(time())

random.seed(random_seed)

##### Constants #####
population_size = 10
probability_of_mutation = 50
max_iterations = 10000
#####################

signal.signal(signal.SIGINT, signal_handler)

# Initialize population
population = []
for i in range(population_size):
	population.append(Queen(n))

# Sort so that best is at the front of the list
population.sort(reverse=True)

# Initialize current iteration at 0
current_iteration = 0

# Continue until optimal solution is found or max_iterations are completed
while population[0].valid_queens != n and current_iteration < max_iterations:
	# Increment current iteration
	current_iteration += 1

	# Create two children
	child_1, child_2 = permutation(population[0], population[1], n)
	# Add children to the population
	population.append(child_1)
	population.append(child_2)

	# Mutate each board in the population with probability_of_mutation change
	for board in population:
		random_number = random.randrange(100)
		if random_number > (100 - probability_of_mutation):
			mutation(board, n)

	# Sort population, such that best board is at the front of the list
	population.sort(reverse=True)
	# Slice population such that max population_size is maintained
	population = population[:population_size]

# Print information (iteration count, random seed,
# 	board state, # of valid queens)
print_info()


