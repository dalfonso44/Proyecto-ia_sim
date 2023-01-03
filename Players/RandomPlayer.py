import random
from Players.Player import *


class RandomPlayer(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)

    def play(self,mundo):
        actions=mundo.actions()
        l=random.choice(actions)
        eval("mundo."+l[:-1]+",True)")
