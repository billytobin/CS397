#Billy Tobin
#basic agent class
import random

class agent():
    def __init__(self, location):
        self.reward = 0
        self.currLoc = location
        self.treasureFound = 0



    #move
    #brings in the array at the certain island
    def move(self, possMoves, actions, isTerm):
        #defining move set
        #moves = range(len(possMoves)-1)
        #bring in array of moves and based on probablity, return the island it should go to
        self.reward-=1
        temp = -1
        if isTerm:
            #print(possMoves)
            self.reward+=5
            temp+=5
            if self.treasureFound == 3:
                temp+=15
                self.reward +=15
            return None, temp
        else:
            #print(len(actions), len(possMoves))
           # print(actions, possMoves)
            nextmove = random.choices(actions, possMoves)
           # print(nextmove)
            if nextmove[0] == 0:
                temp+=1
                self.reward +=1
            return nextmove[0], temp
        


    #super simple dig function, really only here it to make agent moves a bit more clear and undersatndable
    def dig(self, treasure):
        if treasure:
            self.treasureFound += 1
            self.reward += 2
            return 2
        return 0
        
        
