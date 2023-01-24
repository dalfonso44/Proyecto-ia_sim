import numpy as np
from world.world_ import *



class environment_things():
    def __init__(self, x = None,y = None):
        self.soldado = None       
        self.x = x
        self.y = y

class beach(environment_things):
    def __init__(self):
        super().__init__()
        self.poblacion=1
        self.costo=2
    
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
        self.poblacion=2
        self.costo=10

class fish(beach):
    def __init__(self):
        super().__init__()
        self.poblacion=1

class mine(mountain):
    def __init__(self):
        super().__init__()
        self.poblacion=2
        self.costo=5

class fruits(plain):
    def __init__(self):
        super().__init__()
       

class farm(plain):
    def __init__(self):
        super().__init__()
        self.poblacion=2
        self.costo=5

class planting(plain):
    def __init__(self):
        super().__init__()
        self.poblacion=1
        self.costo=2

class town(environment_things):
    def __init__(self):
        super().__init__()

class city(plain):
    def __init__(self,civilization,row,col,poblacion=0):
        super().__init__()
        self.poblacion=poblacion
        self.nivel=0
        self.civilization=civilization
        self.row=row
        self.col=col
        self.history=[civilization]

<<<<<<< HEAD
class map:
    def __init__(self, size_x, size_y,fill, prob_mount=1/3, prod_fruit=1/2,prod_fish=2/3):
        self.size_x=size_x
        self.size_y=size_y
        self.map = self.generation_world((size_x,size_y),fill, prob_mount, prod_fruit,prod_fish)
=======
# class map:
#     def __init__(self, size_x, size_y,fill,prob_city, prob_town, prob_mount, prod_fruit,prod_fish):
#         self.size_x=size_x
#         self.size_y=size_y
#         self.map = self.generation_world((size_x,size_y),fill,prob_city, prob_town, prob_mount, prod_fruit,prod_fish)
>>>>>>> a9d482ba7803714e8ef28ceb3c981f9c02f642a4
    
#     def __str__(self):
#         s=''
#         for i in range(self.size_x):
#             for j in range(self.size_y):
#                 if isinstance(self.map[i,j],ocean):
#                     s +='O'
#                 elif isinstance(self.map[i,j],mine):
#                     s+='K'
#                 elif isinstance(self.map[i,j],fruits):
#                     s +='F'
#                 elif isinstance(self.map[i,j],city):
#                     s +='X'
#                 elif isinstance(self.map[i,j],town):
#                     s +='T'
#                 elif isinstance(self.map[i,j],fish):
#                     s +='P'
#                 elif isinstance(self.map[i,j],farm):
#                     s +='G'
#                 elif isinstance(self.map[i,j],planting):
#                     s+='Y'
#                 elif isinstance(self.map[i,j], port):
#                     s+='R'
#                 elif isinstance(self.map[i,j],plain):
#                     s+='L'
#                 elif isinstance(self.map[i,j],mountain):
#                     s +='M'
#                 elif isinstance(self.map[i,j],beach):
#                     s +='B'
                

#                 if self.map[i,j].soldado == None:
#                     s+='_ '
#                 elif isinstance(self.map[i,j].soldado,Guerrero):
#                     s+='g '
#                 elif isinstance(self.map[i,j].soldado,Defensor):
#                     s+='d '
#                 elif isinstance(self.map[i,j].soldado,Espadachin):
#                     s+='e '
#             s+='\n'
#         return s

<<<<<<< HEAD
    def civilization_submap(sefl,id):
        pass

    def generation_world(self, size, fill, prob_mount, prod_fruit,prod_fish):
        posiciones=[]
        while not posiciones:
            mapa = generacion_de_mapa_aleatorio(size[0],size[1],fill)
            automata_celular_moore(mapa,1)
            generacion_de_playa(mapa)
            posiciones=generacion_de_ciudades_capitales(mapa)

        generacion_de_poblados(mapa,posiciones)
        generacion_de_montannas(mapa, prob_mount)
        generacion_de_frutos(mapa,prod_fruit)
        generacion_de_peces(mapa,prod_fish)
        world = np.full((mapa.shape[0],mapa.shape[1]),None, dtype = environment_things)
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                if mapa[i,j]==1:
                    world[i,j]=plain()
                elif mapa[i,j]==-1:
                    world[i,j]=beach()
                elif mapa[i,j]==2:
                    world[i,j]=city("",i,j)
                elif mapa[i,j]==3:
                    world[i,j]=town()
                elif mapa[i,j]==4:
                    world[i,j]=mountain()
                elif mapa[i,j]==5:
                    world[i,j]=fruits()
                elif mapa[i,j]==6:
                    world[i,j]=fish()
                else:
                    world[i,j]=ocean()
        return world
=======
#     def generation_world(self, size, fill, prob_city, prob_town, prob_mount, prod_fruit,prod_fish):
#         mapa = generacion_de_mapa_aleatorio(size[0],size[1],fill)
#         automata_celular_moore(mapa,1)
#         generacion_de_playa(mapa)
#         posiciones=generacion_de_ciudades_capitales(mapa,prob_city)
#         generacion_de_poblados(mapa, prob_town,posiciones)
#         generacion_de_montannas(mapa, prob_mount)
#         generacion_de_frutos(mapa,prod_fruit)
#         generacion_de_peces(mapa,prod_fish)
#         world = np.full((mapa.shape[0],mapa.shape[1]),None, dtype = environment_things)
#         for i in range(mapa.shape[0]):
#             for j in range(mapa.shape[1]):
#                 if mapa[i,j]==1:
#                     world[i,j]=plain()
#                 elif mapa[i,j]==-1:
#                     world[i,j]=beach()
#                 elif mapa[i,j]==2:
#                     world[i,j]=city("",i,j)
#                 elif mapa[i,j]==3:
#                     world[i,j]=town()
#                 elif mapa[i,j]==4:
#                     world[i,j]=mountain()
#                 elif mapa[i,j]==5:
#                     world[i,j]=fruits()
#                 elif mapa[i,j]==6:
#                     world[i,j]=fish()
#                 else:
#                     world[i,j]=ocean()
#         return world
>>>>>>> a9d482ba7803714e8ef28ceb3c981f9c02f642a4

class Habilidad:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.desbloqueada = False

class Soldado:
    def __init__(self,civilization,row,col):
        self.civilization=civilization
        self.row=row
        self.col=col
        self.energy=False
        self.costo=0
        self.ataque=0
        self.contraataque=0
        self.panico=1
        self.inspiracion=1
        self.comodidad=[]
        self.incomodidad=[]

    dr =[0,0,1,-1,1,1,-1,-1]
    dc =[-1,1,0,0,1,-1,-1,1]
    
    def inspiracion_method(self, mapa):
        panic = 0
        insp = 0
        for i,j in zip(dr,dc):
            if self.row+i<0 or self.row+i>=mapa.shape[0] or self.col+j<0 or self.col+j>=mapa.shape[1]:
                continue
            if mapa[self.row+i,self.col+j].soldado!=None :
                if mapa[self.row+i,self.col+j].soldado.civilization==self.civilization:
                    insp += 0.25
                else:
                    panic+=0.25
            if mapa[self.row+i, self.col+j].__class__ is city: 
                if mapa[self.row+i,self.col+j].civilization==self.civilization:
                    insp+=0.5
                else:
                    panic+=0.5
        if mapa[self.row,self.col].__class__ is city:
            if mapa[self.row,self.col].civilization==self.civilization:
                insp+=1
            else:
                panic+=1
        if mapa[self.row,self.col].__class__ in self.comodidad:
            insp+=0.5
        elif mapa[self.row,self.col].__class__ in self.incomodidad:
            panic+=0.5

        return tuple(max(min(5,int(i)),1) for i in (insp*self.inspiracion,panic*self.panico)) 


    def ataque_method(self,mapa):
        medidas = self.inspiracion_method(mapa)
        return random.randint(self.ataque-medidas[1], self.ataque+medidas[0])

    def contraataque_method(self,mapa):
        medidas = self.inspiracion_method(mapa)
        return random.randint(self.contraataque-medidas[1], self.contraataque+medidas[0])

    def recibe_ataque(self,atacante, mapa):
        self.vida -= atacante.ataque
        if self.vida>0:
            atacante.vida -= self.defensa
        else:
            mapa[atacante.row, atacante.col].ocupado(False, None)
            mapa[self.row, self.col].ocupado(True, atacante)

class Guerrero(Soldado):
    def __init__(self,civilization,row,col):
        super().__init__(civilization,row,col)
        self.vida = 10
        self.ataque = 5
        self.contraataque = 5
        self.name="G"
        self.costo=2
        self.panico = 2
        self.comodidad=[ocean]
        self.incomodidad=[mountain]
    

class Espadachin(Soldado):
    def __init__(self,civilization,row,col):
        super().__init__(civilization,row,col)
        self.vida = 10
        self.ataque = 8
        self.contraataque = 5
        self.name="E"
        self.costo=3
        self.inspiracion=2
        self.comodidad = [mountain]
        self.incomodidad=[ocean]

class Defensor(Soldado):
    def __init__(self,civilization,row,col):
        super().__init__(civilization,row,col)
        self.ataque = 1
        self.vida = 15
        self.contraataque = 8
        self.name="D"
        self.costo=3
        self.comodidad=[city]
