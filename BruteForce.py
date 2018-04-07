####################################################
# BruteForce.py
# description: BruteForce.py will take in a random
# beginning board from Randomizer.py and find the sets
# using the brute force method
#####################################################

from Randomizer import *

import itertools

class BruteForce: 
    # Initialize the dynamic solver with the board
    def __init__(self, values, prop, randomizer):
        # number of values
        self.v = values

        # number of properties 
        self.p = prop

        # store instance of randomizer to find new cards
        self.rand = randomizer

        # collects all the cards that we ever on the board
        # potentially make this only happen if we are in testing such that it reduces the amount of stuff
        # in memory and is faster
        self.all_cards_on_board = set(self.rand.board)

    def find_set(self):
        # find cards
        for cards in itertools.combinations(self.rand.board,self.v):
            is_set = True
            for p in range(self.p):
                cur_prop_value = []
                for card in cards:
                    cur_prop_value.append(card[p])
                if len(set(cur_prop_value)) != self.v and len(set(cur_prop_value)) != 1:
                    is_set = False
                    break
            if is_set:
                self.remove_set_from_board(list(cards))
                return list(cards)

        # draw new cards if no cards found and find another set
        self.rand.draw_new_cards()
        self.all_cards_on_board.update(self.rand.board)

        return self.find_set()

    # Remove an arbitrary set and update constraints
    def remove_set_from_board(self, remove_set):
        self.rand.remove_cards(remove_set)

    # Continue until n sets have been found... (will remove the sets from the board too)
    def find_n_sets(self, n):
        # find n sets
        sets = []

        for _ in range(n):
            sets.append(self.find_set())

        return sets


# POTENTIALLY CAN MOVE THIS OVER or just imoprt the SMTsolver and call the functions so you dont have to copy and paste!

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



# Check to make sure that the set was removed from the board
def check_if_removed(board, model_set):
    for i in model_set:
        assert(i not in board)



# extract the cards from the model built by the SMT and return the set of cards
# if should_print is true then it will print out all the cards nicely
def extract_cards(val, prop, model, should_print):
    for i in range(len(model)):
        if should_print:
            print "Card " + str(i+1) + ": " + model[i]
    return


# run tests
def run_test():


# Checking basic find_set function

# True for extract_cards means to print out the cards



    # basic starting board where the board will contain ALL the cards and therefore must contain a set 
    basic1 = Randomizer(2,2)
    test = BruteForce(basic1.v, basic1.p, basic1)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic1.v, basic1.p, model, False)
    check_if_real_set(original_board, model, basic1.p, basic1.v)


    # 2 values 3 properties
    basic2 = Randomizer(2,3)
    test = BruteForce(basic2.v, basic2.p, basic2)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic2.v, basic2.p, model, False)
    check_if_real_set(original_board, model, basic2.p, basic2.v)

    # actual game of set
    basic3 = Randomizer(3,4)
    # basic3.board = ['20', '11', '00', '01', '12', '02']
    # basic3.board = ['20', '11']
    # print basic3.board
    test = BruteForce(basic3.v, basic3.p, basic3)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic3.v, basic3.p, model, False)
    check_if_real_set(original_board, model, basic3.p, basic3.v)



    # Checking remove card functionality

    # 2 values 3 properties test if remove_card_works
    remove1 = Randomizer(2,3)
    test = BruteForce(remove1.v, remove1.p, remove1)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(remove1.v, remove1.p, model, False)
    # check if the set found was part of the old board and is a set
    check_if_real_set(original_board, model, remove1.p, remove1.v)

    # check that the set is not longer in the new board
    check_if_removed(remove1.board, model)

    # 3 values 4 properties test if remove_card_works
    remove2 = Randomizer(3,4)
    test = BruteForce(remove2.v, remove2.p, remove2)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(remove2.v, remove2.p, model, False)
    # check if the set found was part of the old board and is a set
    check_if_real_set(original_board, model, remove2.p, remove2.v)

    # check that the set is not longer in the new board
    check_if_removed(remove2.board, model)


    # Checking that it can remove multiple sets

    # 3 values 4 properties test and remove 2 sets
    remove2 = Randomizer(3,4) 
    test = BruteForce(remove2.v, remove2.p, remove2)
    model = test.find_n_sets(2)
    for i in model:
      extract_cards(remove2.v, remove2.p, i, False)

    original_board = test.all_cards_on_board
    # need to check whether it has been part of ANY board since we mightve had to add cards
    for i in model:
      check_if_real_set(original_board, i, remove2.p, remove2.v)

    # check that the set is not longer in the new board
    for i in model:
      check_if_removed(remove2.board, i)



    # 3 values 4 properties test and remove 10 sets
    remove2 = Randomizer(3,4) 
    test = BruteForce(remove2.v, remove2.p, remove2)
    model = test.find_n_sets(10)
    for i in model:
      extract_cards(remove2.v, remove2.p, i, False)

    original_board = test.all_cards_on_board
    # need to check whether it has been part of ANY board since we mightve had to add cards
    for i in model:
      check_if_real_set(original_board, i, remove2.p, remove2.v)

    # check that the set is not longer in the new board
    for i in model:
      check_if_removed(remove2.board, i)


# run_test()