# CL: python use PyTorch and Reinforcement Learning write AI can play Tetris game, have same game train data.

## Here's a Python script using PyTorch and Reinforcement Learning to create an AI that can play Tetris. This implementation uses a Deep Q-Network (DQN) approach:

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# Define the Tetris environment (simplified for this example)
class TetrisEnv:
    def __init__(self):
        self.board = np.zeros((20, 10))
        self.current_piece = self.new_piece()
        
    def new_piece(self):
        # Simplified: just return a random piece
        return np.random.randint(0, 7)
    
    def step(self, action):
        # Simplified: perform action and return new state, reward, done
        # Action: 0 - left, 1 - right, 2 - rotate, 3 - down
        reward = 0
        done = False
        
        # Implement game logic here
        
        return self.get_state(), reward, done
    
    def get_state(self):
        # Return the current state of the game
        return np.copy(self.board)

# Define the DQN model
class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Define the agent
class TetrisAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters())
        self.criterion = nn.MSELoss()
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return np.argmax(act_values.cpu().data.numpy())
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * np.amax(self.model(next_state).cpu().data.numpy())
            state = torch.FloatTensor(state).unsqueeze(0)
            target_f = self.model(state)
            target_f[0][action] = target
            loss = self.criterion(self.model(state), target_f)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Training the agent
env = TetrisEnv()
state_size = 200  # 20x10 board
action_size = 4  # left, right, rotate, down
agent = TetrisAgent(state_size, action_size)

episodes = 1000
batch_size = 32

for e in range(episodes):
    state = env.get_state().flatten()
    for time in range(500):  # max 500 steps per episode
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = next_state.flatten()
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            print(f"episode: {e}/{episodes}, score: {time}")
            break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

# Save the trained model
torch.save(agent.model.state_dict(), "tetris_model.pth")

