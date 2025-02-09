import torch
import torch.nn as nn
import torch.optim as optim

class OverfittingRNNAgent(nn.Module):
    def __init__(self, input_size=8, hidden_size=128, output_size=1):
        super(OverfittingRNNAgent, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True, num_layers=5)  # More layers
        self.fc_out = nn.Linear(hidden_size, output_size)
        self.tanh = nn.Identity()

    def forward(self, state):
        hands_that_beat_me = state["hands_that_beat_me"]
        pot = state["pot"] / 1000.0
        my_bankroll = state["my_bankroll"] / 1000.0
        first_to_talk = state["first_to_talk"]
        round_type = state["round_type"]

        state_vector = [
            hands_that_beat_me,
            pot,
            my_bankroll,
            first_to_talk,
            *round_type
        ]

        state_vector = torch.tensor(state_vector, dtype=torch.float32, requires_grad=True).unsqueeze(0)
        rnn_out, _ = self.rnn(state_vector)
        out = self.fc_out(rnn_out)
        return self.tanh(out).squeeze(1)  # Output range: [-1, 1]

    def act(self, state):
        self.eval()
        with torch.no_grad():
            bet_fraction = self(state).item()
            return bet_fraction

    def get_feature_weights(self):
        rnn_weights = self.rnn.weight_ih_l0
        fc_weights = self.fc_out.weight
        feature_importance = torch.abs(torch.matmul(fc_weights, rnn_weights)).squeeze()
        feature_importance /= feature_importance.sum()

        feature_names = [
            "hands_that_beat_me", "pot", "my_bankroll", "first_to_talk",
            "round_type_1", "round_type_2", "round_type_3", "round_type_4"
        ]

        return {name: round(weight.item(), 4) for name, weight in zip(feature_names, feature_importance)}

    def train_model(self, rounds, optimizer):
        self.train()
        loss_fn = nn.MSELoss()

        for round in rounds:
            states = round["states"]
            actions = round["actions"]
            reward = round["reward"]

            total_loss = 0

            for state, action in zip(states, actions):
                optimizer.zero_grad()

                output = self(state)
                action_tensor = torch.tensor([action], dtype=torch.float32, requires_grad=True)

                loss = loss_fn(output, action_tensor) * reward  * 2
                total_loss += loss

            total_loss.backward()
            optimizer.step()

# Run the model with overfitting setup
if __name__ == "__main__":
    agent = OverfittingRNNAgent()
    optimizer = optim.RMSprop(agent.parameters(), lr=0.001)

    rounds = [
        {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
              {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
              {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
              {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
              {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
              {
            "states": [
                {"hands_that_beat_me": 0.8, "pot": 100, "my_bankroll": 950, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.9, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.9, 0.9],
            "reward": 1
        },
        {
            "states": [
                {"hands_that_beat_me": 0.1, "pot": 500, "my_bankroll": 1000, "first_to_talk": 1, "round_type": [1, 0, 0, 0]},
                {"hands_that_beat_me": 0.1, "pot": 1500, "my_bankroll": 1000, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
            ],
            "actions": [0.8, 0.9],
            "reward": -1
        }
    ]

    agent.train_model(rounds, optimizer)

    new_state ={"hands_that_beat_me": 0.1, "pot": 2000, "my_bankroll": 950, "first_to_talk": 0, "round_type": [0, 1, 0, 0]}
    bet_fraction = agent.act(new_state)
    print("Predicted Bet Fraction for New State:", bet_fraction)
    print("Feature Weights:", agent.get_feature_weights())
