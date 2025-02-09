from types import SimpleNamespace
import numpy as np
from treys import Deck, Evaluator, Card as TreysCard
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from bot import Bot

class LinearRegressionAgent:
    def __init__(self, state_size, action_size, weights):
        self.state_size = state_size
        self.action_size = action_size
        self.states = np.empty((0, state_size))  # Initialize as an empty 2D array
        self.model = LinearRegression()
        self.X = []  # state-action pairs as input features
        self.y = []  # rewards as target values

        self.weights = np.array(weights)


    def addToMemory(self, state):
        self.states = np.vstack([self.states, state])  # Append new row

    def get_q_value(self, state, action):
        if len(self.X) > 0:
            # Concatenate state with action to form the state-action vector
            state_action = np.concatenate([state, [action]])
            print("state action:", state_action)
            # Manually compute the q-value: dot product of weights and state-action vector
            q_value = np.dot(self.weights[:-1].T, state_action) + self.weights[-1]  # Exclude intercept from dot product
            
            print("Manually computed q-value:", q_value)
            return q_value
        else:
            return 0.0

    def learnOutcome(self, state, actions, rewards):
        decision = self.act(state)
        print(f"Decision made for state {state}: {decision}")
        self.train(self.states, actions, rewards)
        self.states = np.empty((0, self.state_size))  # Reset stored states

    def act(self, state):
        q_values = [self.get_q_value(state, action) for action in range(self.action_size)]
        print(f"Q-values for state {state}: {q_values}")
        return np.max(q_values)

    def update(self, state, action, reward, next_state, done):
        state_action = np.concatenate([state, [action]])
        self.X.append(state_action)
        self.y.append(reward)

        if done:
            self.X = np.array(self.X)
            self.y = np.array(self.y)
            self.model.fit(self.X, self.y)
            self.X, self.y = [], []

    

    def train(self, states, actions, rewards, max_iter=500):
        print("Training started...")

        actions = np.atleast_2d(actions).T  # Reshape actions to (n, 1)
        self.X = np.column_stack((states, actions))
        self.y = rewards

        # Initialize SGDRegressor (learning_rate="constant" and warm_start=True allow for incremental training)
        self.model = SGDRegressor(learning_rate="constant", eta0=0.01, max_iter=max_iter, warm_start=True)

        # Perform the training with max_iter
        self.model.fit(self.X, self.y)

        # Get the updated weights after training
        coef = self.model.coef_  # Shape (5,)
        intercept = self.model.intercept_  # Shape (1,)

        # Reshaping coef_ to (5, 1)
        coef_reshaped = coef.reshape(-1, 1)
        
        # Reshaping intercept_ to (1, 1)
        intercept_reshaped = intercept.reshape(1, 1)

        # Concatenate coefficients and intercept
        weights = np.concatenate([coef_reshaped, intercept_reshaped], axis=0)
        self.weights = weights

        print("Reshaped Coefficients:", coef_reshaped.shape)  # Should print (5, 1)
        print("Reshaped Intercept:", intercept_reshaped.shape)  # Should print (1, 1)
        print("Concatenated Weights:", weights)  # Should print (6, 1)
        print(f"Training complete!")

# Example usage
 
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

def get_reward(payouts: SimpleNamespace, bot_username: str) -> float:
    for username in vars(payouts):  # `vars()` gives access to object attributes
        payout = getattr(payouts, username)  # Get payout by attribute name
        if payout > 0:
            if username == bot_username:
                return payout / 2000  # Positive reward for bot
            else:
                return -payout / 2000  # Negative reward for others

    # Return 0 if no payout condition met
    return 0
    

class LRBot(Bot):

    def __init__(self, host, port, room, username):
        self.username = username
        super().__init__(host, port, room, username)
        self.model = LinearRegressionAgent(7, 2, [0.8, 0.1,0.1,0.1,0.4, 0.1, 0.1])
        self.actions = np.array([])

    def act(self, state, hand):
        print('asked to act')
        print('acting', type(state), hand, self.my_id)
        hand_stg = 0.9
        pot = state.pot / 1000
        dealer_pos = state.dealer_position
        round = one_hot(state.round)
        stack = state.players[1].stack / 1000
        model_state = np.array([hand_stg, pot, stack, dealer_pos, round[0], round[1], round[2]])
        print("current state: ", model_state)
        self.model.addToMemory(model_state)
        decision = self.model.act(model_state)
        print("decision: ", decision)
        self.actions = np.append(self.actions, decision)
    
        

        bet_amount = decision * state.players[1].stack

        if (bet_amount > state.target_bet):
            print("you raised")
            return {'type': 'raise', 'amount' : bet_amount - state.target_bet}
        
        if (bet_amount > state.target_bet * 0.90):
             return {'type' : 'call'}
        
        return {'type' : 'fold'}

        

    def opponent_action(self, action, player):
        print('opponent action?', action, player)

    def game_over(self, payouts):
        print('game over', payouts)
        print(self.model.states)
        print(self.actions)
        print(get_reward(payouts, self.username))
        self.model.learnOutcome(self.model.states[-1], self.actions, np.full(len(self.model.states), get_reward(payouts, self.username)))
        self.actions = np.array([])
        

    def start_game(self, my_id):
        self.my_id = my_id
        print('start game', my_id)