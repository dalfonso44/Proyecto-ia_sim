from clases import *
import math
import random
from collections import defaultdict
import copy

class RandomPlayer(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)

    def play(self,mundo):
        actions=mundo.actions()
        l=random.choice(actions)
        eval("mundo."+l[:-1]+",True)")

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


class MC_D_Player(Jugador):
    def __init__(self, civilization):
        super().__init__(civilization)
        self.T=1.0
        self.G=1.0
        
        self.B=100
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

class Node():
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """
    def __init__(self,civilization,me,H,action='') -> None:
        self.state=civilization
        self.actions=civilization.actions()
        self.me=me
        self.H=H
        self.action=action
        
    def find_children(self):
        "All possible successors of this board state"
        children=[]
        for a in self.actions:
            c=copy.deepcopy(self.state)
            eval('c.'+a[:-1]+",True)")
            children.append(Node(c,self.me,self.H,a))
        return children

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        c=copy.deepcopy(self.state)
        a=random.choice(self.actions)
        eval('c.'+a[:-1]+",True)")
        return Node(c,self.me,self.H,a)

    def is_terminal(self):
        "Returns True if the node has no children"
        return self.state.turn==self.H

    def reward_1(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        payer_highscore=max(self.state.players,key =lambda x:x.puntuacion)
        return (payer_highscore.civilization==self.me)

    def reward_2(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        for i in self.state.players:
            if self.me==i.civilization:
                return 3*i.puntuacion-sum(j.puntuacion for j in self.state.players)

    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        payer_sort_score=sorted(self.state.players,key =lambda x:x.puntuacion)
        if self.me==payer_sort_score[-1].civilization:
            return payer_sort_score[-1].puntuacion-payer_sort_score[-2].puntuacion
        elif self.me==payer_sort_score[-2].civilization:
            return payer_sort_score[-2].puntuacion-payer_sort_score[-1].puntuacion
        else:
            return payer_sort_score[-3].puntuacion-payer_sort_score[-1].puntuacion

    def reward_3(self):
        for i in self.state.players:
            if self.me==i.civilization:
                return i.puntuacion
class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."
    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        while True:
            if node.is_terminal():
                reward = node.reward()
                return reward
            node = node.find_random_child()

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            
    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )
        return max(self.children[node], key=uct)


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