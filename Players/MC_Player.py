import random
from Players.Player import *
import math

class MC_Player(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)
        self.T=1.0
        self.G=3.0
    
    def play(self,mundo):
        actions=mundo.actions()
        x=random.random()
        acumulativa=[0]
        for i in range(len(actions)):
            acumulativa.append(acumulativa[i]+math.exp(self.T*(eval('mundo.'+actions[i])-self.G)))
        l=next(actions[i] for i in range(len(actions)) if x*acumulativa[-1]<=acumulativa[i+1])    
        eval("mundo."+l[:-1]+",True)")
