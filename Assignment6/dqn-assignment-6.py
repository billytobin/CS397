import gymnasium as gym
import math
import os
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as torch_functional

# Leave this alone, solves a macOS issue
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Create the environment with Gym
env = gym.make("CartPole-v1")

# Set up matplotlib for dynamic plots
is_ipython = "inline" in matplotlib.get_backend()
if is_ipython:
    from IPython import display
plt.ion()

# Determine whether to use a GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
# Define a named tuple to hold experience tuples
Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))

class ReplayMemory(object):
    # Initialize the replay memory with a fixed capacity
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
    
    # Function to save a transition to memory
    def push(self, *args):
        self.memory.append(Transition(*args))
    
    # Function to sample a batch of transitions from memory
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    # Function to get the current size of the memory
    def __len__(self):
        return len(self.memory)

# Define the neural network architecture for DQN
class DQN(nn.Module):
    # Initialize DQN layers
    def __init__(self, inputs, outputs):
        super(DQN, self).__init__()
        # TODO: Define network layers
        self.layer1 = nn.Linear(inputs, 128)
        self.layer2 = nn.Linear(128,64)
        self.layer3 = nn.Linear(64, outputs)
        # TODO: Experiment with number of layers and neurons per layer
        

    # Define forward pass
    def forward(self, x):
        # TODO: Implement the forward pass
        firstL = torch_functional.relu(self.layer1(x))
        secondL = torch_functional.relu(self.layer2(firstL))
        return self.layer3(secondL)
        # TODO: Experiment with different activation functions
        # leaky, tanh, sig
        

# Hyperparameters (TODO: Define appropriate values)
BATCH_SIZE = 150 # Batch size
GAMMA = 0.9 # Discount factor
EPS_START = 0.9 # Starting value of epsilon
EPS_END = 0.05# Minimum value of epsilon
EPS_DECAY = 1000 # Rate of decay for epsilon
TAU = 0.005# Target network update rate
LR = 0.0004# Learning rate

# Get number of actions from gym action space
n_actions = env.action_space.n
# Get the number of state observations
state, info = env.reset()
n_observations = len(state)

# Initialize DQN policy and target networks
policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

steps_done = 0

# Define epsilon-greedy action selection function
def select_action(state):
    global steps_done
    #increment steps done after defining eps threshold
    sample = random.random()
    
    # TODO: define epsilon threshold
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1 * (steps_done / EPS_DECAY))
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # Pass the current state through the policy network to get the Q-values for all actions.
            qvals = policy_net(state)
            # Find the action with the highest Q-value.
            
            ind = np.argmax(qvals)
            
            #act_index = qvals.index(maxAction) #didnt work
            # Reshapes the index into a tensor with shape (1, 1), which can be used for further processing or as an input to another function.
            return torch.tensor([[ind]])
        

            #this seem to be the easiest way to accomplish this


    else:
        # Creates a new PyTorch tensor.
        #going to do so in a few lines, was easier to do so
        # Generate a nested list with a single element, which is a random sample from the environment's action space.
        random_action = env.action_space.sample()
        # Place the tensor on the specified device (CPU or GPU).
        # Set the data type of the tensor to a 64-bit integer.
        
        #It was easiest to do all these in one line
        return torch.tensor([[random_action]], device=device, dtype=torch.long)
    

episode_durations = []

# Define function to plot episode durations
def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title("Result")
    else:
        plt.clf()
        plt.title("Training...")
    plt.xlabel("Episode")
    plt.ylabel("Duration")
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())

def optimize_model():
    # TODO: Implement optimization step : will do in subsequent steps
    # If length of memory is less than batch size, return
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Convert batch-array of Transitions to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))
    # Compute a mask of non-final states and concatenate the batch elements
    non_final_mask = torch.tensor(
        tuple(map(lambda s: s is not None, batch.next_state)),
        device=device,
        dtype=torch.bool,
    )
    # Create a list comprehension that filters out None values from batch.next_state.

    # Concatenates the remaining tensors in the list into a single tensor.
    # The resulting tensor non_final_next_states contains all the next state tensors for non-terminal states in the batch.
    non_final_next_states = torch.cat([s for s in batch.next_state if s is not None ])
    # Concatenates tensors from batch.state into a single tensor.
    # The resulting tensor state_batch contains all state tensors in the batch.
    state_batch = torch.cat(batch.state)
    # Concatenates tensors from batch.action into a single tensor.
    # The resulting tensor action_batch contains all action tensors in the batch.
    action_batch = torch.cat(batch.action)
    # Concatenates tensors from batch.reward into a single tensor.
    # The resulting tensor reward_batch contains all reward tensors in the batch.
    reward_batch = torch.cat(batch.reward)
    # Pass the state_batch tensor through the policy_net neural network to get Q-values for all actions.
    # Gather specific Q-values from the result tensor. The 1 indicates that we're selecting values along the action dimension (for each state in the batch).
    # The resulting tensor holding the Q-values corresponding to the actions that were actually taken in each state.
    action_qvals = policy_net(state_batch).gather(1, action_batch)


    # Initialize a tensor for the next state values with zeros for all batch entries.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    # Without gradient calculation for efficiency,
    # update the values for non-final states using the maximum predicted Q-value
    # from the target network, ensuring final states remain zero.
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]
    
    # Compute the expected Q values
    exp_qvals = (next_state_values * GAMMA)+ reward_batch
    # Compute Huber loss
    # using smoothL1loss
    hub_temp = nn.SmoothL1Loss()
    hub = hub_temp(action_qvals,exp_qvals.unsqueeze(1))  
    # Optimize the model
    optimizer.zero_grad()
    hub.backward()
    # In-place gradient clipping, avoids suoper big steps
    nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    #finally step
    optimizer.step()

def main():
    if torch.cuda.is_available():
        num_episodes = 600
    else:
        num_episodes = 50

    for i_episode in range(num_episodes):
        # Initialize the environment and get it's state
        state, info = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for t in count():
            action = select_action(state)
            observation, reward, terminated, truncated, _ = env.step(action.item())
            reward = torch.tensor([reward], device=device)
            done = terminated or truncated

            if terminated:
                next_state = None
            else:
                next_state = torch.tensor(
                    observation, dtype=torch.float32, device=device
                ).unsqueeze(0)

            # Store the transition in memory
            memory.push(state, action, next_state, reward)

            # Move to the next state
            state = next_state

            # Perform one step of the optimization (on the policy network)
            optimize_model()

            # Soft update of the target network's weights
            target_net_state_dict = target_net.state_dict()
            policy_net_state_dict = policy_net.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[
                    key
                ] * TAU + target_net_state_dict[key] * (1 - TAU)
            target_net.load_state_dict(target_net_state_dict)

            if done:
                episode_durations.append(t + 1)
                plot_durations()
                break

    print("Complete")
    plot_durations(show_result=True)
    plt.ioff()
    plt.show()

main()
