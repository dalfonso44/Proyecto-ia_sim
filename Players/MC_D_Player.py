import math
import random
from Players.Player import *

class MC_D_Player(Jugador):
    def __init__(self, civilization, T=1.0, G=1.0, B=100, D=2):
        super().__init__(civilization)
        self.T=T
        self.G=G
        
        self.B=B
        self.D=D
    
    def play_complex(self,action,mundo,d,P=0):
        if d==0:
            return math.exp(self.T*(P+eval('mundo.'+action)-self.G*self.D))
        P+=eval("mundo."+action[:-1]+",True)")
        actions=mundo.actions()
        actionsB=[]
        for _ in range(self.B):
            actionsB.append(random.choice(actions))
            actions.remove(actionsB[-1])
            if not len(actions):
                break
        prob= sum(self.play_complex(a,mundo,d-1,P) for a in actionsB)
        eval("mundo."+action[:-1]+",True,True)")
        return prob

    def play(self,mundo):
        actions=mundo.actions()
        
        mundo.deads=[]
        x=random.random()
        actionsB=[]
        for _ in range(self.B):
            actionsB.append(random.choice(actions))
            actions.remove(actionsB[-1])
            if not len(actions):
                break
        prob=[self.play_complex(a,mundo,self.D) for a in actionsB]
        x*=sum(prob)
        acumulativa=0
        l=""
        for i in range(len(actionsB)):
            acumulativa+=prob[i]
            if x<=acumulativa:
                l=actionsB[i]
        if l=="":
            l=actionsB[-1]        
        eval("mundo."+l[:-1]+",True)")
