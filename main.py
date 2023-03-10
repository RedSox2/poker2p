""" imports for console control and card managment """
from time import sleep
from os import system, name
from collections import defaultdict
import random

deck = [
    'A♤', 'A♡', 'A♢', 'A♧', 
    'K♤', 'K♡', 'K♢', 'K♧', 
    'Q♤', 'Q♡', 'Q♢', 'Q♧', 
    'J♤', 'J♡', 'J♢', 'J♧', 
    'T♤', 'T♡', 'T♢', 'T♧', 
    '9♤', '9♡', '9♢', '9♧', 
    '8♤', '8♡', '8♢', '8♧', 
    '7♤', '7♡', '7♢', '7♧', 
    '6♤', '6♡', '6♢', '6♧', 
    '5♤', '5♡', '5♢', '5♧', 
    '4♤', '4♡', '4♢', '4♧', 
    '3♤', '3♡', '3♢', '3♧', 
    '2♤', '2♡', '2♢', '2♧'
]

deck_save = deck.copy()

score_key = {
    0: 'folded',
    1: 'a high card',
    2: 'one pair', 
    3: 'two pair', 
    4: 'three of a kind', 
    5: 'a straight', 
    6: 'a flush', 
    7: 'a full house', 
    8: 'four of a kind', 
    9: 'a straight flush'
} 

card_ranks = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
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
    # check straight with low Ace
    if set(values) == set(['A', '2', '3', '4', '5']):
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
    system('cls' if name == 'nt' else 'clear')
def wait():
    """ wait for enter """
    input('Press ENTER to continue . . .')
    clear()

pot = None
class Player:
    """ class for player hands, includes name, cards, chips, and cards score """

    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.score = 0
        self.chips = 10
        self.betting = 0
        self.last = 0
        self.called = ['fold']
        self.best = []
        self.folded = False

    def reset(self):
        self.hand.clear()
        self.score = 0
        self.betting = 0
        self.last = 0
        self.called = ['fold']
        self.best.clear()
        self.folded = False

    def ante(self):
        """ remove ante and add to pot """
        global pot
        self.chips -= 1
        pot += 1

    def bet(self, bet: int, diff: int, player_total: int):
        """ bet a specific amount """
        global pot
        if bet > player_total:
            bet = player_total
        if bet > self.chips: 
            bet = self.chips
        if bet < diff: 
            bet = diff
        self.chips -= bet
        self.betting += bet
        pot += bet

    def deal(self, card):
        """ deals a card to the hand """
        self.hand.append(card)

    def fold(self):
        """ fold the hand """
        self.folded = True
        self.score = 0

    def call(self, community_cards: list):
        """ pick the five used cards and get the hand rank """
        global card_ranks
        self.called.clear()
        print(self.name + ':')
        all_cards = self.hand + community_cards
        for index, card in enumerate(all_cards): 
            print(f'{index+1}: {card}')

        for i in range(1, 6):
            while True:
                try:
                    index = int(input(f'Card #{i}: '))-1
                    if all_cards[index] not in self.called and index < 8:
                        break
                    print('Already using that card')
                except ValueError:
                    print('Not a card #')
            self.called.append(all_cards[index])

        self.best = list(sorted({card_ranks[n[0]] for n in self.called}, reverse=True))

        checks = [                  
            check_one_pair,         
            check_two_pair,         
            check_three_of_a_kind,  
            check_straight,         
            check_flush,            
            check_full_house,       
            check_four_of_a_kind,   
            check_straight_flush    
        ]

        for check in checks[::-1]:
            if check(self.called):
                self.score = checks.index(check)+2
                break
        else:
            self.score = 1

        print('You have', score_key[self.score])
        self.called = sorted(self.called, reverse=True, key=lambda x: (sum(x[0] in i for i in self.called), card_ranks[x[0]]))


clear()
player1 = Player(input('Player 1: '))
player2 = Player(input('Player 2: '))

sleep(1)

community = []

while player1.chips > 0 and player2.chips > 0:
    player1.reset()
    player2.reset()

    community.clear()

    deck = deck_save

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    
    clear()
    pot = 0

    player1.ante()
    player2.ante()

    player1.deal(deck.pop())
    player2.deal(deck.pop())

    player1.deal(deck.pop())
    player2.deal(deck.pop())
    # pre-flop betting
    while not player1.folded and not player2.folded and (player1.chips > 0 or player2.chips > 0):
        clear()
        print(player1.name, 'only!')
        wait()

        print(player1.name + ':')
        print('Cards:', *player1.hand)
        print('Chips:', player1.chips)
        print('Bet:', player1.betting, '\n')

        print('Pot:', pot, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        to_call = player2.betting - player1.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in), to_call, player2.chips)
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break
            if to_call > 0:
                player1.bet(to_call, 0, player2.chips)

        if player1.betting == player2.betting and player2.betting != 0: 
            break

        clear()
        print(player2.name, 'only!')
        wait()

        print(player2.name + ':')
        print('Cards:', *player2.hand)
        print('Chips:', player2.chips)
        print('Bet:', player2.betting, '\n')

        print('Pot:', pot, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player1.name, 'bet:', player1.betting, '\n')

        to_call = player1.betting - player2.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in), to_call, player1.chips)
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
            if to_call > 0:
                player2.bet(to_call, 0, player1.chips)

        if player1.betting == player2.betting:
            break
    clear()
    wait()

    # deal the flop
    print('Heads up!!!')
    print('The flop:')
    
    deck.pop()
    community += [deck.pop() for _ in range(3)]
    print(*community)

    sleep(3)

    player2.last = player2.betting
        
    # flop betting
    while not player1.folded and not player2.folded and (player1.chips > 0 or player2.chips > 0):
        clear()
        print(player1.name, 'only!')
        wait()

        print(player1.name + ':')
        print('Cards:', *player1.hand)
        print('Chips:', player1.chips)
        print('Bet:', player1.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        to_call = player2.betting - player1.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in), to_call, player2.chips)
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break
            if to_call > 0:
                player1.bet(to_call, 0, player2.chips)

        if player1.betting == player2.betting and player2.betting != player2.last: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()
        
        print(player2.name + ':')
        print('Cards:', *player2.hand)
        print('Chips:', player2.chips)
        print('Bet:', player2.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player1.name, 'bet:', player1.betting, '\n')

        to_call = player1.betting - player2.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in), to_call, player1.chips)
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
            if to_call > 0:
                player2.bet(to_call, 0, player1.chips)
        
        if player1.betting == player2.betting:
            break
    clear()
    wait()

    # deal the turn 
    print('Heads up!!!')
    print('The turn:')
    
    deck.pop()
    community += [deck.pop()]
    print(*community)

    sleep(3)

    player2.last = player2.betting
        
    # turn betting
    while not player1.folded and not player2.folded and (player1.chips > 0 or player2.chips > 0):
        clear()
        print(player1.name, 'only!')
        wait()

        print(player1.name + ':')
        print('Cards:', *player1.hand)
        print('Chips:', player1.chips)
        print('Bet:', player1.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        to_call = player2.betting - player1.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in), to_call, player2.chips)
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break
            if to_call > 0:
                player1.bet(to_call, 0, player2.chips)

        if player1.betting == player2.betting and player2.betting != player2.last: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()

        print(player2.name + ':')
        print('Cards:', *player2.hand)
        print('Chips:', player2.chips)
        print('Bet:', player2.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player1.name, 'bet:', player1.betting, '\n')

        to_call = player1.betting - player2.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in), to_call, player1.chips)
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
            if to_call > 0:
                player2.bet(to_call, 0, player1.chips)
        
        if player1.betting == player2.betting:
            break
    clear()
    wait()

    # deal the river 
    print('Heads up!!!')
    print('The river:')
    
    deck.pop()
    community += [deck.pop()]
    print(*community)

    sleep(3)

    player2.last = player2.betting

        
    # river betting
    while not player1.folded and not player2.folded and (player1.chips > 0 or player2.chips > 0):
        clear()
        print(player1.name, 'only!')
        wait()

        print(player1.name + ':')
        print('Cards:', *player1.hand)
        print('Chips:', player1.chips)
        print('Bet:', player1.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        to_call = player2.betting - player1.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in), to_call, player2.chips)
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break
            if to_call > 0:
                player1.bet(to_call, 0, player2.chips)

        if player1.betting == player2.betting and player2.betting != player2.last: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()

        print(player2.name + ':')
        print('Cards:', *player2.hand)
        print('Chips:', player2.chips)
        print('Bet:', player2.betting, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player1.name, 'bet:', player1.betting, '\n')

        to_call = player1.betting - player2.betting
        print(to_call, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in), to_call, player1.chips)
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
            if to_call > 0:
                player2.bet(to_call, 0, player1.chips)
        
        if player1.betting == player2.betting:
            break
    clear()
    wait()

    # compute the hands of each
    if not player1.folded and not player2.folded:
        print(player1.name, 'only!')
        wait()
        player1.call(community)
        sleep(2)
        clear()

        print(player2.name, 'only!')
        wait()
        player2.call(community)
        sleep(2)
        clear()

    if player1.score > player2.score or player2.folded:
        print(player1.name, 'wins!')
        print('They had:', *player1.called)
        print('Called as:', score_key[player1.score])
        print(player2.name, 'had', *player2.called)
        print('Called as:', score_key[player2.score])
        player1.chips += pot
    elif player2.score > player1.score or player1.folded:
        print(player2.name, 'wins!')
        print('They had:', *player2.called)
        print('Called as:', score_key[player2.score])
        print(player1.name, 'had', *player1.called)
        print('Called as:', score_key[player1.score])
        player2.chips += pot
    else:
        if player1.score == 7:
            player1.best = [card_ranks[n] for n in sorted(set([i[0] for i in player1.called]), key=lambda x: player1.called.count(x), reverse=True)]
            player2.best = [card_ranks[n] for n in sorted(set([i[0] for i in player2.called]), key=lambda x: player2.called.count(x), reverse=True)]
        
        for p1, p2 in zip(player1.best, player2.best):
            if p1 > p2:
                print(player1.name, 'wins!')
                print('They had:', *player1.called)
                print('Called as:', score_key[player1.score])
                print(player2.name, 'had', *player2.called)
                print('Called as:', score_key[player2.score])
                player1.chips += pot
                break
            elif p2 > p1:
                print(player2.name, 'wins!')
                print('They had:', *player2.called)
                print('Called as:', score_key[player2.score])
                print(player1.name, 'had', *player1.called)
                print('Called as:', score_key[player1.score])
                player2.chips += pot
                break
        else:
            print('You tie! Split the pot!!!')
            print(player1.name, 'had:', *player1.called)
            print('Called as:', score_key[player1.score])
            print(player2.name, 'had:', *player2.called)
            print('Called as:', score_key[player2.score])

            player1.chips += pot//2
            player2.chips += pot//2
        
    wait()

if player1.chips <= 0:
    print(player2.name, 'wins the game!!!')
else:
    print(player1.name, 'wins the game!!!')
