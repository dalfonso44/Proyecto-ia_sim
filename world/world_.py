import numpy as np
import random
import itertools as it


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

def distancia(i,j,posiciones,posible,b=2):
    if not posible:
        return 0
    if not len(posiciones):
        return 1.0
    return max(min(max(abs(x-i),abs(y-j)) for x,y in posiciones)-b,0)

def generacion_de_ciudades_capitales(mapa, cant_ciudades=3):
    posiciones=[]
    while(cant_ciudades>0):
        prob=[[distancia(i,j,posiciones,mapa[i,j]==1) for j in range(mapa.shape[1])] for i in range(mapa.shape[0])]
        suma=sum(sum(i) for i in prob)
        if suma==0:
            return False
        x=random.random()*suma
        s=0
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                s+=prob[i][j]
                if x<s:
                    cant_ciudades-=1
                    mapa[i,j]=2
                    posiciones.append((i,j))
                    break
            if x<s:
                break
    return posiciones

def generacion_de_poblados(mapa,posiciones):
    while(True):
        prob=[[distancia(i,j,posiciones,mapa[i,j]==1) for j in range(mapa.shape[1])] for i in range(mapa.shape[0])]
        suma=sum(sum(i) for i in prob)
        if suma==0:
            break
        x=random.random()*suma
        s=0
        for i in range(mapa.shape[0]):
            for j in range(mapa.shape[1]):
                s+=prob[i][j]
                if x<s:
                    mapa[i,j]=3
                    posiciones.append((i,j))
                    break
            if x<s:
                break
    
def generacion_de_montannas(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]==1 and random.random() < prob:
                mapa[i,j]=4
    
def generacion_de_frutos(mapa, prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j]==1 and random.random() < prob:
               mapa[i,j]=5

def generacion_de_peces(mapa,prob):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            if mapa[i,j] ==-1 and random.random() < prob:
               mapa[i,j]=6



