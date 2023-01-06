import random
import copy

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
        if self.is_terminal():
            return []
        children=[]
        for a in self.actions:
            c=copy.deepcopy(self.state)
            eval('c.'+a[:-1]+",True)")
            children.append(Node(c,self.me,self.H,a))
        return children

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        if self.is_terminal():
            return None
        c=copy.deepcopy(self.state)
        a=random.choice(self.actions)
        eval('c.'+a[:-1]+",True)")
        return Node(c,self.me,self.H,a)

    def find_random_child_new(self):
        "Random successor of this board state (for more efficient simulation)"
        a=random.choice(self.actions)
        eval('self.state.'+a[:-1]+",True)")
        self.action=a
        self.actions=self.state.actions()

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
