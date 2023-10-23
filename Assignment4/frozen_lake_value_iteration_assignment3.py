import gym
from collections import Counter, defaultdict
import numpy as np
import sys

ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
TEST_EPISODES = 20
SEED = 42


ACTIONS = { 0:"Left",
           1: "Down",
           2:"Right",
           3: "Up  "}


class Agent:
    def __init__(self):
        # Define env
        self.env = self.create_env()
        # Define state
        self.state = 0
        self.numberStates = self.env.observation_space.n
        self.numberActions = self.env.action_space.n
        # Define rewards
        self.rewards = defaultdict(lambda: defaultdict(lambda: 0))
        # Define transits
        self.transits = defaultdict(lambda: Counter())
        # Define values
        self.value_table = np.zeros(self.numberStates)
        pass

    @staticmethod
    def create_env():
        # Return created environment
        return gym.make(ENV_NAME, is_slippery=True)
        

    def update_transits_rewards(self, state, action, new_state, reward):
        # Get the key, which is a state action pair
        key = (state, action)
        # update rewards which is accessed by key plus the new state
        self.rewards[key][new_state] += reward 
        # update transits count which is accessed by key and new_state
        self.transits[key][new_state]+=1
        

    def play_n_random_steps(self, count):

        self.env.reset()
        
        # for loop that iterates count number of times
        for i in range(count):
            # get an action
            random_action = self.env.action_space.sample()
            # step through the environment
            observation, reward, terminated, info = self.env.step(random_action)
          
            # update the transits rewards
            self.update_transits_rewards(self.state, random_action, observation, reward)
            # update the state
            self.state=observation

            if terminated == True:
                #reset the env and place the agent back to beginning
                self.env.reset()
                self.state=0
            

    def print_value_table(self):
        # print the value table in a 2d matrix format
        output = ""
        for i, val in enumerate(self.value_table):
            if i % 4 == 0:
                output += ("\n")
            output += (" %.3f " % val)
        print(output)

        

    def extract_policy(self):
        # Define policy as an empty list
        policy = []
        # for every state
        for i in range(self.numberStates):
            # select the action
            action = self.select_action(i)
            # append action to the policy
            policy.append(action)
        # return policy
        return policy
      

    def print_policy(self, policy):
        # define actions in NL
            #did that up top
        # nested for loop to print the actions in 2d matrix format
        output=""
        for i, val in enumerate(policy):
            if i % 4 == 0:
                output += ("\n")
            output += (" {} ".format (ACTIONS[val]))
        print(output)
        

    def calc_action_value(self, state, action):
        # get target counts which access transits by state, action
        target_counts = self.transits[(state,action)]
        #
        # get the sum of all the counts
        sum_counts = sum(target_counts.values())

        return_sum=0
        #print(tar_counts)
        #print(self.value_table)
        # for each target state
        for pair in target_counts:
         #   print(pair)

            # calculate the proportion of reward plus gamma * value of the target state, then sum it all together. 
            prop = target_counts[pair] / sum_counts
            reward = self.rewards[(state,action)][pair]      
            return_sum += prop * (reward + GAMMA * self.value_table[pair])

        # return that sum
        return return_sum

    def select_action(self, state):
        # define best action and best value
        best_action = -sys.maxsize-1
        best_value=-sys.maxsize-1
        # For action in the range of actions
        for i in range(self.numberActions):
            # calculate the action value
            av = self.calc_action_value(state,i)
            # if best value is less than action value
            if best_value < av:
                # update best value and best action
                best_action=i
                best_value=av
        # return best action
        return best_action

    def play_episode(self, env):
        # define reward and state
        reward=0
        env.reset()
        state=0
        count=0
        # While loop
        while True:

            # Ididn't quite get this next set of instructions,
            # What would the difference be if the state is a multiple
            # With the count, would we use that to penalize how long it takes to terminate? 

            temp_reward=0
            # select an action
            action = self.select_action(state)
            # take a step
            observation,rew,terminated,info = env.step(action)
            # if state is multiple
            if state==observation:
                # update reward
                temp_reward+= rew
                # update count
                count+=1
            else:
                # update reward
                temp_reward+= rew 
                # update count
                count+=1
            # update total reward
            reward+=temp_reward
            # get out if we're done
            if terminated:
                #print(observation)
                break
            # set state to new state
            state= observation
        # return total reward
        #print(reward)
        return reward

    def value_iteration(self):
        # for each state
        for i in range(self.numberStates):
            # set state_values equalt to a list of calc_action_value for every action
            state_values =[self.calc_action_value(i,j) for j in range(self.numberActions)]
        # set self values to the max state_values         
            self.value_table[i]=max(state_values)
        


if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()

    iter_no = 0
    best_reward = 0
    while True:
        iter_no += 1
        agent.play_n_random_steps(100)
        agent.value_iteration()

        reward = sum([agent.play_episode(test_env) for _ in range(TEST_EPISODES)]) / TEST_EPISODES# sum of play episode for all 20 episodes / number of episodes
        
        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward=reward

        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            agent.print_value_table()
            policy = agent.extract_policy()
            agent.print_policy(policy)
            break
