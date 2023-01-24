import numpy as np
#from world_ import *
from world.world_ import *
#from ..CSP.csp import CSP, backtracking_search
#from ..CSP.csp import UniversalDict
#from ..CSP.csp import AC3
import random
from world.clases import *
from CSP.csp import *



def different_values_constraint(A,a,B,b):
    """ A constraint saying two neighboring variables must differ in value"""
    return a!= b        

def in_zone_constraint():
    """"""   
    pass

def all_diff_constraint(*values):
    """Returns True if all values are different, False otherwise"""
    return len(values) is len(set(values))

def valid_world_constraint(*values):
    """Returns true if the is a valid world"""   
    pass 


    

def myMapConstraint(A,a,B,b):
    r = random.randint(0,1)
    if r == 0:return different_values_constraint(A,a,B,b) 
    return not different_values_constraint(A,a,B,b)  

# class CivilizationDict():
#     def __init__(self) -> None:
#         self.value = None
#         self.domain0 = [ocean(),mountain()]
#         self.domain1 = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits()]
#         self.domain2 = [mountain(),mine()]
#         self.domain3 = [beach(), ocean(), port(), fish(), farm()]

#     def __getitem__(self,key):
#         zone = key.zone
#         if zone is None:
#             self.value = self.domain0
#             return self.domain0 
#         elif zone == 'indian':
#             self.value = self.domain1
#             return self.domain1
#         elif zone == 'dessert':
#             self.value = self.domain2
#             return self.domain2    
#         elif zone == 'viking':
#             self.value = self.domain3
#             return self.domain3
               

#     def __repr__(self) -> str: return '{{Any: {0!r}}}'.format(self.value)             



class map:
    def __init__(self,players,fill = None,prob_city = None, prob_town = None, prob_mount = None, prod_fruit = None,prod_fish = None):
        self.size_x= self.size_y = len(players) * 2
        self.players = players
        self.nei = dict()
        self.map = np.ndarray((self.size_x,self.size_y),dtype=environment_things)
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
#                self.map[i,j] = environment_things(i,j)
                self.map[i,j] = environment_things()
        
        self.neighbors = self.parse_neighbors(self.map)   
        domain = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits()]
        self.domains = UniversalDict(domain)
        #self.domains2 = CivilizationDict()

        self.world = self.generation_world_csp()


    def parse_neighbors(self,map):
            def calculate_adyacents(map,x,y):
                dx = np.array([-1,1,0,0,-1,1,-1,1]) #up down left right diag izq diag der
                dy = np.array([0,0,-1,1,-1,-1,1,1])  
                adyacents = []      

                for i in range(len(dx)):
                    new_x = x + dx[i]
                    new_y = y + dy[i]
                    if (new_x >= 0 and new_y >= 0 and new_x < map.shape[0] and new_y < map.shape[1]):
                        adyacents.append(map[new_x,new_y])

                return adyacents    
            neighbors = dict()
            for i in range(map.shape[0]):
                for j in range(map.shape[1]):
                    neighbors[map[i,j]] = calculate_adyacents(map,i,j)
            return neighbors        
    
    
    def __str__(self):
        s=''
        for i in range(self.world.shape[0]):
            for j in range(self.world.shape[1]):
                if isinstance(self.world[i,j],ocean):
                    s +='O '
                elif isinstance(self.world[i,j],mountain):
                    s +='M '
                elif isinstance(self.world[i,j],fruits):
                    s +='F '
                elif isinstance(self.world[i,j],beach):
                    s +='B '
                elif isinstance(self.world[i,j],city):
                    s +='X '
                elif isinstance(self.world[i,j],town):
                    s +='T '
                elif isinstance(self.world[i,j],fish):
                    s +='P '
                else:
                    s+='L '
            s+='\n'
        return s

    def make_zones(self,world,players):
        def propagate_zone(x,y,world,civ):
            dr = [-1,-1,-1,0,0,1,1,1]
            dc = [-1,0,1,-1,1,-1,0,1]
            for i in range(len(dr)):
                new_x = x + dr[i]
                new_y = y + dc[i]
                if new_x > 0 and new_y > 0 and new_x < world.shape[0] and new_y < world.shape[1]:
                    world[new_x,new_y].zone = civ
            return world        
            
        cities_loc = []
        x = -1
        y = -1
        for player in players:
            civ = player.civilization
            c = city(civ,0,0)
            #c.zone = civ
            
            while (len(cities_loc) > 0 and (x,y) not in cities_loc):
                x = random.randint(0,world.shape[0] -1)
                y = random.randint(0,world.shape[1] - 1)
            c.row=x
            c.col=y
            world [x,y] = c
            world = propagate_zone(x,y,world,civ)
            cities_loc.append((x,y))
        return world    



    def generation_world_csp(self):
        world = np.full((self.size_x,self.size_y),environment_things(), dtype = environment_things)
        neighbors = self.parse_neighbors(world)
        world = self.make_zones(world,self.players) # reparte las ciudades de las civilizaciones
        
        #d = CivilizationDict()
        map_csp = CSP(list(self.neighbors.keys()), self.domains,self.neighbors, myMapConstraint)  
        assignments = backtracking_search(map_csp)
        for cell in assignments.keys():
            x = cell.x
            y = cell.y
            world[x,y] = assignments[cell]

        return world 


