import random
import numpy as np

class environment_things():
    pass

class beach(environment_things):
    pass
    
class ocean(environment_things):
    def __init__(self) -> None:
        super().__init__()
    pass
  
class mountain(environment_things):
   pass

class plain(environment_things):
    pass

class port(beach):
    pass

class fish(beach):
    pass

class mine(mountain):
    pass

class fruits(plain):
    pass

class farm(plain):
    pass

class planting(plain):
    pass

class town(environment_things):
    pass

class city(plain):
    pass

class map:
    def __init__(self, size_x, size_y,fill):
        self.size_x=size_x
        self.size_y=size_y
        self.map = generation_world((size_x,size_y),fill)
    
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


dr = [-1,-1,-1,0,0,1,1,1]
dc = [-1,0,1,-1,1,-1,0,1]

def generacion_de_mapa_aleatorio(tamanno_x, tamanno_y, relleno):
    mapa = np.zeros((tamanno_x,tamanno_y))
    for i in range(tamanno_x):
        for j in range(tamanno_y):
            mapa[i,j] = 1 if random.random()<relleno else 0
    return mapa

def cantidad_adyacentes(mapa,pos_x,pos_y):
    cant=0
    for i,j in zip(dr,dc):
        if pos_x+i>=0 and pos_x+i<mapa.shape[0] and pos_y+j>=0 and pos_y+j<mapa.shape[1]:
            cant += mapa[pos_x+i,pos_y+j]
    return cant

def automata_celular_moore(mapa,generaciones):
    for i in range(generaciones):
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                cant = cantidad_adyacentes(mapa,i,j)
                if cant>4:
                    mapa[i,j]=1
                elif cant<4:
                    mapa[i,j]=0

def generacion_de_playa(mapa):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            cant = cantidad_adyacentes(mapa,i,j)
            if cant>0 and (not mapa[i,j]):
                mapa[i,j]=-1
   
def comprobacion_relleno(mapa, pos_x,pos_y, rellenar,value):
    for n,m in zip(dr,dc):
        if n+pos_x>=0 and n+pos_x<mapa.shape[0] and m+pos_y>=0 and m+pos_y<mapa.shape[1]:
            if not rellenar and mapa[n+pos_x,m+pos_y]==2:
                return False
            elif rellenar:
                mapa[n+pos_x,m+pos_y]=value
    return True

def generacion_de_ciudades_capitales(mapa, prob, cant_ciudades=3):
    while(cant_ciudades>0):
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                if cant_ciudades>0 and mapa[i,j]==1 and random.random() > prob:
                        cant_ciudades-=1
                        mapa[i,j]=2
                        comprobacion_relleno(mapa,i,j,True, 2)

def generacion_de_poblados(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]==1 and random.random() > prob:
                mapa[i,j]=3
                comprobacion_relleno(mapa,i,j,True, 3)
    
def generacion_de_montannas(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]!=0 and mapa[i,j] !=-1 and random.random() > prob:
                mapa[i,j]=4
    
def generacion_de_frutos(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]!=0 and mapa[i,j] !=-1 and random.random() > prob:
               mapa[i,j]=5

def generacion_de_peces(mapa,prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j] ==-1 and random.random() > prob:
               mapa[i,j]=6

def generation_world(size, fill, prob_city=0.99, prob_town=0.8, prob_mount=0.8, prod_fruit=0.8,prod_fish=0.5):
    mapa = generacion_de_mapa_aleatorio(size[0],size[1],fill)
    automata_celular_moore(mapa,1)
    generacion_de_playa(mapa)
    generacion_de_ciudades_capitales(mapa,prob_city)
    generacion_de_poblados(mapa, prob_town)
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

