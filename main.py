#!/usr/bin/env python3
import asyncio
import argparse
import random
from tg.bot import Bot
from treys import Evaluator
import time

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
<<<<<<< HEAD
        print('acting', state, hand, self.my_id))
=======
        print('acting', type(state), hand, self.my_id)
>>>>>>> 450468c93658fb90c1f179ba802dfde85fb195c3
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
    elif args.type == "insecure":
        bot = Insequre(args.host,args.port, args.room, "insecure")
    else:
        bot = TemplateBot(args.host, args.port, args.room, args.username)
    asyncio.run(bot.start())
