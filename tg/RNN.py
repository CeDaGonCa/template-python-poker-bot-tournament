import torch
import torch.nn as nn
import torch.optim as optim

class RNNAgent(nn.Module):
    def __init__(self, input_size=8, hidden_size=64, output_size=1):
        """
        Initialize the RNN-based policy network.

        Args:
            input_size (int): Size of the input features for the RNN.
            hidden_size (int): Number of hidden units in the RNN.
            output_size (int): Size of the output (1 for bet fraction).
        """
        super(RNNAgent, self).__init__()
        # RNN for processing the state sequence
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        # Final output layer
        self.fc_out = nn.Linear(hidden_size, output_size)
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
        hands_that_beat_me = state["hands_that_beat_me"]  # Percentage of hands that beat my hand
        pot = state["pot"]  # Current pot size
        my_bankroll = state["my_bankroll"]  # My bankroll
        first_to_talk = state["first_to_talk"]  # Boolean (1 for True, 0 for False)
        round_type = state["round_type"]  # One-hot encoded round type

        # Combine all features into a single vector
        state_vector = [
            hands_that_beat_me,
            pot,
            my_bankroll,
            first_to_talk,
            *round_type  # Unpack one-hot encoded round type
        ]

        # Convert to tensor
        state_vector = torch.tensor(state_vector, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, input_size)

        # Process the state vector with RNN
        rnn_out, _ = self.rnn(state_vector)  # Shape: (1, 1, hidden_size)
        rnn_final = rnn_out[:, -1, :]  # Use the output of the last time step

        # Final output
        out = self.fc_out(rnn_final)
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

def train(agent, rounds, optimizer):
    """
    Train the agent using policy gradients.

    Args:
        agent (RNNAgent): The RNN-based policy network.
        rounds (list): List of rounds, where each round contains states, actions, and a reward.
        optimizer (torch.optim): Optimizer for the agent.
    """
    agent.train()  # Set model to training mode
    optimizer.zero_grad()

    # Compute loss for each round
    loss = 0
    for round in rounds:
        states = round["states"]  # List of states in the round
        actions = round["actions"]  # List of actions taken in the round
        reward = round["reward"]  # Reward for the entire round

        # Compute loss for each state-action pair in the round
        for state, action in zip(states, actions):
            output = agent(state)
            loss += -torch.log(output) * reward  # Policy gradient loss

    # Backpropagate and update weights
    loss.backward()
    optimizer.step()

# Example usage
if __name__ == "__main__":
    # Initialize agent and optimizer
    agent = RNNAgent()
    optimizer = optim.Adam(agent.parameters(), lr=0.001)

    # Sample data for training
    rounds = [
        {
            "states": [
                {
                    "hands_that_beat_me": 0.3,
                    "pot": 100,
                    "my_bankroll": 950,
                    "first_to_talk": 1,
                    "round_type": [1, 0, 0, 0]  # Pre-flop
                },
                {
                    "hands_that_beat_me": 0.25,
                    "pot": 2000,
                    "my_bankroll": 950,
                    "first_to_talk": 0,
                    "round_type": [0, 1, 0, 0]  # Flop
                }
            ],
            "actions": [0.1, 0.0],  # Actions taken in the round
            "reward": 1.0  # Reward for the round
        },
        {
            "states": [
                {
                    "hands_that_beat_me": 0.4,
                    "pot": 500,
                    "my_bankroll": 1000,
                    "first_to_talk": 1,
                    "round_type": [1, 0, 0, 0]  # Pre-flop
                },
                {
                    "hands_that_beat_me": 0.35,
                    "pot": 1500,
                    "my_bankroll": 1000,
                    "first_to_talk": 0,
                    "round_type": [0, 1, 0, 0]  # Flop
                }
            ],
            "actions": [0.2, 0.0],  # Actions taken in the round
            "reward": -0.5  # Reward for the round
        }
    ]

    # Train the agent
    train(agent, rounds, optimizer)

    # Test the agent on a new state
    new_state = {
        "hands_that_beat_me": 0.4,  # 40% of hands beat my hand
        "pot": 500,                 # Current pot size
        "my_bankroll": 1000,        # My bankroll
        "first_to_talk": 1,         # I am first to act (1 for True, 0 for False)
        "round_type": [1, 0, 0, 0]  # Pre-flop (one-hot encoded)
    }

    # Predict bet fraction for the new state
    bet_fraction = agent.act(new_state)
    print("Predicted Bet Fraction for New State:", bet_fraction)