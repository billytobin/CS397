#Billy Tobin
#basic agent class
import random


class agent():
    def __init__(self, location, vpi):
        self.reward = 0
        self.currLoc = location
        self.vpi = vpi



    #move
    #brings in the array at the certain island
    def move(self, possMoves,actions, isTerm):
        #defining move set
        #moves = range(len(possMoves)-1)
        #bring in array of moves and based on probablity, return the island it should go to
        #count=1
        #temp=0
        
        if isTerm:
            #print(possMoves)
            #if self.treasureFound == 3:
            #    temp+=15
             #   self.reward +=15
            return None, 0
        else:
            #print(len(actions), len(possMoves))
           # print(actions, possMoves)
            #nextmove = random.choices(actions, possMoves)        
            loc = 0
            high = 0
            for i in range(len(possMoves)):
                if possMoves[i] != 0:
                    if self.vpi[i]>high:
                        high = self.vpi[i]
                        loc = actions[i]

            self.reward += high
            return loc, high


             
             
           # print(nextmove)
            #if nextmove[0] == 0:
             #   temp+=1
              #  self.reward +=1
             #return nextmove[0], nextmove.treasure
        


    #super simple dig function, really only here it to make agent moves a bit more clear and undersatndable
    def dig(self, treasure):
        if treasure:
            self.treasureFound += 1
            self.reward += 2
            return 2
        return 0
        
        
