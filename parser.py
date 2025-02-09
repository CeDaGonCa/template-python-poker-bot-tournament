"""
number of players left / players that started the round : [0,1]
opponent's bankroll stdev from average bankroll
percentage of hands that beat my hand [0,1]
pot / big blind
my bank roll stdev from avg
my position (last to play or first to play?) [0,1]
each player's history of actions list of lists of floats between 0 and 1
round (pre flop, flop, etc..) (one hot encoding)



Form of Data

start game 480586a1-e9b3-4b9d-ba9f-27e3ad477348

asked to act
acting namespace(done=False, pot=150, players=[namespace(last_round=None, id='joey.atie@mail.mcgill.ca', stack=900, folded=False, current_bet=100, should_move=True), namespace(last_round=None, id='MachineStruggling', stack=950, folded=False, current_bet=50, should_move=True)], round='pre-flop', target_bet=100, dealer_position=0, small_blind=50, big_blind=100, cards=[], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=5), namespace(suit='spades', rank=8)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='raise', amount=100) namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=300, players=[namespace(last_round='pre-flop', id='joey.atie@mail.mcgill.ca', stack=800, folded=False, current_bet=200, should_move=False), namespace(last_round='pre-flop', id='MachineStruggling', stack=900, folded=False, current_bet=100, should_move=True)], round='pre-flop', target_bet=200, dealer_position=0, small_blind=50, big_blind=100, cards=[], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=5), namespace(suit='spades', rank=8)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='call') namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=400, players=[namespace(last_round='flop', id='joey.atie@mail.mcgill.ca', stack=800, folded=False, current_bet=200, should_move=False), namespace(last_round='pre-flop', id='MachineStruggling', stack=800, folded=False, current_bet=200, should_move=True)], round='flop', target_bet=200, dealer_position=0, small_blind=50, big_blind=100, cards=[namespace(suit='spades', rank=5), namespace(suit='diamonds', rank=2), namespace(suit='spades', rank=3)], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=5), namespace(suit='spades', rank=8)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='fold') namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
game over namespace(joey.atie@mail.mcgill.ca=0, _machine_struggling=400)


start game 480586a1-e9b3-4b9d-ba9f-27e3ad477348

opponent action? namespace(type='call') namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=200, players=[namespace(last_round='pre-flop', id='joey.atie@mail.mcgill.ca', stack=700, folded=False, current_bet=100, should_move=False), namespace(last_round=None, id='MachineStruggling', stack=1100, folded=False, current_bet=100, should_move=True)], round='pre-flop', target_bet=100, dealer_position=1, small_blind=50, big_blind=100, cards=[], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=6), namespace(suit='spades', rank=12)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='raise', amount=200) namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=400, players=[namespace(last_round='flop', id='joey.atie@mail.mcgill.ca', stack=500, folded=False, current_bet=300, should_move=False), namespace(last_round='pre-flop', id='MachineStruggling', stack=1100, folded=False, current_bet=100, should_move=True)], round='flop', target_bet=300, dealer_position=1, small_blind=50, big_blind=100, cards=[namespace(suit='hearts', rank=9), namespace(suit='diamonds', rank=10), namespace(suit='spades', rank=5)], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=6), namespace(suit='spades', rank=12)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='call') namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=600, players=[namespace(last_round='turn', id='joey.atie@mail.mcgill.ca', stack=500, folded=False, current_bet=300, should_move=False), namespace(last_round='flop', id='MachineStruggling', stack=900, folded=False, current_bet=300, should_move=True)], round='turn', target_bet=300, dealer_position=1, small_blind=50, big_blind=100, cards=[namespace(suit='hearts', rank=9), namespace(suit='diamonds', rank=10), namespace(suit='spades', rank=5), namespace(suit='diamonds', rank=7)], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=6), namespace(suit='spades', rank=12)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
opponent action? namespace(type='call') namespace(player_id='4d96d7c9-d5d1-4252-a21c-adb5d3412dab', username='joey.atie@mail.mcgill.ca')
asked to act
acting namespace(done=False, pot=600, players=[namespace(last_round='river', id='joey.atie@mail.mcgill.ca', stack=500, folded=False, current_bet=300, should_move=False), namespace(last_round='turn', id='MachineStruggling', stack=900, folded=False, current_bet=300, should_move=True)], round='river', target_bet=300, dealer_position=1, small_blind=50, big_blind=100, cards=[namespace(suit='hearts', rank=9), namespace(suit='diamonds', rank=10), namespace(suit='spades', rank=5), namespace(suit='diamonds', rank=7), namespace(suit='clubs', rank=7)], whose_turn='MachineStruggling') [namespace(suit='diamonds', rank=6), namespace(suit='spades', rank=12)] 480586a1-e9b3-4b9d-ba9f-27e3ad477348
game over namespace(joey.atie@mail.mcgill.ca=0, _machine_struggling=600)
"""


#!/usr/bin/env python3
import asyncio
import argparse
import numpy as np

from tg.bot import Bot
import time

from tg.types import Card, Rank, Suit

from treys import Deck, Evaluator, Card as TreysCard
import random
from types import SimpleNamespace

parser = argparse.ArgumentParser(
    prog='Template bot',
    description='A Turing Games poker bot that always checks or calls, no matter what the target bet is (it never folds and it never raises)')

parser.add_argument('--port', type=int, default=1999,
                    help='The port to connect to the server on')
parser.add_argument('--host', type=str, default='localhost',
                    help='The host to connect to the server on')
parser.add_argument('--room', type=str, default='my-new-room',
                    help='The room to connect to')
parser.add_argument('--username', type=str, default='bot',
                    help='The username to use')

args = parser.parse_args()

# Always call
class TemplateBot(Bot):
    def act(self, state, hand):

        round = np.array([0, 0, 0])
        if (state.round == "flop"):
            round = [1, 0, 0]
        elif (state.round == "turn"):
            round = [0, 1, 0]
        elif (state.round == "river"):
            round = [0, 0, 1]


        strength = evaluate_hand_with_board(hand, state.cards)

        buffer = round + " , " + state.pot + " , " + state.dealer_position + " , " + state.players.last_round + " , " + state.players[1].stack + " , " + round(strength, 32)
        file = open("parsed.csv", "a")
        file.write(buffer)
        file.close()

        return {'type': 'call'}

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)

if __name__ == "__main__":
    bot = TemplateBot(args.host, args.port, args.room, args.username)
    asyncio.run(bot.start())



def convert_namespace_to_card(ns):
    return SimpleNamespace(rank=ns.rank, suit=ns.suit)

def convert_card_to_treys(card: SimpleNamespace) -> int:
    """Converts a namespace Card object to Treys format."""
    rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(card.rank, str(card.rank))
    suit_str = card.suit[0].lower()  # 'hearts' -> 'h', 'spades' -> 's', etc.
    return TreysCard.new(rank_str + suit_str)

def evaluate_hand_with_board(hole_cards, board_cards, simulations=10000):
    """
    Evaluates the current strength of a poker hand given the board.
    Uses Monte Carlo simulations to estimate the winning probability against a random hand.
    """
    deck = Deck()
    evaluator = Evaluator()
    
    # Convert namespace objects to Treys format
    hole_cards = [convert_card_to_treys(convert_namespace_to_card(card)) for card in hole_cards]
    board_cards = [convert_card_to_treys(convert_namespace_to_card(card)) for card in board_cards]
    
    # Remove used cards from the deck
    for card in hole_cards + board_cards:
        deck.cards.remove(card)
    
    win_count = 0
    
    for _ in range(simulations):
        # Generate a random opponent hand
        opponent_hand = deck.draw(2)
        
        # Complete the board if not fully revealed
        remaining_community_cards = deck.draw(5 - len(board_cards))
        full_board = board_cards + remaining_community_cards
        
        # Evaluate hands
        my_score = evaluator.evaluate(full_board, hole_cards)
        opponent_score = evaluator.evaluate(full_board, opponent_hand)
        
        if my_score < opponent_score:  # Lower score means a stronger hand
            win_count += 1
    
    win_probability = win_count / simulations
    return win_probability
