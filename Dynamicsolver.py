####################################################
# Dynamicsolver.py
# description: Dynamicsolver.py will take in a random
# beginning board from Randomizer.py and find the sets
# using a dynamic algorithm
#####################################################

from Randomizer import *


import itertools

class Dynamicsolver: 
    # Initialize the dynamic solver with the board
    def __init__(self, values, prop, randomizer):
        # number of values
        self.v = values

        # number of properties 
        self.p = prop

        # store instance of randomizer to find new cards
        self.rand = randomizer

        # how many sets to add to the board after removing cards
        self.sets_to_add = 0

        # collects all the cards that we ever on the board
        self.all_cards_on_board = set(self.rand.board)

        
        # DYNAMIC SPECIFIC FIELDS
        # perhaps make this into an interface to clean up the code though probably not necessary

        # represent all the sets that we have found so far
        self.found_sets = []


        # cards searching for
        # mapped from card that you have to the set that it completes
        self.cards_searching_for = {}


        def create_initial_combos(cards):
            # if self.v is 1 then all cards are considered a set
            if (self.v == 1):
                self.found_sets = cards

            # all sets are defined by two cards
            elif (self.v == 2):
                for i in itertools.combinations(cards,2):
                    self.found_sets.append(list(i))

            else:
                # assign them all as partial sets
                all_combos = itertools.combinations(cards,2)
                for i in all_combos:
                    self.partial_sets.append(list(i))

                # find all the sets
                self.find_all_sets()

        # partial sets mapped by the card that they are searching for? 
        # Upon initialization, create sets of two because we know that 
        # any two cards have the potential of being in a set
        self.partial_sets = []

        create_initial_combos(self.rand.board)



        # find all sets on the given board and queue up cards to be searching for
        # self.find_all_sets()


        # cards searching for... could be a list of cards that we are searching for and if 
        # a card drawn is one of these we can quickly pull it out... assuming 

        # keep the threshold of cards searching for... ie, it could be mapped by one or two cards?
        # but potentiaally makes sense to only map by one considering that the reason it grows exponentially
        # is because its v^p but if we know we are going to keep v < 10 then it would make sense to only map 
        # by a couple 



    def find_all_sets(self):
        # for all possible sets in the partial sets
        sets_to_delete = []
        cards_cannot_use = []
        # might be worthwhile to go over the indices rather than i in j so that when removing you can do it directly...

        # start from the back for easier deletion 
        for ps in range(len(self.partial_sets)):

            # be able to delete sets that we have removed the card from
            is_bad_set = False
            for i in self.partial_sets[len(self.partial_sets)-ps-1]:
                if i in cards_cannot_use:
                    sets_to_delete+=[len(self.partial_sets)-ps-1]
                    is_bad_set = True
                    break

            # if this is a bad possible set immediately go to the next possible set 
            if is_bad_set:
                continue 

            # determine whether for each property are we searching for the same or different value
            is_same_for_prop = []
            diff_value_needed = [[] for _ in range(self.p)]

            # can determine what the set is aiming for based on only two cards
            for p in range(self.p):
                # same value for this property
                p_1 = self.partial_sets[len(self.partial_sets)-ps-1][1][p]
                p_0 = self.partial_sets[len(self.partial_sets)-ps-1][0][p] 
                if (p_0 == p_1):
                    is_same_for_prop.append(True)
                # or different
                else:
                    # go over all cards in the partial sets and see what value we need for each property
                    for i in self.partial_sets[len(self.partial_sets)-ps-1]:
                        diff_value_needed[p] += [int(i[p])]

                    is_same_for_prop.append(False)

            # check if a card can be appended to this combo
            for card in self.rand.board:

                # if this card is one we cannot use skip to the next card 
                if card in cards_cannot_use:
                    continue


                # only potentially include it if its not one of the cards already included in the possible set
                if card not in self.partial_sets[len(self.partial_sets)-ps-1]:

                    failed = False
                    for p in range(self.p):

                        if is_same_for_prop[p]:
                            # not the same characteristic
                            if card[p] != self.partial_sets[len(self.partial_sets)-ps-1][0][p]:
                                failed = True
                                break
                        else:
                            # remember what properties we need per property
                            if int(card[p]) not in diff_value_needed[p]:
                                diff_value_needed[p]+=[int(card[p])]
                            else:
                                # there are overlapping "different" properties therefore not a card we want
                                failed = True
                                break

                    # print failed
                    # satisfies all characteristics add it to the set
                    if not failed:
                        # partial sets
                        self.partial_sets[len(self.partial_sets)-ps-1].append(card)


            # added all the satisfying cards to the card
            # if the length of the possible set is v then it is a set!
            if len(self.partial_sets[len(self.partial_sets)-ps-1]) == self.v:

                self.found_sets.append(self.partial_sets[len(self.partial_sets)-ps-1])
                sets_to_delete.append(len(self.partial_sets)-ps-1)

                # alernatively just immediately delete the card from the list!
                cards_cannot_use += self.partial_sets[len(self.partial_sets)-ps-1]

            # missing one card, queue this up to the next one! 
            elif len(self.partial_sets[len(self.partial_sets)-ps-1]) == self.v-1:
                # determine WHAT the last card should be 
                card_missing = ""
                tot_val = sum(range(self.v))
                for p in range(self.p):
                    if is_same_for_prop[p]:
                        # match the arbitrarily first cards pth property
                        card_missing+= self.partial_sets[len(self.partial_sets)-ps-1][0][p]
                    else:
                        values_have = diff_value_needed[p]
                        value_missing = tot_val - sum(values_have)
                        card_missing+= str(value_missing)

                self.cards_searching_for[card_missing] = self.partial_sets[len(self.partial_sets)-ps-1]

        for i in sets_to_delete:
            # delete partial sets 
            # delete this possible set from possible sets... 
            del self.partial_sets[i]

        
        self.delete_from_partial_sets(cards_cannot_use)

        # # BUT also make sure that any other previous set did NOT use any card from the set(s) found      
        # # must check to see if any of the cards you cannot use is in partial_sets and then remove card
        # for i in self.partial_sets:
        #     for card in cards_cannot_use:
        #         for j in range(len(i)):
                    
        #             # if this partial set used a card we are not supposed to use...
        #             if card == i[len(i)-1-j]:

        #                 # if the card was missing just one card remove it from the cards searching for 
        #                 # since it is now missing 2 cards
        #                 if len(i) == v-1:
        #                   del self.cards_searching_for[i]

        #                 # delete the card from the partial set
        #                 del i[len(i)-1-j]


    # delete these partial sets that include the cards we aren't allowed to use
    def delete_from_partial_sets(self, cards_cannot_use):
        # don't iterate if there are no cards we need to worry about
        if len(cards_cannot_use) == 0:
            return

        # BUT also make sure that any other previous set did NOT use any card from the set(s) found      
        # must check to see if any of the cards you cannot use is in partial_sets and then remove card
        for i in self.partial_sets:
            for card in cards_cannot_use:
                for j in range(len(i)):
                    
                    # if this partial set used a card we are not supposed to use...
                    if card == i[len(i)-1-j]:

                        # if the card was missing just one card remove it from the cards searching for 
                        # since it is now missing 2 cards
                        if len(i) == self.v-1:
                            print self.cards_searching_for
                            for missing_card, partial in self.cards_searching_for.items():
                                print i
                                if partial == i:
                                    del self.cards_searching_for[missing_card]
                            print self.cards_searching_for

                        # delete the card from the partial set
                        del i[len(i)-1-j]




    def find_set(self):
        # if there are sets already queued as being found, immediately return
        if len(self.found_sets) != 0:
            return self.found_sets.pop()
        else:
            # must have to draw new cards and rebuild what can be used or not... 
            self.rand.draw_new_cards()

            # last v new cards in the board are new cards
            new_cards = self.rand.board[len(self.rand.board)-self.v:]
            self.find_sets_complete_partial(new_cards)

            # once the new cards are added and appropriately chhanged check for a set
            self.find_set()


    # quickly see if the cards just drawn satisfy any of the partial sets
    def find_sets_complete_partial(self, new_cards):
        # make sure that any new sets that are satisfied that we don't use any of the cards again
        cards_cannot_use = []

        # look through all of the new cards pulled and see if it finishes any of the sets
        for i in new_cards:
            # if a card in the ones drawn is one of the ones found
            if i in self.cards_searching_for:
                # finish the set
                original_set = self.cards_searching_for[i]

                # delete it from partial sets
                self.partial_sets.remove(i)

                new_set.append(i)
                self.found_sets.append(new_set)

                # no longer can use any of the cards in the new set in any other sets
                cards_cannot_use += new_set

                # delete it from one of the cards searching for 
                del self.cards_searching_for[i]

        # delete partial sets that include the cards we removed
        self.delete_from_partial_sets(cards_cannot_use)



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



    # # basic starting board where the board will contain ALL the cards and therefore must contain a set 
    # basic1 = Randomizer(2,2)
    # test = Dynamicsolver(basic1.v, basic1.p, basic1)
    # original_board = test.all_cards_on_board
    # model = test.find_set()
    # extract_cards(basic1.v, basic1.p, model, False)
    # check_if_real_set(original_board, model, basic1.p, basic1.v)


    # # 2 values 3 properties
    # basic2 = Randomizer(2,3)
    # test = Dynamicsolver(basic2.v, basic2.p, basic2)
    # original_board = test.all_cards_on_board
    # model = test.find_set()
    # extract_cards(basic2.v, basic2.p, model, False)
    # check_if_real_set(original_board, model, basic2.p, basic2.v)

    # actual game of set
    basic3 = Randomizer(3,2)
    # basic3.board = ['20', '11', '00', '01', '12', '02']
    basic3.board = ['20', '11']
    # print basic3.board
    test = Dynamicsolver(basic3.v, basic3.p, basic3)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic3.v, basic3.p, model, True)
    check_if_real_set(original_board, model, basic3.p, basic3.v)



# # Checking remove card functionality

#   # 2 values 3 properties test if remove_card_works
#   remove1 = Randomizer(2,3)
#   test = Dynamicsolver(remove1.v, remove1.p, remove1)
#   original_board = test.all_cards_on_board
#   model = test.find_set()
#   extract_cards(remove1.v, remove1.p, model, False)
#   # check if the set found was part of the old board and is a set
#   check_if_real_set(original_board, model, remove1.p, remove1.v)

#   # check that the set is not longer in the new board
#   check_if_removed(remove1.board, model)

#   # 3 values 4 properties test if remove_card_works
#   remove2 = Randomizer(3,4)
#   test = Dynamicsolver(remove2.v, remove2.p, remove2)
#   original_board = test.all_cards_on_board
#   model = test.find_set()
#   extract_cards(remove2.v, remove2.p, model, False)
#   # check if the set found was part of the old board and is a set
#   check_if_real_set(original_board, model, remove2.p, remove2.v)

#   # check that the set is not longer in the new board
#   check_if_removed(remove2.board, model)


# # Checking that it can remove multiple sets

#   # 3 values 4 properties test and remove 2 sets
#   remove2 = Randomizer(3,4) 
#   test = Dynamicsolver(remove2.v, remove2.p, remove2)
#   model = test.find_n_sets(2)
#   for i in model:
#       extract_cards(remove2.v, remove2.p, i, False)

#   original_board = test.all_cards_on_board
# # need to check whether it has been part of ANY board since we mightve had to add cards
#   for i in model:
#       check_if_real_set(original_board, i, remove2.p, remove2.v)

#   # check that the set is not longer in the new board
#   for i in model:
#       check_if_removed(remove2.board, i)

#   # 3 values 4 properties test and remove 10 sets
#   remove2 = Randomizer(3,4) 
#   test = Dynamicsolver(remove2.v, remove2.p, remove2)
#   model = test.find_n_sets(10)
#   for i in model:
#       extract_cards(remove2.v, remove2.p, i, False)

#   original_board = test.all_cards_on_board
# # need to check whether it has been part of ANY board since we mightve had to add cards
#   for i in model:
#       check_if_real_set(original_board, i, remove2.p, remove2.v)

#   # check that the set is not longer in the new board
#   for i in model:
#       check_if_removed(remove2.board, i)


run_test()