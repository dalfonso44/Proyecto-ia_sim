
import numpy as np
from world_ import *
from cps import CSP, backtracking_search
from cps import UniversalDict
from cps import AC3
import random


class environment_things():
    def __init__(self,cord_x = None,cord_y = None):
        self.soldado = None  
        self.name = "thing"
        self.x = cord_x
        self.y = cord_y     
        self.zone = None
        self.poblacion = 1
        self.costo =2
    def __str__(self) -> str:
        return self.name    

class dessert(environment_things):
    def __init__(self, cord_x=None, cord_y=None):
        super().__init__(cord_x, cord_y)

class beach(environment_things):
    def __init__(self):
        super().__init__()
        self.name = "beach"
    
class ocean(environment_things):
    def __init__(self) -> None:
        super().__init__()
  
class mountain(environment_things):
    def __init__(self):
        super().__init__()
        self.name = "mountain"

class plain(environment_things):
    def __init__(self):
        super().__init__()
        self.name = "plain"

class port(beach):
    def __init__(self):
        super().__init__()
        self.name = "port"
        self.poblacion = 2
        self.costo = 10

class fish(beach):
    def __init__(self):
        super().__init__()
        self.name = "fish"
        self.poblacion = 1

class mine(mountain):
    def __init__(self):
        super().__init__()
        self.name = "mine"
        self.poblacion = 2
        self.costo = 5

class fruits(plain):
    def __init__(self):
        super().__init__()
        self.name = "fruits"

class farm(plain):
    def __init__(self):
        super().__init__()
        self.name = "farm"
        self.poblacion = 2
        self.costo = 5

class planting(plain):
    def __init__(self):
        super().__init__()
        self.name = "planting"
        self.poblacion = 1
        self.costo = 2

class town(environment_things):
    def __init__(self):
        super().__init__()
        self.name = "town"

class city(plain):
    def __init__(self, civilization,row = None,col = None,poblacion=0):
        super().__init__()
        self.name = "city"
        self.poblacion= poblacion
        self.nivel=0
        self.zone = civilization
        self.row = row 
        self.col = col
        self.history = [civilization]

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

class CivilizationDict():
    def __init__(self) -> None:
        self.value = None
        self.domain0 = [ocean(),mountain()]
        self.domain1 = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits()]
        self.domain2 = [dessert(), mountain(),mine()]
        self.domain3 = [beach(), ocean(), port(), fish(), farm()]

    def __getitem__(self,key):
        zone = key.zone
        if zone is None:
            self.value = self.domain0
            return self.domain0 
        elif zone == 'indian':
            self.value = self.domain1
            return self.domain1
        elif zone == 'dessert':
            self.value = self.domain2
            return self.domain2    
        elif zone == 'viking':
            self.value = self.domain3
            return self.domain3
               

    def __repr__(self) -> str: return '{{Any: {0!r}}}'.format(self.value)             



class map:
    def __init__(self,players,fill = None,prob_city = None, prob_town = None, prob_mount = None, prod_fruit = None,prod_fish = None):
        self.size_x= self.size_y = len(players) * 2
        self.players = players
        self.nei = dict()
        self.map = np.ndarray((self.size_x,self.size_y),dtype=environment_things)
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                self.map[i,j] = environment_things(i,j)
        
        self.neighbors = self.parse_neighbors(self.map)   
        domain = [town(), beach(), ocean(),mountain(),plain(),port(),fish(),mine(),farm(),fruits()]
        self.domains = UniversalDict(domain)
        self.domains2 = CivilizationDict()

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
            c = city(civ)
            #c.zone = civ
            
            while (len(cities_loc) > 0 and (x,y) not in cities_loc):
                x = random.randint(0,world.shape[0] -1)
                y = random.randint(0,world.shape[1] - 1)
            world [x,y] = c
            world = propagate_zone(x,y,world,civ)
            cities_loc.append((x,y))
        return world    



    def generation_world_csp(self):
        world = np.full((self.size_x,self.size_y),environment_things(), dtype = environment_things)
        neighbors = self.parse_neighbors(world)
        world = self.make_zones(world,self.players) # reparte las ciudades de las civilizaciones
        
        d = CivilizationDict()
        map_csp = CSP(list(self.neighbors.keys()), self.domains,self.neighbors, myMapConstraint)  
        assignments = backtracking_search(map_csp)
        for cell in assignments.keys():
            x = cell.x
            y = cell.y
            world[x,y] = assignments[cell]

        return world    


    def generation_world(self, size, fill, prob_city, prob_town, prob_mount, prod_fruit,prod_fish):
        mapa = generacion_de_mapa_aleatorio(size[0],size[1],fill)
        automata_celular_moore(mapa,1)
        generacion_de_playa(mapa)
        posiciones=generacion_de_ciudades_capitales(mapa,prob_city)
        generacion_de_poblados(mapa, prob_town,posiciones)
        generacion_de_montannas(mapa, prob_mount)
        generacion_de_frutos(mapa,prod_fruit)
        generacion_de_peces(mapa,prod_fish)
        world = np.full((mapa.shape[0],mapa.shape[1]),ocean(), dtype = environment_things)
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                if mapa[i,j]==1:
                    world[i,j]=plain()
                elif mapa[i,j]==-1:
                    world[i,j]=beach()
                elif mapa[i,j]==2:
                    world[i,j]=city()
                elif mapa[i,j]==3:
                    world[i,j]=town()
                elif mapa[i,j]==4:
                    world[i,j]=mountain()
                elif mapa[i,j]==5:
                    world[i,j]=fruits()
                elif mapa[i,j]==6:
                    world[i,j]=fish()
        return world

   


class Habilidad:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.desbloqueada = False

class Soldado:
    def __init__(self):
        self.ataque = 0
        self.contraataque = 0
        self.vida = 0
        self.civilizacion=None
    
    def recibe_ataque(self,atacante, mapa):
        self.vida -= atacante.ataque
        if self.vida>0:
            atacante.vida -= self.defensa
        else:
            mapa[atacante.row, atacante.col].ocupado(False, None)
            mapa[self.row, self.col].ocupado(True, atacante)

class Guerrero(Soldado):
    def __init__(self):
        super().__init__(self)
        self.vida = 10
        self.ataque = 5
        self.contraataque = 5

class Espadachin(Soldado):
    def __init__(self):
        super().__init__(self)
        self.vida = 10
        self.ataque = 8
        self.contraataque = 5

class Defensor(Soldado):
    def __init__(self):
        super().__init__(self)
        self.ataque = 1
        self.vida = 15
        self.contraataque = 8

class Jugador:
    def __init__(self, name, civilization):
        self.soldados = []
        self.presupuesto = 3
        self.habilidades_desarrolladas=[]
        self.ciudades=[]
        self.civilization = civilization



    def tropas(self):
        pass

    def invertir(self):
        pass
    
    def construir(self):
        pass
    
    def construir_puerto(self):
        pass

    def construir_mina(self):
        pass

    def construir_granja(self):
        pass
    
    def pescar(self):
        pass
    
    def recolectar_frutos(self):
        pass

    def entrenar(self):
        pass
    
    def desarrollar_habilidades(self):
        pass

    def movimiento(self):
        pass
    
    def atacar(self):
        pass

    def tomar_ciudad(self):
        pass

