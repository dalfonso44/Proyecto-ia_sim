
from collections import defaultdict
from distutils.command.build import build
from unittest import result
import numpy as np
from Game.Civilization import Civilization
from world.world_ import *
from CSP.csp import *
import random
from world.clases import *


def create_map(x,y,civ):
    m = map(x,y,civ)
    mapa = m.map
    assignments = backtracking_search(m)
    for assignment in assignments:
        value = assignments[assignment]
        x= assignment.x
        y = assignment.y
        mapa[x,y] = value
   
    return mapa

class UniversalDict:

    def __init__(self, value): self.value = value

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Any: {0!r}}}'.format(self.value)


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def myMapConstraint(A,a,B,b, values = None):
   r = random.randint(0,1)
   if r == 0:
        return different_values_constraint(A,a,B,b) 
   return not different_values_constraint(A,a,B,b)  



class map(CSP):
    def __init__(self, size_x, size_y, civilizations) -> None:
        self.map = np.ndarray((size_x,size_y),dtype=environment_things)
        self.map.fill(environment_things())

        cities = self.build_cities(civilizations) #-1 posiciones donde estan las ciudades

        variables = self.agroup_variables() # 0

        neighbors = self.agroup_neighbors(cities)

        domain = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits()]
        domains = UniversalDict(domain)
        super().__init__(neighbors.keys(), domains, neighbors, myMapConstraint)
       

    def nconflicts(self, var, val, assignment):
        return super().nconflicts(var, val, assignment)


    def assign(self, var, val, assignment):
        return super().assign(var, val, assignment)

    def unassign(self, var, assignment):
        return super().unassign(var, assignment)

    def record_conflict(self,assignment,var,val,delta):
        pass     

    def display(self, assignment):
        return super().display(assignment)       


    def build_cities(self, civilizations):
        cities = []
        def build_city(pos,cities,civ,i) :
            x,y = pos
            c =city(civilizations[i],x,y)
            self.map[x,y] = c
            cities.append(c)
            
        for i in range(len(civilizations)):
            x = random.randint(0,self.map.shape[0]-1)
            y = random.randint(0,self.map.shape[1]-1)
            pos = (x,y)
            build_city(pos, cities,civilizations,i)
        return cities    

    def agroup_variables(self):
        variables = []
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i,j] == 0:
                    variables.append((i,j))

        return variables          

    def agroup_neighbors(self,cities):
        # solo participan en la restriccion los alrededores de las ciudades
        def buscar_posiciones_aledanas(x,y,cantidad):
            dx = np.array([-1,1,0,0,-1,1,-1,1]) #up down left right diag izq diag der
            dy = np.array([0,0,-1,1,-1,-1,1,1])  
            result = []
            for i in range(len(dx)):
                if cantidad == 0: break
                new_x = dx[i] +x
                new_y= dy[i] + y
                if new_x > 0 and new_y > 0 and new_x < self.map.shape[0] and new_y < self.map.shape[0]:
                    if not isinstance(self.map[new_x,new_y], city) and not isinstance(self.map[new_x,new_y], town)  :
                        result.append(environment_things(new_x,new_y))
                        self.map[new_x,new_y] = town()
                        x = new_x
                        y = new_y
                        cantidad -=1 
            return result               

                
                

        neighbors = defaultdict(list)
        variables = []
        for cty in cities:
            x= cty.row
            y = cty.col

            # las posiciones del asentaminto
            setlement_pos = buscar_posiciones_aledanas(x,y,4)
            for p in setlement_pos:
                for q in setlement_pos:
                    if p!=q:
                        neighbors[p].append(q)
        return neighbors    

                    

            





    

   


