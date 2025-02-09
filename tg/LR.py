import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor

class LinearRegressionAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.states = np.empty((0, state_size))  # Initialize as an empty 2D array
        self.model = LinearRegression()
        self.X = []  # state-action pairs as input features
        self.y = []  # rewards as target values

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
if __name__ == "__main__":
    state_size = 4
    action_size = 2

    states = np.array([
        [0.9, 2, 0.950, 0],
    ], dtype=np.float64)

    actions = np.array([0])
    rewards = np.array([-0.7])

    agent = LinearRegressionAgent(state_size, action_size)
    
    for state in states:
        agent.addToMemory(state)
    agent.learnOutcome(states[0], actions, rewards)
    print("Final action decision:", agent.act(states[0]))



   