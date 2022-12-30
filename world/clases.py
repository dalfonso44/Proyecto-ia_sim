import numpy as np
from world_ import *



class environment_things():
    def __init__(self):
        self.soldado = None       

class beach(environment_things):
    def __init__(self):
        super().__init__()
    
class ocean(environment_things):
    def __init__(self) -> None:
        super().__init__()
  
class mountain(environment_things):
    def __init__(self):
        super().__init__()

class plain(environment_things):
    def __init__(self):
        super().__init__()

class port(beach):
    def __init__(self):
        super().__init__()

class fish(beach):
    def __init__(self):
        super().__init__()

class mine(mountain):
    def __init__(self):
        super().__init__()

class fruits(plain):
    def __init__(self):
        super().__init__()

class farm(plain):
    def __init__(self):
        super().__init__()

class planting(plain):
    def __init__(self):
        super().__init__()

class town(environment_things):
    def __init__(self):
        super().__init__()

class city(plain):
    def __init__(self):
        super().__init__()
        self.poblacion=0
        self.nivel=0

class map:
    def __init__(self, size_x, size_y,fill,prob_city, prob_town, prob_mount, prod_fruit,prod_fish):
        self.size_x=size_x
        self.size_y=size_y
        self.map = self.generation_world((size_x,size_y),fill,prob_city, prob_town, prob_mount, prod_fruit,prod_fish)
    
    def __str__(self):
        s=''
        for i in range(self.size_x):
            for j in range(self.size_y):
                if isinstance(self.map[i,j],ocean):
                    s +='O '
                elif isinstance(self.map[i,j],mountain):
                    s +='M '
                elif isinstance(self.map[i,j],fruits):
                    s +='F '
                elif isinstance(self.map[i,j],beach):
                    s +='B '
                elif isinstance(self.map[i,j],city):
                    s +='X '
                elif isinstance(self.map[i,j],town):
                    s +='T '
                elif isinstance(self.map[i,j],fish):
                    s +='P '
                else:
                    s+='L '
            s+='\n'
        return s

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
    def __init__(self, name):
        self.soldados = []
        self.presupuesto = 3
        self.habilidades_desarrolladas=[]
        self.ciudades=[]


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

