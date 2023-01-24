import numpy as np

from world_ import *
from collections import defaultdict
import random
from clases import *
from csp import *



def different_values_constraint(A,a,B,b):
    """ A constraint saying two neighboring variables must differ in value"""
    return a!= b        



def all_diff_constraint(*values):
    """Returns True if all values are different, False otherwise"""
    return len(values) is len(set(values))


def myMapConstraint(A,a,B,b):
    r = random.randint(0,1)
    if r == 0:return different_values_constraint(A,a,B,b) 
    return not different_values_constraint(A,a,B,b)  




class map(CSP):
    def __init__(self,size_x, size_y,civilizations,fill = None,prob_city = None, prob_town = None, prob_mount = None, prod_fruit = None,prod_fish = None):
        self.size_x= size_x
        self.size_y = size_y
        self.civilizations = civilizations

        self.map = np.ndarray((size_x,size_y), dtype = environment_things)
        self.map.fill(environment_things)

        cities = self.build_cities(civilizations)

        neighbors = self.agroup_neighbors(cities)

        domain = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits(), planting()]
        #domain = [2,3,4,5,6,7,8,9,10,11,12]
        domains = UniversalDict(domain)

        m =CSP(list(neighbors.keys()), domains,neighbors, myMapConstraint)
        assignments = backtracking_search(m)
        for assignmnent in assignments:
            value = assignments[assignmnent]
            x,y = assignmnent
            self.map[x,y] = value



        


    
    def __str__(self):
        s=''
        for i in range(self.size_x):
            for j in range(self.size_y):
                if isinstance(self.map[i,j],environment_things):
                    s+="_"

                if isinstance(self.map[i,j],ocean):
                    s +='O'
                elif isinstance(self.map[i,j],mine):
                    s+='K'
                elif isinstance(self.map[i,j],fruits):
                    s +='F'
                elif isinstance(self.map[i,j],city):
                    s +='X'
                elif isinstance(self.map[i,j],town):
                    s +='T'
                elif isinstance(self.map[i,j],fish):
                    s +='P'
                elif isinstance(self.map[i,j],farm):
                    s +='G'
                elif isinstance(self.map[i,j],planting):
                    s+='Y'
                elif isinstance(self.map[i,j], port):
                    s+='R'
                elif isinstance(self.map[i,j],plain):
                    s+='L'
                elif isinstance(self.map[i,j],mountain):
                    s +='M'
                elif isinstance(self.map[i,j],beach):
                    s +='B'

                    
                

                if self.map[i,j].soldado == None:
                    s+='_ '
                elif isinstance(self.map[i,j].soldado,Guerrero):
                    s+='g '
                elif isinstance(self.map[i,j].soldado,Defensor):
                    s+='d '
                elif isinstance(self.map[i,j].soldado,Espadachin):
                    s+='e '
            s+='\n'
        return s

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

   


    def agroup_neighbors(self,cities):
        # solo participan en la restriccion los alrededores de las ciudades
        def buscar_posiciones_aledanas(x,y,cantidad):
            domain = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits(), planting()]
            dx = np.array([-1,1,0,0,-1,1,-1,1]) #up down left right diag izq diag der
            dy = np.array([0,0,-1,1,-1,-1,1,1])  
            result = []
            for i in range(len(dx)):
                if cantidad == 0: break
                new_x = dx[i] +x
                new_y= dy[i] + y
                if new_x > 0 and new_y > 0 and new_x < self.map.shape[0] and new_y < self.map.shape[0]:
                    if not isinstance(self.map[new_x, new_y], city) and not isinstance(self.map[new_x,new_y], ocean) :
                        result.append((new_x,new_y))
                        self.map[new_x,new_y] = ocean # ya esta marcado
                        x = new_x
                        y = new_y
                        cantidad -=1 
            return result               

                
                

        neighbors = defaultdict(list)
        variables = []
        for cty in cities:
            x = cty.row
            y = cty.col
            # las posiciones del asentaminto
            r = random.randint(1,5)
            setlement_pos = buscar_posiciones_aledanas(x,y,r)
            for p in setlement_pos:
                for q in setlement_pos:
                    if p!=q:
                        neighbors[p].append(q)
        return neighbors        



    # def generation_world_csp(self):
    #     world = np.full((self.size_x,self.size_y),environment_things(), dtype = environment_things)
    #     neighbors = self.parse_neighbors(world)
    #     world = self.make_zones(world,self.players) # reparte las ciudades de las civilizaciones
        
    #     #d = CivilizationDict()
    #     map_csp = CSP(list(self.neighbors.keys()), self.domains,self.neighbors, myMapConstraint)  
    #     assignments = backtracking_search(map_csp)
    #     for cell in assignments.keys():
    #         x = cell.x
    #         y = cell.y
    #         world[x,y] = assignments[cell]

    #     return world 


# probando el mapa

mapa = map(10,10,['viking', 'indians', 'mexicans'])



print(mapa)


