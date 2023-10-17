#Billy Tobin
#main
import island
import agent
import numpy as np

gamma = .99
num_of_steps = 25



i1 = island.island(1,-1,"Island 1")
i2 = island.island(2,-1,"Island 2")
i3 = island.island(3,2,"Island 3")
i4 = island.island(4,-1,"Island 4")
i5 = island.island(5,-1,"Island 5")
i6 = island.island(6,-1,"Island 6")
i7 = island.island(7,2,"Island 7")
i8 = island.island(8,-1,"Island 8")
i9 = island.island(9,2,"Island 9")
i10 = island.island(10,15,"Island 10", True)

possActions = [i1,i2,i3,i4,i5,i6,i7,i8,i9,i10]

portTrans=[[0,.1,.3,.1,0.1,.2,0,0,.1,0],
           [0,0,0.2,.3,0,0.1,0,.3,0,0],
           [0.1,0,0,0.1,0,.3,0,0,.3,0.1],
           [0.1,0,0.2,0,0,0,.1,.2,0.3,0],
           [0,0,.3,0,0,0.4,0.1,0,0,0.1],
           [0.1,0.3,.2,0.1,0.2,0,0.1,.1,0,0.1],
           [0,0.1,0,0.3,0,0.2,0,0,0.1,0.2],
           [0.1,.2,0,0.2,0,0,0.1,0,0.2,0.2],
           [.1,.3,.1,0,.1,0,0.1,.1,0,0.1],
           [0,0,0,0,0,0,0,0,0,0]]

#for i in range(len(portTrans)):
     #print(portTrans[i][i+1])

#closed form value
p = np.array(portTrans)
r = np.array([i.treasure for i in possActions])
id = np.identity(len([i.treasure for i in possActions]))

Vpi = np.matmul(np.linalg.inv(id-(gamma* p)), r)
#print(Vpi)
#Task 2

def run(steps):
    actions=[]
    curr = i1
    
    agent1 = agent.agent(curr.location, Vpi)
    actions.append(["Start      ",curr.name, 0])
   
    # for i in range(steps):
    #     if curr.terminal == True:
    #         actions.append(" Reached Terminal State")
    #         return actions
    #     probs = portTrans[curr.location-1]
    for i in range(steps):
        nextMove, reward = agent1.move(portTrans[curr.location-1], possActions, curr.terminal)
        
        #if term state is reached
        if nextMove == None:
            actions.append(["Terminate   ",curr.name,reward * (gamma ** i)])
            break
        
        
        #if we want to dig
        # if nextMove == 1:
        #     reward = agent1.dig(curr.treasure)
        #     if curr.treasure:
        #         curr.treasure = False
        #     actions.append(["Dig        ",curr.name,reward * (gamma ** i)])
        
        else: # if we move islands 

            curr = nextMove
            actions.append(["Move Island",curr.name,reward * (gamma ** i)])
        #print(actions)

    #implement Gamma

    '''Should I have implemented gamma at the end of each episode, or does in time work?''' 

    #for i in range(len(actions)):
   #     actions[i][2] = int(actions[i][2]) * (gamma ** float(i))

    return actions

#print(run(25)[0])
results= run(num_of_steps)
print(f"Run 1: \n{results}\n\n")
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in results]))
#Task 3

# for i in range(1,11):
#      results= run(num_of_steps)
#      print(f"\nRun {i}:\n")
#      print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in results]))
     
#      #total reward calculation
#      sums = 0.0
#      for i in results:
#          sums += i[2]
#      print("Total Reward: ", sums)

#Task 3