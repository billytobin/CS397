#Billy Tobin
#main
import island
import agent


gamma = .99 #could not figure out where to implement this yet?
num_of_steps = 25



i1 = island.island(1,False,"Island 1")
i2 = island.island(2,False,"Island 2")
i3 = island.island(3,True,"Island 3")
i4 = island.island(4,False,"Island 4")
i5 = island.island(5,False,"Island 5")
i6 = island.island(6,False,"Island 6")
i7 = island.island(7,True,"Island 7")
i8 = island.island(8,False,"Island 8")
i9 = island.island(9,True,"Island 9")
i10 = island.island(10,False,"Island 10", True)

possActions = [1,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10]

portTrans=[[0.1,0,.1,.3,.1,0.1,.2,0,0,.1,0],
           [0.1,0,0,0.2,.3,0,0.1,0,.3,0,0],
           [0.1,0.1,0,0,0.1,0,.3,0,0,.3,0.1],
           [0.1,0.1,0,0.2,0,0,0,.1,.2,0.3,0],
           [0.1,0,0,.3,0,0,0.4,0.1,0,0,0.1],
           [0.1,0.1,0.3,.2,0.1,0.2,0,0.1,.1,0,0.1],
           [0.1,0,0.1,0,0.3,0,0.2,0,0,0.1,0.2],
           [0.1,0.1,.2,0,0.2,0,0,0.1,0,0.2,0.2],
           [0.1,.1,.3,.1,0,.1,0,0.1,.1,0,0.1],
           [0,0,0,0,0,0,0,0,0,0,0]]

#for i in range(len(portTrans)):
     #print(portTrans[i][i+1])


#Task 2

def run(steps):
    actions=[]
    curr = i1
    
    agent1 = agent.agent(curr.location)
    actions.append([["move"],[curr.name], [0]])
   
    # for i in range(steps):
    #     if curr.terminal == True:
    #         actions.append(" Reached Terminal State")
    #         return actions
    #     probs = portTrans[curr.location-1]
    for i in range(steps):
        nextMove, reward = agent1.move(portTrans[curr.location-1], possActions, curr.terminal)
        
        #if term state is reached
        if nextMove == None:
            actions.append([["Term"],[curr.location],[reward]])
            return actions
        
        
        #if we want to dig
        if nextMove == 1:
            reward = agent1.dig(curr.treasure)
            if curr.treasure:
                curr.treasure = False
            actions.append([["Dig"],[curr.location],[reward]])
        
        else: # if we move islands 

            curr = nextMove
            actions.append([["Move"],[curr.location],[reward]])
        #print(actions)
    return actions

#print(run(25)[0])
results= run(num_of_steps)
print(f"Run 1: \n{results}\n\n")

#Task 3

# for i in range(1,11):
#     results= run(num_of_steps)
#     print(f"Run {i}: \n{results[0]}, \nTotal Reward: {results[1]}\n\n")