from Players.Player import *
from Players.MCTS import *
from Players.Node import *


class MCTSPlayer(Jugador):
    def __init__(self, civilization,B=100,H=5):
        super().__init__(civilization)
        self.B=B
        self.H=H

    def play(self,mundo):
        acciones=[]
        tree = MCTS()
        board = Node(mundo,self.civilization,min(self.H+mundo.turn,mundo.turns))
        while True:
            if len(board.actions)==1:
                acciones.append("termina(0)")
            if len(acciones)>1 and acciones[-1]=="termina(0)":
                for l in acciones:
                    eval("mundo."+l[:-1]+",True)")
                return
            for _ in range(self.B):
                tree.do_rollout(board)
            board=tree.choose(board)
            acciones.append(board.action)