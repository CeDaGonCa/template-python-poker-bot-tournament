import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class RNNAgent(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, output_size=1):
        """
        Initialize the RNN-based policy network.

        Args:
            input_size (int): Size of the input features for the RNN (1 for bet fractions).
            hidden_size (int): Number of hidden units in the RNN.
            output_size (int): Size of the output (1 for bet fraction).
        """
        super(RNNAgent, self).__init__()
        # RNN for processing the sequence of each player's history of actions
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        # Fully connected layers for scalar features
        self.fc_scalar = nn.Linear(6, hidden_size)  # 6 scalar features
        # Final output layer
        self.fc_out = nn.Linear(hidden_size * 2, output_size)  # Concatenated RNN and scalar features
        self.sigmoid = nn.Sigmoid()

    def forward(self, state):
        """
        Forward pass through the model.

        Args:
            state (dict): Dictionary containing all game state features.

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, output_size).
        """
        # Extract features from the state
        players_history = state["players_history"]  # List of lists of bet fractions
        num_players_ratio = state["num_players_ratio"]  # Number of players left / players that started
        opp_bankroll_stdev = state["opp_bankroll_stdev"]  # Opponent's bankroll stdev from average
        hand_strength = state["hand_strength"]  # Percentage of hands that beat my hand
        pot_big_blind = state["pot_big_blind"]  # Pot / big blind
        my_bankroll_stdev = state["my_bankroll_stdev"]  # My bankroll stdev from average
        my_position = state["my_position"]  # My position (0 for first to act, 1 for last to act)

        # Process each player's history of actions with RNN
        rnn_outputs = []
        for history in players_history:
            history = torch.tensor(history, dtype=torch.float32).unsqueeze(0).unsqueeze(-1)  # Shape: (1, seq_len, 1)
            rnn_out, _ = self.rnn(history)  # Shape: (1, seq_len, hidden_size)
            rnn_outputs.append(rnn_out[:, -1, :])  # Use the output of the last time step
        rnn_combined = torch.mean(torch.stack(rnn_outputs), dim=0)  # Average over players

        # Concatenate scalar features
        scalar_features = torch.tensor([
            num_players_ratio, opp_bankroll_stdev, hand_strength, pot_big_blind, my_bankroll_stdev, my_position
        ], dtype=torch.float32).unsqueeze(0)  # Shape: (1, 6)
        scalar_out = self.fc_scalar(scalar_features)  # Shape: (1, hidden_size)

        # Concatenate RNN output and scalar features
        combined = torch.cat([rnn_combined, scalar_out], dim=-1)  # Shape: (1, hidden_size * 2)

        # Final output
        out = self.fc_out(combined)
        out = self.sigmoid(out)  # Ensure output is between 0 and 1
        return out

    def act(self, state):
        """
        Predict the bet fraction for a given state.

        Args:
            state (dict): Input state (dictionary of features).

        Returns:
            float: Bet fraction (between 0 and 1).
        """
        self.eval()  # Set model to evaluation mode
        with torch.no_grad():
            bet_fraction = self(state).item()
            return bet_fraction

def compute_reward(outcome, money_betted, money_won, potential_winnings):
    """
    Compute the reward based on the outcome.

    Args:
        outcome (str): "win" or "lose".
        money_betted (float): Amount of money betted.
        money_won (float): Amount of money won.
        potential_winnings (float): Potential winnings if the bot had won.

    Returns:
        float: Reward value.
    """
    if outcome == "win":
        return money_won / money_betted  # Positive reward: money won / money betted
    else:
        return -money_betted / potential_winnings  # Negative reward: money lost / potential winnings

def train(agent, rounds, optimizer):
    """
    Train the agent using policy gradients.

    Args:
        agent (RNNAgent): The RNN-based policy network.
        rounds (list): List of rounds, where each round contains states, actions, and outcomes.
        optimizer (torch.optim): Optimizer for the agent.
    """
    agent.train()  # Set model to training mode
    for round in rounds:
        states, actions, outcomes = round
        # Compute rewards for each state in the round
        rewards = []
        for outcome, money_betted, money_won, potential_winnings in outcomes:
            reward = compute_reward(outcome, money_betted, money_won, potential_winnings)
            rewards.append(reward)
        rewards = torch.tensor(rewards, dtype=torch.float32)

        # Normalize rewards
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)

        # Update model
        optimizer.zero_grad()
        for state, action, reward in zip(states, actions, rewards):
            output = agent(state)
            loss = -torch.log(output) * reward  # Policy gradient loss
            loss.backward()
        optimizer.step()


# Example usage
if __name__ == "__main__":
    # Example game state
    state = {
        "players_history": [
            [0.1, 0.2, 0.0],  # Player 1's history of actions
            [0.5, 0.0, 0.8],  # Player 2's history of actions
            [0.0, 0.0, 0.0],  # Player 3's history of actions
            [0.3, 0.4, 0.1]   # Player 4's history of actions
        ],
        "num_players_ratio": 0.75,  # 3 players left out of 4
        "opp_bankroll_stdev": 0.2,  # Opponent's bankroll stdev from average
        "hand_strength": 0.7,  # 30% of hands beat my hand
        "pot_big_blind": 10.0,  # Pot is 10 big blinds
        "my_bankroll_stdev": 0.1,  # My bankroll stdev from average
        "my_position": 0.5  # My position (0 for first to act, 1 for last to act)
    }

    # Initialize agent and optimizer
    agent = RNNAgent()
    optimizer = optim.Adam(agent.parameters(), lr=0.001)

    # Example training data
    rounds = [
        (
            [state],  # States
            [0.5],  # Actions (bet fractions)
            [("win", 100, 200, 300)]  # Outcomes (outcome, money_betted, money_won, potential_winnings)
        )
    ]

    # Train the agent
    train(agent, rounds, optimizer)

    # Predict bet fraction for a new state
    bet_fraction = agent.act(state)
    print("Predicted Bet Fraction:", bet_fraction)