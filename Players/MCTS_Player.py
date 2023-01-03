from Players.Player import *
from Players.MCTS import *
from Players.Node import *


class MCTSPlayer(Jugador):
    def __init__(self, civilization,B=50,H=2):
        super().__init__(civilization)
        self.B=B
        self.H=H

    def play(self,mundo):
        if len(mundo.actions())==1:
            mundo.termina(0,True)
            return
        tree = MCTS()
        board = Node(mundo,self.civilization,min(self.H+mundo.turn,mundo.turns))
        for _ in range(self.B):
            tree.do_rollout(board)
        l=tree.choose(board).action
        print(l)
        eval("mundo."+l[:-1]+",True)")