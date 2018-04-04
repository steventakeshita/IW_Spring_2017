def find_all_sets(self):
        # for all possible sets in the partial sets
        sets_to_delete = []
        cards_cannot_use = []
        # might be worthwhile to go over the indices rather than i in j so that when removing you can do it directly...

        # start from the back for easier deletion 
        for ps in range(len(self.partial_sets)):



            # cur_partial_set = self.partial_sets[len(self.partial_sets)-ps-1]

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
        self.remove_set_from_board(cards_cannot_use)

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


