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

random.shuffle(deck)
random.shuffle(deck)
random.shuffle(deck)

card_ranks = {
    '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10,'J':11, 'Q':12, 'K':13, 'A':14
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
        self.called.clear()
        self.best.clear()

    def ante(self):
        """ remove ante and add to pot """
        global pot
        self.chips -= 1
        pot += 1

    def bet(self, bet: int):
        """ bet a specific amount """
        global pot
        if bet < 0: 
            bet = 0
        if bet > self.chips: 
            bet = self.chips
        self.chips -= bet
        self.betting += bet
        pot += bet

    def deal(self, *cards):
        """ deals a card to the hand """
        for card in cards:
            self.hand.append(card)

    def fold(self):
        """ fold the hand """
        self.folded = True
        self.score = 0

    def call(self, community_cards: list):
        """ pick the five used cards and get the hand rank """
        global card_ranks
        self.called.clear()
        all_cards = self.hand + community_cards
        for index, card in enumerate(all_cards): 
            print(f'{index+1}: {card}')

        for i in range(1, 6):
            while True:
                try:
                    index = int(input(f'Card #{i}: '))-1
                    if all_cards[index] not in self.called:
                        break
                    print('Already using that card')
                except ValueError:
                    print('Not a card #')
            self.called.append(all_cards[index])

        self.best = list(sorted({card_ranks[n[0]] for n in self.called}))[::-1]

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

        score_key = {
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
        
        print('You have', score_key[self.score])


player1 = Player(input('Player 1: '))
player2 = Player(input('Player 2: '))

sleep(1)

community = []

while player1.chips > 0 and player2.chips > 0:
    player1.reset()
    player2.reset()
    
    clear()
    pot = 0

    player1.ante()
    player2.ante()

    player1.deal(deck.pop())
    player2.deal(deck.pop())

    player1.deal(deck.pop())
    player2.deal(deck.pop())

    # pre-flop betting
    while not player1.folded and not player2.folded:
        clear()
        print(player1.name, 'only!')
        wait()

        print('Cards:', *player1.hand)
        print('Chips:', player1.chips, '\n')

        print('Pot:', pot, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player2.betting - player1.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in))
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break

        if player1.betting == player2.betting and player2.betting != 0: 
            break

        clear()
        print(player2.name, 'only!')
        wait()

        print('Cards:', *player2.hand)
        print('Chips:', player2.chips, '\n')

        print('Pot:', pot, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player1.betting - player2.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in))
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
        
        if player1.betting == player2.betting:
            break
    sleep(2)
    clear()

    # deal the flop
    print('Heads up!!!')
    print('The flop:')
    
    deck.pop()
    community += [deck.pop() for _ in range(3)]
    print(*community)

    sleep(3)

    player2.last = player2.betting
        
    # flop betting
    while not player1.folded and not player2.folded:
        clear()
        print(player1.name, 'only!')
        wait()

        print('Cards:', *player1.hand)
        print('Chips:', player1.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player2.betting - player1.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in))
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break

        if player1.betting == player2.betting and player2.betting != player2.last: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()
        
        print('Cards:', *player2.hand)
        print('Chips:', player2.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player1.betting - player2.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in))
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
        
        if player1.betting == player2.betting:
            break
    sleep(2)
    clear()

    # deal the turn 
    print('Heads up!!!')
    print('The turn:')
    
    deck.pop()
    community += [deck.pop()]
    print(*community)

    sleep(3)

    player2.last = player2.betting
        
    # turn betting
    while not player1.folded and not player2.folded:
        clear()
        print(player1.name, 'only!')
        wait()

        print('Cards:', *player1.hand)
        print('Chips:', player1.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player2.betting - player1.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in))
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break

        if player1.betting == player2.betting and player2.betting != player2.last: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()

        print('Cards:', *player2.hand)
        print('Chips:', player2.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player1.betting - player2.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in))
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
        
        if player1.betting == player2.betting:
            break
    sleep(2)
    clear()

    # deal the river 
    print('Heads up!!!')
    print('The river:')
    
    deck.pop()
    community += [deck.pop()]
    print(*community)

    sleep(3)

    player2.last = player2.betting

        
    # river betting
    while not player1.folded and not player2.folded:
        clear()
        print(player1.name, 'only!')
        wait()

        print('Cards:', *player1.hand)
        print('Chips:', player1.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player2.name, 'chips:', player2.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player2.betting - player1.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player1.bet(int(bet_in))
        except ValueError: 
            if bet_in == 'f':
                player1.fold()
                break

        if player1.betting == player2.betting and player2.betting != player2.betting: 
            break
        
        clear()
        print(player2.name, 'only!')
        wait()

        print('Cards:', *player2.hand)
        print('Chips:', player2.chips, '\n')

        print('Pot:', pot)
        print('Community:', *community, '\n')

        print(player1.name, 'chips:', player1.chips)
        print(player2.name, 'bet:', player2.betting, '\n')

        print(player1.betting - player2.betting, 'to call')
        try: 
            bet_in = input('Bet: ')
            player2.bet(int(bet_in))
        except ValueError:
            if bet_in == 'f':
                player2.fold()
                break
        
        if player1.betting == player2.betting:
            break
    sleep(2)
    clear()

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
        print(player2.name, 'had', *player2.called)
    elif player2.score > player1.score or player1.folded:
        print(player2.name, 'wins!')
        print('The had:', *player2.called)
        print(player1.name, 'had', *player2.called)
    else:
        print('Tie! We\'ll get to it')

    print(player1.score, player2.score)

    print('Success!!!')
    break