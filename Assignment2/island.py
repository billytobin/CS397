#Billy Tobin
#Island Objects

#Should have location (int), treasure (bool), and Name (str)

class island:
    def __init__(self, locNum, treasure, name, terminal=False):
        self.location = locNum
        self.treasure = treasure
        self.name = name
        self.terminal = terminal


        