import numpy as np
import random


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
            cant += (mapa[pos_x+i,pos_y+j]==1)
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

def distancia(i,j,posiciones,area):
    prod=1.0
    if len(posiciones):
        for x,y in posiciones:
            prod*=(abs(i-x)+abs(j-y))
    return prod/area**(len(posiciones)/2)

def generacion_de_ciudades_capitales(mapa, prob, cant_ciudades=3):
    posiciones=[]
    while(cant_ciudades>0):
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                d=distancia(i,j,posiciones,mapa.shape[0]*mapa.shape[1])
                if cant_ciudades>0 and mapa[i,j]==1 and random.random()*d**(0.1) > prob:
                        cant_ciudades-=1
                        mapa[i,j]=2
                        posiciones.append((i,j))
#                        comprobacion_relleno(mapa,i,j,True, 2)
    print(posiciones)
    return posiciones

def generacion_de_poblados(mapa, prob,posiciones):
    cant_pueblos =random.randint(4,6)
    while(cant_pueblos>0):
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                d=distancia(i,j,posiciones,mapa.shape[0]*mapa.shape[1])
                if cant_pueblos>0 and mapa[i,j]==1 and random.random()*d**(0.002) > prob:
                    mapa[i,j]=3
                    cant_pueblos-=1
                    posiciones.append((i,j))
    #                comprobacion_relleno(mapa,i,j,True, 3)
    print("poblado",posiciones)

    
def generacion_de_montannas(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]==1 and random.random() > prob:
                mapa[i,j]=4
    
def generacion_de_frutos(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]==1 and random.random() > prob:
               mapa[i,j]=5

def generacion_de_peces(mapa,prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j] ==-1 and random.random() > prob:
               mapa[i,j]=6



