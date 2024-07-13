"""
RdeepBot - This bot looks ahead by following a random path down the game tree. That is,
 it assumes that all players have the same strategy as rand.py, and samples N random
 games following from a given move. It then ranks the moves by averaging the heuristics
 of the resulting states.
"""

# Import the API objects
from api import State, util, Deck
import os, sys, pickle

fp = []

class Bot:

    __possible_cards = None
    __permutation_table = None

    def __init__(self):
        self.__possible_cards = range(0,20)
        self.__permutation_table = []
        cards = self.__possible_cards
        global index
        index = -2
        end = len(cards)

        for i in range(cards[0], end - 4):
            for j in range(i + 1, end - 3):
                for k in range(j + 1, end - 2):
                    for x in range(k + 1, end - 1):
                        for y in range(x + 1, end):
                            self.__permutation_table.append((i,j,k,x,y))

        global fp
        fp = self.fin(self.__permutation_table)

    def get_move(self, state):


        self.__permutation_table = self.fout(fp)

        #print("META:", self.__possible_cards,len(self.__permutation_table), self.__permutation_table[0])

        trump_index = state.get_trump_index()
        moves = state.moves()
        best_move = moves[0]

        self.remove_from_table(trump_index)
        #print("REMOVED TRUMP:", trump_index, "NEW SIZE:", len(self.__permutation_table))
        for i, j in moves:
            if i != None and j == None:
                self.remove_from_table(i)
                #print("REMOVED MY CARDS:", i , "NEW SIZE:", len(self.__permutation_table))

        self.__permutation_table = self.__permutation_table
        if state.get_opponents_played_card() is None:
            pass
        else:
            opponent = state.get_opponents_played_card()
            self.remove_from_table(opponent)
            #print("REMOVED OPPONENTS CARD:", opponent, "NEW SIZE:", len(self.__permutation_table))

        hand = self.predict_hand()
        print("PREDICTION" , util.get_rank(hand[0]) + util.get_suit(hand[0]),
                            util.get_rank(hand[1]) + util.get_suit(hand[1]),
                            util.get_rank(hand[2]) + util.get_suit(hand[2]),
                            util.get_rank(hand[3]) + util.get_suit(hand[3]),
                            util.get_rank(hand[4]) + util.get_suit(hand[4]))

        global fp
        fp = self.fin(self.__permutation_table)

        return best_move # Return the best scoring move

    def predict_hand(self):

        probability_matrix = []
        cards = self.__possible_cards
        for card in cards:
            counter = 0
            for perm in self.__permutation_table:
                for card_index in perm:
                    if card_index == card:
                        counter += 1
                        break
            probability_matrix.append(float(counter) / len(self.__permutation_table))

        probability_matrix, cards = zip(*sorted(zip(probability_matrix, cards)))
        end = len(cards) - 1
        p = cards
        #print("LIST:" , zip(probability_matrix,p))

        return (cards[end], cards[end - 1], cards[end - 2], cards[end - 3], cards[end - 4])

    def remove_from_table(self, played_card):

        try:
            self.__possible_cards.remove(played_card)

            for permutation in self.__permutation_table:
                for card in permutation:
                    if card == played_card:
                        self.__permutation_table.remove(permutation)
                        break
        except:
            #print("Could not remove",played_card)

        return

    def fin(self,content):

        with open('outfile', 'wb') as fp:
            pickle.dump(content, fp)

        return fp

    def fout(self,fp):

        with open ('outfile', 'rb') as fp:
            itemlist = pickle.load(fp)

        return itemlist
