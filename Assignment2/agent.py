#Billy Tobin
#basic agent class

class agent():
    def __init__(self):
        self.reward = 0
        self.currLoc = 0
        self.treasureFound = 0



    #move
    #brings in the array at the certain island
    def move(self, possMoves, isTerm):
        #bring in array of moves and based on probablity, return the island it should go to
        if not isTerm:
            if self.treasureFound == 3:
                self.reward +=15
            return -1
        else:
            pass
        


    #super simple dig function, only need it to make agent moves clear and undersatndable
    def dig(self, treasure):

        if treasure:
            self.treasureFound += 1
            self.reward += 2
        
