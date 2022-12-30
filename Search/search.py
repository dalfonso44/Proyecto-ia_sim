import heapq
import math
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations
from xml.etree.ElementTree import fromstring

# Problem
class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When you create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial = None, goal = None, **kwargs) -> None:
        self.__dict__.update(initial = initial, goal = goal, **kwargs)

    def acions(self,state): raise NotImplementedError
    def result(self,state,action): raise NotImplementedError
    def is_goal(self,state) : return state == self.goal
    def action_cost(self,s,a,s1) : return 1 # implementar segun el problema
    def h(self,node): return 0

    def __str__(self) -> str:
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)

#........................................................................................................

# Node    
class Node:
        """A node in a search tree"""
        def __init__(self, state, parent = None, action = None, path_cost = 0) -> None:
            self.__dict__.update(state = state, parent = parent, action = action, path_cost = path_cost)  

        def __repr__(self) -> str: return '<{}>'.format(self.state)
        def __len__(self): return 0 if self.parent is None else (1 + len(self.parent)) 
        def __lt__(self,other): return self.path_cost < other.path_cost                       
     
failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.     

def expand(problem, node):
    """Expand a node, generating the children nodes."""
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s,action)
        cost = node.path_cost + problem.action_cost(s,action,s1)
        yield Node(s1,node,action,cost)


def path_actions(node):
    """The secuence of actions to get this node"""
    if node.parent is None:
        return []

    return path_actions(node.parent) + [node.action]  

def path_states(node):
    """The sequence of states to get this node"""
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]
#........................................................................................................

# Queues
FIFOQueue  = deque

LIFOQueue = list

class PriorityQueue:
    """A queue in wich the item with minimum f(item) is always popped first."""
    def __init__(self, items = (), key = lambda x: x) -> None:
        self.key = key
        self.items = [] # heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self,item):
        pair = (self.key(item),item)
        heapq.heappush(self.items,pair)     

    def pop(self):
        """Pop and return the item with min f(item) value"""
        return heapq.heappop(self.items)[1]    

    def top(self): return self.items[0][1]   

    def __len__(self): return len(self.items)   


#........................................................................................................


# Search Algorithms

def best_first_search(problem, f):
    """Search nodes with minimun f(node) value first"""
    node = Node(problem.initial)
    frontier = PriorityQueue([node],key = f)
    reached = {problem.initial : node}
    while frontier :
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem,node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)

    return failure  

def best_first_tree_search(problem,f):
    """A version of best_first_search without the 'reached' table"""
    frontier = PriorityQueue([Node(problem.initial)], key =f)
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):return node
        for child in expand(problem,node):
            s = node.state
            if not is_cycle(child):
                frontier.add(child)

    return failure            

def is_cycle(node, k = 30):
    def find_cycle(ancestor,k):
        return (ancestor is not None and k > 0 and 
        (ancestor.state == node.state or find_cycle(ancestor.parent,k-1)))

    return find_cycle(node.parent,k)    





#........................................................................................................