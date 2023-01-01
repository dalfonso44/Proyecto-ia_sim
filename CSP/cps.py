
from itertools import count
from operator import eq, neg
from sortedcontainers import SortedSet

from Search import search


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)

class CSP(search.Problem):
    """This class describes a finite-domain Constraint Satisfaction Problem
    A CSP is specified by the following inputs:
        - variables : A list of variables; each is atomic
        - domains : A dict { var : [posible_values]}
        - neighbors : A dict {var: [var_2,...,var_n]} if var and var_i participate in the same constraint
        - constainst : A function f(A,A,B,b) that return true if neighbors A, B 
        satisfy the constraint when A=a, B=b
    """
    def __init__(self,variables,domains,neighbors,constraints) -> None:
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: value} to assignment; Discard the old value if any"""
        assignment[var] = val
        self.nassigns+=1

    def unassign(self,var,assignment) :
        """Remove {var: val} from assignment
        Do not use this for changing a variable to a new value"""
        if var in assignment:
            del assignment[var]

    def nconflicts(self,var,val,assignment):
        """Returns the number of conflicts var = val has with other variables"""
        def conflict(var2):
            return var2 in assignment and not self.constraints(var,val,var2,assignment[var2])
        return count(conflict(v) for v in self.neighbors[var])            

    def acions(self, state):
        """Returns a list pf applicable actions : non conflicting assignments to an unassigned variable"""
        if len(state) == len(self.variables): return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var,val) for val in self.domains[var] if self.nconflicts(var,val,assignment) == 0]

    def result(self, state, action):
        """Performs an action and return the new state"""
        (var,val) = action
        return state + ((var,val),)

    def is_goal(self, state):
        """The goal test is to assign all variables, with all constraints satisfied"""
        assignment = dict(state)
        return (len(assignment) == len(self.variables) and all(self.nconflicts(variables, assignment[variables], assignment) == 0 for variables in self.variables))

    # for constraint propagation
    def support_prunning(self):
        """Make sure we can prune values from domains."""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def prune(self,var,value,removals):
        """Rule out var = value"""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var,value))            

    def h(self, node):
        pass          

def no_arc_heuristic(csp, queue):  return queue    

def dom_j_up(csp, queue):
    return SortedSet(queue, key = lambda t: neg(len(csp.curr_domains[t[1]])))

def AC3(csp, queue = None, removals = None, arc_heuristic = dom_j_up):
    if queue is None:
        queue = {(Xi,Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}

    csp.support_prunning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue :
        (Xi,Xj) = queue.pop()
        revised,checks = revise(csp,Xi,Xj,removals,checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk,Xi))
    return True,checks # Csp is satisfiable       

def revise(csp,Xi,Xj,removals, checks = 0):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi,x,Xj,y):
                conflict = False
            checks += 1
            if not conflict:
                break   
        if conflict :
            csp.prune(Xi,x,removals)
            revised = True
    return revised, checks      


class UniversalDict:
    """Returns the same value for any key"""
    def __init__(self, value) -> None:
        self.value = value

    def __getitem__(self,key): return self.value

    def __repr__(self) -> str: return '{{Any: {0!r}}}'.format(self.value)
        


