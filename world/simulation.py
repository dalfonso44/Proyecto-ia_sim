from world.clases2 import Habilidad, Jugador, map
import random


mapa = map()
jugadores = [Jugador('1'),Jugador('2'),Jugador('3')]
jugador_actual = -1

#habilidades=[Habilidad('pesca',5), Habilidad('nautica',5), Habilidad('navegacion',5), 
#             Habilidad('escalada',5), Habilidad('mineria',5), Habilidad('herreria',5),
#             Habilidad(pass'organizacion',5), Habilidad('agricultura',5), Habilidad('milicias',5)]

def definir_jugador(jugadores):
    jugador_actual = (jugador_actual + 1)%len(jugadores)

def crear_jugadores():
    pass

def tropas(jugador_actual):
    for i in jugador_actual.soldados:
        tm,ta,tt = jugador_actual.tropas(i)
        x = random.random()
        if x<tm:
            new_pos = jugador_actual.movimiento(i, mapa)
            mapa[i.row,i.col].ocupado(False,None)
            mapa[new_pos].ocupado(True,i)

        elif x<tm+ta:
            soldado_herido = jugador_actual.atacar(i, mapa)
            soldado_herido.recibe_ataque(i, mapa)
        
        else:
            jugador_actual.tomar_ciudad(i,mapa)
            mapa[i.row,i.col].civilizacion = jugador_actual.civilizacion


def juega(jugador_actual):
    
    tropas(jugador_actual)
    
    c,e,d = jugador_actual.invertir()
    x = random.random()
   
    if x<c:
        cp,cm,cg,p,rf = jugador_actual.construir()
        x=random.random()
        if x<cp:
            jugador_actual.construir_puerto(mapa)
        elif x<cp+cm:
            jugador_actual.construir_minas(mapa)
        elif x<cp+cm+cg:
            jugador_actual.construir_granjas(mapa)
        elif x<cp+cm+cg+p:
            jugador_actual.pescar(mapa)
        else:
            jugador_actual.recolectar_frutos(mapa)
    
    elif x<c+e:
        eg,ed,ee = jugador_actual.entrenar()
        x = random.random()
        if x<eg:
            jugador_actual.crear_guerrero()
        elif x<eg+ed:
            jugador_actual.crear_defensor()
        else:
            jugador_actual.crear_espadachin()
    
    else:
        d1, d2, d3 = jugador_actual.desarrollar_habilidades()
        x = random.random()
        if x<d1:
            jugador_actual.desarrollar_d1()
        elif x<d1+d2:
            jugador_actual.desarrollar_d2()
        else:
            jugador_actual.desarrollar_d3()


jugadores = crear_jugadores()
for i in range(30):
    definir_jugador(jugador_actual)
    jugadores = crear_jugadores()
    juega(jugador_actual)

    
        
        

    