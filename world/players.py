from clases import *
import math
import random

class RandomPlayer(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)

    def play(self,actions,mundo):
        return random.choice(actions)

class MC_Player(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)
        self.T=1.0
        self.G=3.0
    
    def play(self,actions,mundo):
        x=random.random()
        acumulativa=[0]
        for i in range(len(actions)):
            acumulativa.append(acumulativa[i]+math.exp(self.T*(eval('mundo.'+actions[i])-self.G)))

        return next(actions[i] for i in range(len(actions)) if x*acumulativa[-1]<=acumulativa[i+1])    


class MC_D_Player(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)
        self.T=1.0
        self.G=1.0
        
        self.B=10000
        self.D=2
    
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

    def play(self,actions,mundo):
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
        for i in range(len(actionsB)):
            acumulativa+=prob[i]
            if x<=acumulativa:
                return actionsB[i]
        return actionsB[-1]        



class MCTSPlayer(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)
        self.T=1.0
        self.G=1.0
        
        self.B=10000
        self.D=2

    def play_game(self,turns,mundo):
        for i in range(turns):
            for j in range(len(mundo.players)):
                mundo.actual_player = j
                while(True):
                    l=mundo.players[j].play(mundo.actions(),mundo)
                    if l=='termina(0)':
                        break
                    eval("self."+l[:-1]+",True)")
            for c in mundo.ciudades:
                for j in mundo.players:
                    if c.civilization == j.civilization:
                        j.presupuesto += c.poblacion//mundo.intereses
            for j in mundo.players:
                for s in j.soldados:
                    s.energy=True
            if i%3==2:
                for j in mundo.players:
                    for hab in j.habilidades:
                        for h in hab:
                            h.precio+=1

    
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

    def play(self,actions,mundo):
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
        for i in range(len(actionsB)):
            acumulativa+=prob[i]
            if x<=acumulativa:
                return actionsB[i]
        return actionsB[-1]        
