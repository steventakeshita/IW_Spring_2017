####################################################
# Timing.py
# description: Timing.py will use both the SMT and
# dynamic algorithm solver and time them for varying 
# amounts of sets, values, and properties
#####################################################

import time

from SMTsolver import *

# list the number of sets to find, values and properties of each deck
sets_to_find = [1]
values = [5]
properties = [5]

# how many trials to run for each iteration to average
num_trials = 1


# run correctness tests
def check_if_real_set(board, possible_set, prop, val):
	# all different cards
	assert(len(possible_set) == len(set(possible_set)))

	# from the board
	for i in possible_set:
		assert(i in board)

	# all cards are either the same or all different for all properties
	for i in range(prop):
		cur_prop = []
		for j in possible_set:
			cur_prop.append(int(j[i]))
		# all distinct elements or they all collapse to one
		assert(len(cur_prop) == len(set(cur_prop)) or len(set(cur_prop)) == 1)	

# check that all the sets found contain distinct cards
def check_all_sets_distinct(sets):
	all_cards = list(itertools.chain.from_iterable(sets))
	assert(len(all_cards) == len(set(all_cards)))


# run the SMT solver on a board to find n sets and return the time it took
def runSMTsolver(randomizer, n):
	# checks CPU time... NOT real time
	start = time.clock()
	
	test = SMTsolver(randomizer.v, randomizer.p, randomizer)
	model = test.find_n_sets(n)

	finish = time.clock()

	# confirm that this is in fact a set
	# need to check whether it has been part of ANY board since we mightve had to add cards
	# can comment this test out if want to be faster
	for i in model:
		check_if_real_set(test.all_cards_on_board, i, randomizer.p, randomizer.v)

	check_all_sets_distinct(model)

	# return total time it took to find the sets
	return finish - start

# run the dynamic solver on a board to find n sets and return the time it took
def runDynamicsolver(randomizer, n):
	# checks CPU time... NOT real time
	start = time.clock()
	
	test = Dynamicsolver(randomizer.v, randomizer.p, randomizer)
	model = test.find_n_sets(n)

	finish = time.clock()

	# confirm that this is in fact a set
	# need to check whether it has been part of ANY board since we mightve had to add cards
	# can comment this test out if want to be faster
	for i in model:
		check_if_real_set(test.all_cards_on_board, i, randomizer.p, randomizer.v)

	# return total time it took to find the sets
	return finish - start

# run all the trials
def run_trials():
	for v in values:
		for p in properties:
			for n in sets_to_find:

				SMT_time = []
				Dynamic_time = []

				for _ in range(num_trials):
					cur_rand = Randomizer(v,p) 

					SMT_time.append(runSMTsolver(cur_rand, n))
					# Dynamic_time.append(runDynamicsolver(cur_rand, n)) 

				avg_SMT = sum(SMT_time)/float(num_trials)
				# avg_Dynamic = sum(Dynamic_time)/float(num_trials)

				print "Value: " + str(v) + " | Properties: " + str(p) + " | Sets found: " + str(n) + " | SMT time: " + str(avg_SMT) 
				# print "Value: " + str(v) + " | Properties: " + str(p) + " | Sets found: " + str(n) + " | SMT time: " + str(avg_SMT) + " | Dynamic time: " + str(avg_Dynamic)

run_trials()