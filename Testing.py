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
