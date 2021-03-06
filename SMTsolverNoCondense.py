####################################################
# SMTsolver.py
# description: SMTsolver.py will take in the random
# beginning board from Randomizer.py and find
# the sets using an SMT (z3)
#####################################################

from z3 import *

from Randomizer import *
# from Testing import *

import itertools
import time

# helper function to convert from the coordinates system to the list version
def coord_to_list(row,col,prop):
	return row*prop + col

class SMTsolverNoCondense: 
	# Initialize the SMT solver with the board
	def __init__(self, values, prop, randomizer):
		# number of values
		self.v = values

		# number of properties 
		self.p = prop

		# need to create variables for all v*p spots for v cards that will be the satisfying cards
		self.K = [ Int('k%s%s' % (i+1,j+1)) for i in range(self.v) for j in  range(self.p)]

		# store instance of randomizer to find new cards
		self.rand = randomizer

		# how many sets to add to the board after removing cards
		self.sets_to_add = 0

		# assign to variables since you only have to create these constraints one time for each run
		self.satisfying = self.create_satisfying_constraint()
		self.all_diff = self.create_all_diff_constraint()

		# create the inital SMT with all the starting constraints
		self.create_SMT()


		# collects all the cards that we ever on the board
		# potentially make this only happen if we are in testing such that it reduces the amount of stuff
		# in memory and is faster
		self.all_cards_on_board = set(self.rand.board)

	# create the original SMT with all the correct constraints
	def create_SMT(self):
		# generic solver that will find sets to remove and need to reset it everytime new constraints are added
		self.s = Solver()

		# create constraints
		self.s.add(self.satisfying)
		self.s.add(self.all_diff)

		self.create_from_board_constraint()


	# All cards in the satisfying set for all properties
	# have either the same value or all differing values
	def create_satisfying_constraint(self):
		tot_constraint = []
		# for every property
		for i in range(self.p):
			# all the same value
			all_same = [And([self.K[coord_to_list(m,i,self.p)] == self.K[coord_to_list(m+1,i,self.p)] for m in range(self.v-1)])]
			
			# or all different
			all_different = []
			for m in range(self.v-1):
				all_different+=[self.K[coord_to_list(m,i,self.p)] != self.K[coord_to_list(j,i,self.p)] for j in range(m+1,self.v)]
			all_different = [And(all_different)]

			# combine them all 
			tot_constraint.append(Or(all_same + all_different))

		return And(tot_constraint)

	# all cards selected for the set must be from the board
	def create_from_board_constraint(self):
		# for every card in the satisfying set
		every_card = []
		for i in range(self.v):
			in_board = []
			# for every card in the board
			for j in range(len(self.rand.board)):
				# traverse each property
				# card must match card from board in all properties
				prop = And([self.K[coord_to_list(i,m,self.p)] == self.rand.board[j][m] for m in range(self.p)])
				in_board.append(prop)

			every_card.append(Or(in_board))
				
		# add all the constraints
		self.s.add(And(every_card))

	# all cards selected must be distinct
	def create_all_diff_constraint(self):

		# for every card in the satisfying set
		every_card = []
		for i in range(self.v-1):
			in_board = []
			# for every card in the board
			for j in range(i+1, self.v):
				# traverse each property
				prop = Or([self.K[coord_to_list(i,m,self.p)] != self.K[coord_to_list(j,m,self.p)] for m in range(self.p)])
				in_board.append(prop)

			every_card.append(And(in_board))

		# add all the constraints
		return And(every_card)


	# update constraint when remove cards
	def update_constraint(self, set_to_remove):

		# for every card in the satisfying set
		every_card = []
		for i in range(self.v):
			in_board = []
			# for every card in the board
			for j in range(self.v):
				# traverse each property
				# card must not be one of the cards in set_to_remove
				prop = Or([self.K[coord_to_list(i,m,self.p)] != set_to_remove[j][m] for m in range(self.p)])
				in_board.append(prop)

			every_card.append(And(in_board))

		# add all the constraints
		self.s.add(And(every_card))


	# Given a board from the randomizer find a set within the board
	def find_set(self):
		# satsified means there exists a set of satisfying assignments
		if (self.s.check() == sat):

			# remove a set, so must add another one when it is time to add new cards
			self.sets_to_add+=1
			
			cards_to_remove = self.s.model()
			model_set = create_model_set(self.v, self.p, self.K, cards_to_remove)
			# removing from the board
			self.remove_set_from_board(model_set)

			# update constraints
			self.update_constraint(model_set)

			return model_set

		# if no set exists add new cards
		else:
			# draw v cards because no sets exist in the board
			if self.sets_to_add == 0:
				self.sets_to_add = 1

			# add back sets_to_add many sets to the board if there existed many sets on the board
			for _ in range(self.sets_to_add):
				if (not self.rand.draw_new_cards()):
					print "Not enough cards left in the deck, though this should never occur"
					return None

			self.all_cards_on_board.update(self.rand.board)

			# reset sets to add
			self.sets_to_add = 0

			# reupdate all constraints for SMT
			self.create_SMT()

			# retry to find another set
			return self.find_set()



	# Remove an arbitrary set and update constraints
	def remove_set_from_board(self, remove_set):
		# model_set = []
		# for i in range(self.v):
		# 	card = ""
		# 	for j in range(self.p):
		# 		var = self.K[i*self.p + j]
		# 		card += str(remove_set[var])
		# 	model_set.append(card)

		self.rand.remove_cards(remove_set)

	# Continue until n sets have been found... (will remove the sets from the board too)
	def find_n_sets(self, n):
		# find n sets
		sets = []

		for _ in range(n):
			sets.append(self.find_set())

		return sets



# Testing code to import


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


# returns the card in the same format as the desk from the SMT format
def create_model_set(val, prop, K, model):
	model_set = []
	for i in range(val):
		card = ""
		for j in range(prop):
			var = K[i*prop + j]
			card += str(model[var])
		model_set.append(card)
	return model_set


# extract the cards from the model built by the SMT and return the set of cards
# if should_print is true then it will print out all the cards nicely
def extract_cards(val, prop, K, model, should_print):
	for i in range(len(model)):
		if should_print:
			print "Card " + str(i+1) + ": " + model[i]
	return

# Check to make sure that the set was removed from the board
def check_if_removed(board, model_set):
	for i in model_set:
		assert(i not in board)


#### TESTING

# avg = []

# for _ in range(5):
# 	# 3 values 4 properties test and remove 10 sets
# 	remove2 = Randomizer(3,4) 

# 	start = time.clock()

# 	test = SMTsolver(remove2.v, remove2.p, remove2)
# 	model = test.find_n_sets(10)

# 	finish = time.clock()


# 	avg.append(finish-start)

# print(sum(avg)/5)


# avg = []

# for _ in range(5):
# 	# 3 values 4 properties test and remove 10 sets
# 	remove2 = Randomizer(4,5) 

# 	start = time.clock()

# 	test = SMTsolver(remove2.v, remove2.p, remove2)
# 	model = test.find_n_sets(10)

# 	finish = time.clock()


# 	avg.append(finish-start)

# print(sum(avg)/5)



# avg = []

# for _ in range(5):
# 	# 3 values 4 properties test and remove 10 sets
# 	remove2 = Randomizer(5,4) 

# 	start = time.clock()

# 	test = SMTsolver(remove2.v, remove2.p, remove2)
# 	model = test.find_n_sets(10)

# 	finish = time.clock()


# 	avg.append(finish-start)

# print(sum(avg)/5)








# run tests
def run_test():


# Checking basic find_set function

# True for extract_cards means to print out the cards

	# basic starting board where the board will contain ALL the cards and therefore must contain a set 
	basic1 = Randomizer(2,2)
	test = SMTsolverNoCondense(basic1.v, basic1.p, basic1)
	original_board = test.all_cards_on_board
	model = test.find_set()
	extract_cards(basic1.v, basic1.p, test.K, model, False)
	check_if_real_set(original_board, model, basic1.p, basic1.v)

	# 2 values 3 properties
	basic2 = Randomizer(2,3)
	test = SMTsolverNoCondense(basic2.v, basic2.p, basic2)
	original_board = test.all_cards_on_board
	model = test.find_set()
	extract_cards(basic2.v, basic2.p, test.K, model, False)
	check_if_real_set(original_board, model, basic2.p, basic2.v)

	# actual game of set
	basic3 = Randomizer(3,4)
	test = SMTsolverNoCondense(basic3.v, basic3.p, basic3)
	original_board = test.all_cards_on_board
	model = test.find_set()
 	extract_cards(basic3.v, basic3.p, test.K, model, False)
	check_if_real_set(original_board, model, basic3.p, basic3.v)


# Checking remove card functionality

	# 2 values 3 properties test if remove_card_works
	remove1 = Randomizer(2,3)
	test = SMTsolverNoCondense(remove1.v, remove1.p, remove1)
	original_board = test.all_cards_on_board
	model = test.find_set()
	extract_cards(remove1.v, remove1.p, test.K, model, False)
	# check if the set found was part of the old board and is a set
	check_if_real_set(original_board, model, remove1.p, remove1.v)

	# check that the set is not longer in the new board
	check_if_removed(remove1.board, model)

	# 3 values 4 properties test if remove_card_works
	remove2 = Randomizer(3,4)
	test = SMTsolverNoCondense(remove2.v, remove2.p, remove2)
	original_board = test.all_cards_on_board
	model = test.find_set()
	extract_cards(remove2.v, remove2.p, test.K, model, False)
	# check if the set found was part of the old board and is a set
	check_if_real_set(original_board, model, remove2.p, remove2.v)

	# check that the set is not longer in the new board
	check_if_removed(remove2.board, model)


# Checking that it can remove multiple sets

	# 3 values 4 properties test and remove 2 sets
	remove2 = Randomizer(3,4) 
	test = SMTsolverNoCondense(remove2.v, remove2.p, remove2)
	model = test.find_n_sets(2)

	check_all_sets_distinct(model)
	for i in model:
		extract_cards(remove2.v, remove2.p, test.K, i, False)

	original_board = test.all_cards_on_board
# need to check whether it has been part of ANY board since we mightve had to add cards
	for i in model:
		check_if_real_set(original_board, i, remove2.p, remove2.v)

	# check that the set is not longer in the new board
	for i in model:
		check_if_removed(remove2.board, i)




	# 3 values 4 properties test and remove 10 sets
	remove2 = Randomizer(4,5) 

	test = SMTsolverNoCondense(remove2.v, remove2.p, remove2)
	model = test.find_n_sets(10)

	check_all_sets_distinct(model)
	for i in model:
		extract_cards(remove2.v, remove2.p, test.K, i, False)

	original_board = test.all_cards_on_board
# need to check whether it has been part of ANY board since we mightve had to add cards
	for i in model:
		check_if_real_set(original_board, i, remove2.p, remove2.v)

	# check that the set is not longer in the new board
	for i in model:
		check_if_removed(remove2.board, i)

	print "all tests complete!"
# RUN TESTING 
# run_test()