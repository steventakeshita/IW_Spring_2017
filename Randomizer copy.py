####################################################
# Randomizer.py
# description: Randomizer.py is an object that takes in 
# values v and properties p that will randomize a 
# deck for the Game of Set. It will create the 
# randomized board and will support the update 
# functions of adding new cards and removing cards
#####################################################


import random

# for randomization tests
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# Creates a randomization deck in which it starts with a deck and a board of size v*p
# Allows for removal of cards and drawing of new cards 
class Randomizer: 
	def __init__(self, values, prop):
		# number of value
		self.v = values
		# number of properties
		self.p = prop





		# # helper function to creates all cards in the deck
		# def create_cards(values_deck, prop_deck):
		# 	total_cards = [str(val) for val in range(values_deck)]
		# 	for p in range(prop_deck-1):
		# 		new_cards = []
		# 		for i in total_cards:
		# 			for j in range(values_deck):
		# 				new_cards.append(i + str(j))
		# 				total_cards = new_cards
		# 	return total_cards

		# # cards are represented as a string of length p with values [0,v) 
		# self.deck =  create_cards(values, prop)

		# cards currently out
		# take out values * prop cards initially... this will also get rid of the cards in the deck
		# random.sample(items, values*prop) can use but does with replacement

		# self.board = [self.deck.pop(random.randrange(len(self.deck))) for _ in xrange(values*prop)]

		self.board = self.create_n_cards(values*prop, [])

	# create a card with p properties and each property is randomized from 0 to v-1
	def create_card(self):
		card = ""
		for i in range(self.p):
			card += random.randint(0, self.v-1)
		return card

	# create n new cards that are not in the board
	def create_n_cards(self, n, board):
		count = 0
		while count < n:
			card = self.create_card()
			if card not in board:
				board.append(card)
				count+=1

	# remove given cards from the deck
	def remove_cards(self, cards_to_remove):
		indices = []
		for i in range(len(self.board)):
			if self.board[i] in cards_to_remove: 
				indices.append(i)

		for i in range(len(indices)):
			del self.board[indices[len(indices)-1-i]]



	# draws v new cards from the deck and adds it the board while removing them from the deck
	def draw_new_cards(self):
		# make sure that there are cards left to draw
		if (len(self.deck) >= self.v):
			# new_cards = [self.deck.pop(random.randrange(len(self.deck))) for _ in xrange(self.v)]
			self.board = create_n_cards()
			# self.board = self.board + new_cards
			return True
		else:
			return False




# Testing
def run_rand_initial_tests(val, prop, num_trials):
	# run trials testing to see the distribution of starting board
	rand_start = Randomizer(val, prop)
	count = Counter(rand_start.board)
	for _ in range(num_trials-1):
		rand_start = Randomizer(val, prop)
		count.update(rand_start.board)

	# graph the 1000 trials as a histogram of counts 
	labels, values = zip(*count.items())

	indexes = np.arange(len(labels))
	width = 1

	plt.bar(indexes, values, width)
	plt.ylabel('Number of Occurences')
	plt.xlabel('Card Number')
	plt.xlim([0,len(labels)])

	plt.show()
	# successful if uniform distribution
	return

def run_rand_next_card_tests(val, prop, num_trials):

	# run trials to test for distribution of next card + board
	rand_next_card = Randomizer(val, prop)
	count = Counter(rand_next_card.board)
	for _ in range(num_trials-1):
		rand_next_card = Randomizer(val, prop)
		rand_next_card.draw_new_cards()
		count.update(rand_next_card.board)

	# graph the 1000 trials as a histogram of counts 
	labels, values = zip(*count.items())

	indexes = np.arange(len(labels))
	width = 1

	plt.bar(indexes, values, width)
	plt.ylabel('Number of Occurences')
	plt.xlabel('Card Number')
	plt.xlim([0,len(labels)])

	plt.show()
	# successful if uniform distribution
	return	

# 10,000 trials for random beginning board
# run_rand_initial_tests(4,5,10000)

# run_rand_next_card_tests(3,4,1000)