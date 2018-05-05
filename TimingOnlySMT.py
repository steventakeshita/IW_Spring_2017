####################################################
# Timing.py
# description: Timing.py will use both the SMT and
# dynamic algorithm solver and time them for varying 
# amounts of sets, values, and properties
#####################################################

import time

from SMTsolver import *
from Dynamicsolver import *
from BruteForce import *
from pylab import savefig


import matplotlib.pyplot as plt

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


	# for i in model:
	# 	check_if_real_set(test.all_cards_on_board, i, randomizer.p, randomizer.v)

	# check_all_sets_distinct(model)



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



# run the dynamic solver on a board to find n sets and return the time it took
def runBruteForce(randomizer, n):
	# checks CPU time... NOT real time
	start = time.clock()
	
	test = BruteForce(randomizer.v, randomizer.p, randomizer)
	model = test.find_n_sets(n)

	finish = time.clock()

	# confirm that this is in fact a set
	# need to check whether it has been part of ANY board since we mightve had to add cards
	# can comment this test out if want to be faster
	for i in model:
		check_if_real_set(test.all_cards_on_board, i, randomizer.p, randomizer.v)

	# return total time it took to find the sets
	return finish - start

# reset the board so they run on the same instance
def reset_board(rand, board):
	rand.found_sets = []
	rand.board = board


# run all the trials
def run_trials_plot(values, properties, sets_to_find, num_trials, setting):
	time_smt = []
	time_dyn = []


	for v in values:


		for p in properties:



			for n in sets_to_find:

				SMT_time = []
				Dynamic_time = []

				# have to create new randomizer or else the next solver uses the same "used" board
				for _ in range(num_trials):
					rand = Randomizer(v,p) 
					board = rand.board

					SMT_time.append(runSMTsolver(rand, n))

				avg_SMT = sum(SMT_time)/float(num_trials)


				time_smt.append(avg_SMT)

				print "Value: " + str(v) + " | Properties: " + str(p) + " | Sets found: " + str(n) + " | SMT time: " + str(avg_SMT)

	
	print "NEXT TRIAL"	

	# clear the plot
	plt.gcf().clear()

	# changing value
	if setting == 1:

		plt.plot(values, time_smt, 'b-o')
		plt.ylabel('Time (Seconds)')
		plt.xlabel('Values')

		val_find = ""
		for i in values:
			val_find += str(i)
		file_name = 'VAL-v' + val_find + 'p' + str(properties[0])  + 'n' + str(sets_to_find[0])

		savefig(file_name)
		# plt.show()

	# changing property
	elif setting == 2:
		plt.plot(properties, time_smt, 'b-o')
		plt.ylabel('Time (Seconds)')
		plt.xlabel('Properties')

		prop_find = ""
		for i in properties:
			prop_find += str(i)
		file_name = 'PROP-v' + str(values[0]) + 'p' + prop_find  + 'n' + str(sets_to_find[0])

		savefig(file_name)
		# plt.show()

	# changing number of sets to find
	else:
		plt.plot(sets_to_find, time_smt, 'b-o')
		plt.ylabel('Time (Seconds)')
		plt.xlabel('Number of Sets to Find')


		num_find = ""
		for i in sets_to_find:
			num_find += str(i)
		file_name = 'SETS-v' + str(values[0]) + 'p' + str(properties[0])  + 'n' + num_find

		savefig(file_name)
		# plt.show()


# setting at 1 = value changes, 2 = properties changes, 3 = number of sets changes

def run_all():
	def change_val():
		print "BEGIN CHANGING VALUE"
		sets_to_find = [5]
		values = [3,4,5,6,7,8,9,10]
		properties = [4]
		num_trials = 5

		run_trials_plot(values, properties, sets_to_find, num_trials, 1)

		# sets_to_find = [10]
		# values = [3,4,5,6,7,8,9,10]
		# properties = [4]
		# num_trials = 5

		# run_trials_plot(values, properties, sets_to_find, num_trials, 1)

		# sets_to_find = [15]
		# values = [3,4,5,6,7,8,9,10]
		# properties = [5]
		# num_trials = 5

		# run_trials_plot(values, properties, sets_to_find, num_trials, 1)
		print "END CHANGING VALUE"

	def change_prop():
		print "BEGIN CHANGING PROP"
		# sets_to_find = [5]
		# values = [3]
		# properties = [3,4,5,6,7]
		# num_trials = 5

		# run_trials_plot(values, properties, sets_to_find, num_trials, 2)

		sets_to_find = [10]
		values = [4]
		properties = [3,4,5,6,7,8]
		num_trials = 5

		run_trials_plot(values, properties, sets_to_find, num_trials, 2)

		# sets_to_find = [15]
		# values = [5]
		# properties = [3,4,5,6]
		# num_trials = 5

		# run_trials_plot(values, properties, sets_to_find, num_trials, 2)
		print "END CHANGING PROP"

	def change_n():
		print "BEGIN CHANGING N"
		# sets_to_find = [1,2,3,4,5,6,7,8,9,10]
		# values = [3]
		# properties = [4]
		# num_trials = 5

		# run_trials_plot(values, properties, sets_to_find, num_trials, 3)

		sets_to_find = [5,10,15,20,25,30,35,40,45,50]
		values = [4]
		properties = [5]
		num_trials = 5

		run_trials_plot(values, properties, sets_to_find, num_trials, 3)

		# sets_to_find = [1,2,3,4,5,6,7,8,9,10]
		# values = [5]
		# properties = [6]
		# num_trials = 10

		# run_trials_plot(values, properties, sets_to_find, num_trials, 3)
		print "END CHANGING N"


	change_val()

	change_prop()

	change_n()

run_all()


