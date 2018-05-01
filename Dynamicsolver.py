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

        self.num_found_sets = 1

        # cards searching for
        # mapped from card that you have to the set that it completes
        self.cards_searching_for = {}


        def create_initial_combos(cards):
            # if self.v is 1 then all cards are considered a set
            if (self.v == 1):
                self.found_sets = cards
                # no more cards on the board since they are all sets
                self.rand.board = []

            # all sets are defined by two cards
            elif (self.v == 2):
                for i in itertools.combinations(cards,2):
                    self.found_sets.append(self.sort_cards(list(i)))
                # no more cards on the board since they are all sets
                self.rand.board = []

            else:
                # assign them all as partial sets
                all_combos = itertools.combinations(cards,2)
                for i in all_combos:
                    self.partial_sets.append(self.sort_cards(list(i)))

                # find all the sets
                self.find_all_sets()



        # partial sets mapped by the card that they are searching for? 
        # Upon initialization, create sets of two because we know that 
        # any two cards have the potential of being in a set
        self.partial_sets = []

        create_initial_combos(self.rand.board)

        # compare two cards in a set
    def compare(self, c1, c2):
        for i in range(len(c1)):
            if c1[i] < c2[i]: 
                return -1
            elif c1[i] > c2[i]:
                return 1
            # if its equal then keep going till you find the first different property

    # sort them to check for duplicates
    def sort_cards(self,cur_partial_set):
        return sorted(cur_partial_set, cmp = self.compare)


        # keep the threshold of cards searching for... ie, it could be mapped by one or two cards?
        # but potentiaally makes sense to only map by one considering that the reason it grows exponentially
        # is because its v^p but if we know we are going to keep v < 10 then it would make sense to only map 
        # by a couple 

    # find all cards that complete stes from partial sets
    def find_completing_cards_from_board_for_partial_set(self, cur_partial_set, sets_to_delete, cards_cannot_use):
        # determine whether for each property are we searching for the same or different value
        

        is_same_for_prop = []
        diff_value_needed = [[] for _ in range(self.p)]

        # can determine what the set is aiming for based on only two cards
        for p in range(self.p):

            # same value for this property
            p_1 = cur_partial_set[1][p]
            p_0 = cur_partial_set[0][p] 
            if (p_0 == p_1):
                is_same_for_prop.append(True)
            # or different
            else:
                # go over all cards in the partial sets and see what value we need for each property
                for i in cur_partial_set:
                    diff_value_needed[p] += [int(i[p])]

                is_same_for_prop.append(False)


        # check if a card can be appended to this combo
        for card in self.rand.board:

            # if this card is one we cannot use skip to the next card 
            if card in cards_cannot_use:
                continue

            # only potentially include it if its not one of the cards already included in the possible set
            if card not in cur_partial_set:

                failed = False
                potential_add_diff_values = [[] for _ in range(self.p)]

                # check the card to see what card we can add
                for p in range(self.p):
                    if is_same_for_prop[p]:
                        # not the same characteristic
                        if card[p] != cur_partial_set[0][p]:
                            failed = True
                            break
                    else:
                        # remember what properties we need per property
                        if int(card[p]) not in (diff_value_needed[p] + potential_add_diff_values[p]):
                            potential_add_diff_values[p]+= [int(card[p])]
                        else:
                            # there are overlapping "different" properties therefore not a card we want
                            failed = True
                            break


                # satisfies all characteristics add it to the set
                if not failed:
                    # partial sets

                    new_partial_set = cur_partial_set+[card]

                    new_partial_set = self.sort_cards(new_partial_set)

                    # added all the satisfying cards to the card
                    # if the length of the possible set is v then it is a set!
                    if len(new_partial_set) == self.v:

                        self.found_sets.append(new_partial_set)

                        # i think you have to delete the partial set... since you found the last card it should delete
                        sets_to_delete.append(cur_partial_set)

                        cards_cannot_use += new_partial_set
                    else:
                        # make sure you aren't adding duplicates!!! thereby breaking symmetry
                        if self.partial_sets.count(new_partial_set) > 1:
                            self.partial_sets.remove(new_partial_set)
                        else:
                            self.partial_sets.append(new_partial_set)


                    # combine to see what values we are missing
                    for add in range(self.p):
                        diff_value_needed[add]+= potential_add_diff_values[add]


    # figure out the last card you're missing
    def find_last_card(self, almost_finished):
        is_same_for_prop = []
        diff_value_needed = [[] for _ in range(self.p)]

        # can determine what the set is aiming for based on only two cards
        for p in range(self.p):

            # same value for this property
            p_1 = almost_finished[1][p]
            p_0 = almost_finished[0][p] 
            if (p_0 == p_1):
                is_same_for_prop.append(True)
            # or different
            else:
                # go over all cards in the partial sets and see what value we need for each property
                for i in almost_finished:
                    diff_value_needed[p] += [int(i[p])]

                is_same_for_prop.append(False)


        # determine WHAT the last card should be 
        card_missing = ""
        tot_val = sum(range(self.v))
        for p in range(self.p):
            if is_same_for_prop[p]:
                # match arbitrarily first cards pth property
                card_missing += almost_finished[0][p]
            else:
                values_have = diff_value_needed[p]
                value_missing = tot_val - sum(values_have)
                card_missing += str(value_missing)

        self.cards_searching_for[card_missing] = almost_finished


    def find_all_sets(self):
        # for all possible sets in the partial sets
        sets_to_delete = []
        cards_cannot_use = []

        for cur_partial_set in self.partial_sets:

            # be able to delete sets that we have removed the card from
            is_bad_set = False
            for i in cur_partial_set:
                if i in cards_cannot_use:
                    sets_to_delete.append(cur_partial_set)
                    is_bad_set = True
                    break

            # if this is a bad possible set immediately go to the next possible set 
            if is_bad_set:
                continue 

            self.find_completing_cards_from_board_for_partial_set(cur_partial_set, sets_to_delete, cards_cannot_use)
            
        


        for cur_partial_set in self.partial_sets:
            # missing one card... find the last card and add it to the missing card data structure
            if len(cur_partial_set) == self.v-1:
                self.find_last_card(cur_partial_set)


        for i in sets_to_delete:
            # delete partial sets 
            # delete this possible set from possible sets... 
            self.partial_sets.remove(i)


        
        self.delete_from_partial_sets(cards_cannot_use)
        self.remove_set_from_board(cards_cannot_use)


    # Remove given sets from the board
    def remove_set_from_board(self, remove_sets):
        self.rand.remove_cards(remove_sets)


    # delete these partial sets that include the cards we aren't allowed to use
    def delete_from_partial_sets(self, cards_cannot_use):
        # don't iterate if there are no cards we need to worry about
        if len(cards_cannot_use) == 0:
            return

        # BUT also make sure that any other previous set did NOT use any card from the set(s) found      
        # must check to see if any of the cards you cannot use is in partial_sets and then remove card


        sets_to_delete = []



        # potentially make it faster lol
        # delete the partial set mapping from searching for cards if one of the partial sets uses card we can't use
        for missing_card, partial in self.cards_searching_for.items():
            for card in partial:
                if card in cards_cannot_use:
                    del self.cards_searching_for[missing_card]
                    break




        # # for every partial set
        # for i in self.partial_sets:

        #     to_delete_from_partial = []

        #     for card in i:
        #         if card in cards_cannot_use:
        #             to_delete_from_partial.append(card)

        #     for j in to_delete_from_partial:
        #         i.remove(j)

        
        #     # add to queue of deleting sets
        #     if len(i) == 1 or len(i) == 0:
        #         sets_to_delete.append(i)

        # # delete the sets
        # for i in sets_to_delete:
        #     self.partial_sets.remove(i)




        # for every partial set
        for i in self.partial_sets:
            for card in i:
                if card in cards_cannot_use:
                    sets_to_delete.append(i)
                    break



                    

        # delete the sets
        for i in sets_to_delete:
            self.partial_sets.remove(i)
    

    def find_set(self):
        # if there are sets already queued as being found, immediately return
        if len(self.found_sets) != 0:
            return self.found_sets.pop() 
        else:

            # must have to draw new cards and rebuild what can be used or not... 
            self.rand.draw_new_cards()


            # last v new cards in the board are new cards
            new_cards = self.rand.board[len(self.rand.board)-self.v:]
            self.all_cards_on_board.update(new_cards)
            self.find_sets_complete_partial(new_cards)

            # once the new cards are added and appropriately chhanged check for a set
            return self.find_set()


    # quickly see if the cards just drawn satisfy any of the partial sets
    def find_sets_complete_partial(self, new_cards):
        # make sure that any new sets that are satisfied that we don't use any of the cards again
        cards_cannot_use_from_partial = []
        final_new_cards = []


        # look through all of the new cards pulled and see if it finishes any of the sets
        for i in new_cards:
            # if a card in the ones drawn is one of the cards we are searching for
            if i in self.cards_searching_for:
                # finish the set and remove it from the dictionary
                original_set = self.cards_searching_for.pop(i)

                # need to check that any potential set does not contain any card from a previously completed set
                is_used_in_another_set = False
                for j in original_set:
                    if j in cards_cannot_use_from_partial:
                        is_used_in_another_set = True
                        break

                # if we used one of the cards in the set for a different completed set try the next partial set
                if is_used_in_another_set:
                    continue            

                new_set = original_set + [i]
                
                # add it to found sets
                self.found_sets.append(new_set)


                # delete it from partial sets
                self.partial_sets.remove(original_set)

                # no longer can use any of the cards in the new set in any other sets
                cards_cannot_use_from_partial += new_set

            else:
                # if the new card is not one of them we are searching for.. create new partial sets
                final_new_cards.append(i)

        # delete partial sets that include the cards we removed
        self.delete_from_partial_sets(cards_cannot_use_from_partial)

        self.remove_set_from_board(cards_cannot_use_from_partial)

        # create new partial sets based on what cards are left
        self.create_new_partial_sets(final_new_cards)


    # create new partial sets based on the cards drawn, and the remaining cards left on the board
    def create_new_partial_sets(self, new_cards):

        # assign them all as partial sets
        if len(new_cards) == 1:
            "print possibly might not work when new_cards 1 meaning all of them used to finish the sets"
        # all_combos = itertools.combinations(new_cards,2)


        # # add all new combos...
        # for i in all_combos:
        #     self.partial_sets.append(self.sort_cards(list(i)))

        # print new_cards
        num_new = len(new_cards)
        # also add combos with existing cards
        on_board_cards = self.rand.board
        # print on_board_cards
        for c1 in new_cards:
            for c2 in on_board_cards:
                # quick fix but you should figure out the bug... :(
                if c1 != c2:
                    new_partial_set = [c1]+[c2]
                    self.partial_sets.append(self.sort_cards(new_partial_set))


        # once added new combinations check if there exists any other complete sets
        self.find_all_sets()


    # Continue until n sets have been found... (will remove the sets from the board too)
    def find_n_sets(self, n):
        # find n sets
        sets = []

        self.num_found_sets = n

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


import time


# run tests
def run_test():

    start = time.clock()


# Checking basic find_set function

# True for extract_cards means to print out the cards



    # basic starting board where the board will contain ALL the cards and therefore must contain a set 
    basic1 = Randomizer(2,2)
    test = Dynamicsolver(basic1.v, basic1.p, basic1)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic1.v, basic1.p, model, False)
    check_if_real_set(original_board, model, basic1.p, basic1.v)


    # 2 values 3 properties
    basic2 = Randomizer(2,3)
    test = Dynamicsolver(basic2.v, basic2.p, basic2)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic2.v, basic2.p, model, False)
    check_if_real_set(original_board, model, basic2.p, basic2.v)

    # actual game of set
    basic3 = Randomizer(3,4)
    test = Dynamicsolver(basic3.v, basic3.p, basic3)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(basic3.v, basic3.p, model, True)
    check_if_real_set(original_board, model, basic3.p, basic3.v)



# Checking remove card functionality

    # 2 values 3 properties test if remove_card_works
    remove1 = Randomizer(2,3)
    test = Dynamicsolver(remove1.v, remove1.p, remove1)
    original_board = test.all_cards_on_board
    model = test.find_set()
    extract_cards(remove1.v, remove1.p, model, False)
    # check if the set found was part of the old board and is a set
    check_if_real_set(original_board, model, remove1.p, remove1.v)

    # check that the set is not longer in the new board
    check_if_removed(remove1.board, model)

    # 3 values 4 properties test if remove_card_works
    remove2 = Randomizer(3,4)
    test = Dynamicsolver(remove2.v, remove2.p, remove2)
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
    test = Dynamicsolver(remove2.v, remove2.p, remove2)
    model = test.find_n_sets(2)
    
    # print test.all_cards_on_board

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
    test = Dynamicsolver(remove2.v, remove2.p, remove2)
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


    # 3 values 4 properties test and remove 10 sets
    remove2 = Randomizer(5,5) 
    test = Dynamicsolver(remove2.v, remove2.p, remove2)
    model = test.find_n_sets(1)
    for i in model:
      extract_cards(remove2.v, remove2.p, i, False)

    original_board = test.all_cards_on_board
    # need to check whether it has been part of ANY board since we mightve had to add cards
    for i in model:
      check_if_real_set(original_board, i, remove2.p, remove2.v)

    # check that the set is not longer in the new board
    for i in model:
      check_if_removed(remove2.board, i)

    print time.clock() - start

run_test()