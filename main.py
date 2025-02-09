#!/usr/bin/env python3
import asyncio
import argparse
from tg.LRBot import LRBot
from tg.bot import Bot
from treys import Evaluator
from treys import Deck, Evaluator, Card as TreysCard
import random
from types import SimpleNamespace

def convert_namespace_to_card(ns: SimpleNamespace) -> SimpleNamespace:
    #Ensures that a namespace object has rank and suit attributes.
    return SimpleNamespace(rank=ns.rank, suit=ns.suit)

def convert_card_to_treys(card: SimpleNamespace) -> int:
    #Converts a namespace Card object to Treys format.
    rank_map = {1: 'A', 14: 'A', 11: 'J', 12: 'Q', 13: 'K'}  # Ensure Ace is 'A'
    
    # Ensure Ace is treated correctly
    rank = 14 if card.rank == 1 else card.rank # Convert rank 1 to 14 for Treys
    rank_str = rank_map.get(rank, str(rank))  # Convert other ranks normally
   
    suit_str = card.suit[0].lower()  # 'hearts' -> 'h', 'spades' -> 's', etc.
    print(suit_str + rank_str)
    return TreysCard.new(rank_str + suit_str)


def evaluate_hand_with_board(hole_cards, board_cards, simulations=1000):
    
    #Evaluates the current strength of a poker hand given the board.
    #Uses Monte Carlo simulations to estimate the winning probability against a random hand.
    
    # Convert namespace objects to Treys format
    hole_cards = [convert_card_to_treys(convert_namespace_to_card(card)) for card in hole_cards]
    board_cards = [convert_card_to_treys(convert_namespace_to_card(card)) for card in board_cards]
    
    win_count = 0
    
    for _ in range(simulations):
        # Create a fresh copy of the deck for each simulation
        deck = Deck()
        deck.cards = [card for card in deck.cards if card not in board_cards]
        deck.cards = [card for card in deck.cards if card not in hole_cards]
        # remove from the deck the hole cards and the board cards
        evaluator = Evaluator()
        #print(len(board_cards))
        new_cards = deck.draw(5 - len(board_cards))
        board_cards.extend(new_cards)
        #print("new cards:", new_cards)
        #print("board cards:", board_cards)
        #print(board_cards)
        opponent_hand = deck.draw(2)
        
    
        
        # Evaluate hands
        my_score = evaluator.evaluate(hole_cards, board_cards)
        opponent_score = evaluator.evaluate(opponent_hand, board_cards)
        
        if my_score < opponent_score:  # Lower score means a stronger hand
            win_count += 1
    
    win_probability = win_count / simulations
    return win_probability

def one_hot(state_round):
    round = np.zeros(3)
    if (state_round == "flop"):
        round[0] = 1
    elif (state_round == "turn"):
        round[1] = 1
    elif (state_round == "river"):
        round[2] = 1
    return round

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
parser.add_argument('--type', type=str, default='template',
                    help='The type of bot')  # remember to take th

args = parser.parse_args()


# Always call
class TemplateBot(Bot):
    def act(self, state, hand):
        print('asked to act')
        print('acting', type(state), hand, self.my_id)
        return {'type': 'call'}

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)


class Greedy(Bot):
    accumulator = 0

    def act(self, state, hand):
        evalCard = Evaluator(state.cards, hand)
        print('asked to act')
        print('acting', type(state), hand, self.my_id)
        if evalCard // 3 <= 7462 // 3:
            self.accumulator -= 200
            return {'type': 'raise', 'amount': 100}
        elif evalCard // 3 <= (2 * 7462 // 3):
            self.accumulator -= 50
            return {'type': 'call'}
        else:
            return {'type': 'fold'}

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)


class RandomBot(Bot):
    def act(self, state, hand):
        action = random.randint(1, 3)
        print('asked to act')
        print('acting', type(state), hand, self.my_id)
        if action == 1:
            return {'type': 'call'}
        elif action == 2:
            num = random.randomint(100, 2000)  # dont know how to get the stack might change later
            return {'type': 'raise'}
        elif action == 3:
            return {'type': 'fold'}

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)


class Insequre(Bot):
    confidenceLevel = 50

    def act(self, state, hand):
        print('asked to act')
        print('acting', type(state), hand, self.my_id)
        ran = random.randint(0, 100)
        if self.confidenceLevel > ran + 20:
            return {'type': 'raise', "amount": 100}
        elif self.confidenceLevel > ran - 5:
            return {'type': 'call'}
        else:
            return {'type': 'fold'}

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)

        score = payouts.get('insecure')
        for val in payouts.values():
            if score < val:
                self.confidenceLevel -= 20
            else:
                self.confidenceLevel += 25

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)


if __name__ == "__main__":
    if args.type == "random":
        bot = RandomBot(args.host, args.port, args.room, "random")
    elif args.type == "greedy":
        bot = Greedy(args.host, args.port, args.room, "greedy")
    elif args.type == "lr":
        bot = LRBot(args.host, args.port, args.room, "lrbot")
    elif args.type == "insecure":
        bot = Insequre(args.host,args.port, args.room, "insecure")
    else:
        bot = TemplateBot(args.host, args.port, args.room, args.username)
    asyncio.run(bot.start())
