""" imports for console control and card managment """
from time import sleep
from os import system
from collections import defaultdict
import random

deck = [
    "A♤", "A♡", "A♢", "A♧", 
    "K♤", "K♡", "K♢", "K♧", 
    "Q♤", "Q♡", "Q♢", "Q♧", 
    "J♤", "J♡", "J♢", "J♧", 
    "T♤", "T♡", "T♢", "T♧", 
    "9♤", "9♡", "9♢", "9♧", 
    "8♤", "8♡", "8♢", "8♧", 
    "7♤", "7♡", "7♢", "7♧", 
    "6♤", "6♡", "6♢", "6♧", 
    "5♤", "5♡", "5♢", "5♧", 
    "4♤", "4♡", "4♢", "4♧", 
    "3♤", "3♡", "3♢", "3♧", 
    "2♤", "2♡", "2♢", "2♧"
]

random.shuffle(deck)
random.shuffle(deck)
random.shuffle(deck)

card_ranks = {
    "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10,"J":11, "Q":12, "K":13, "A":14
}


def check_straight_flush(hand):
    """ check for a straight flush """
    if check_flush(hand) and check_straight(hand):
        return True
    return False

def check_four_of_a_kind(hand):
    """ check for four of a kind """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value]+=1
    if sorted(value_counts.values()) == [1,4]:
        return True
    return False

def check_full_house(hand):
    """ check for full house """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value]+=1
    if sorted(value_counts.values()) == [2,3]:
        return True
    return False

def check_flush(hand):
    """ check for flush """
    suits = [i[1] for i in hand]
    if len(set(suits))==1:
        return True
    return False

def check_straight(hand):
    """ check for a straight """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value] += 1
    rank_values = [card_ranks[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range==4):
        return True
    #check straight with low Ace
    if set(values) == set(["A", "2", "3", "4", "5"]):
        return True
    return False

def check_three_of_a_kind(hand):
    """ check for three of a kind """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value]+=1
    if set(value_counts.values()) == set([3,1]):
        return True
    return False

def check_two_pair(hand):
    """ check for two pair """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value]+=1
    if sorted(value_counts.values())==[1,2,2]:
        return True
    return False

def check_one_pair(hand):
    """ check for a piar """
    values = [i[0] for i in hand]
    value_counts = defaultdict(int)
    for value in values:
        value_counts[value]+=1
    if 2 in value_counts.values():
        return True
    return False

def clear() -> None:
    """ clears consle """
    system('clear')


pot = 0
class Hand:
    """ class for player hands, includes name, cards, bank, and cards score """

    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.score = 0
        self.bank = 10
        self.called = []
        self.best = []

    def ante(self):
        """ remove ante and add to pot """
        global pot
        self.bank -= 1
        pot += 1

    def bet(self, bet: int):
        """ bet a specific amount """
        global pot
        self.bank -= bet
        pot += bet

    def deal(self, *cards):
        """ deals a card to the hand """
        for card in cards:
            self.hand.append(card)

    def call(self, community_cards: list[str]) -> int:
        """ pick the five used cards and get the hand rank """
        global card_ranks
        all_cards = self.hand + community_cards
        for index, card in enumerate(all_cards): 
            print(f"{index+1}: {card}")

        for i in range(1, 6):
            while True:
                index = int(input(f"Card #{i}: "))-1
                if all_cards[index] not in self.called:
                    break
                print('Already using that card')
            self.called.append(all_cards[index])

        self.best = list(sorted({card_ranks[n[0]] for n in self.called}))[::-1]

        checks = [
            check_one_pair,         # 2
            check_two_pair,         # 3
            check_three_of_a_kind,  # 4
            check_straight,         # 5
            check_flush,            # 6
            check_full_house,       # 7
            check_four_of_a_kind,   # 8
            check_straight_flush    # 9
        ]

        for check in checks[::-1]:
            if check(self.called):
                return checks.index(check)+2
        return 1

player1 = Hand("")
player2 = Hand("")

player1.deal(deck.pop(), deck.pop())

community = [deck.pop() for _ in range(5)]

score = player1.call(community)

print(score, player1.called, player1.best)

# sleep(1)
# while player1.bank > 0 and player2.bank > 0:
#     pot = 0
