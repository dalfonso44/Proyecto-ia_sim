from world.clases import *

class Jugador:
    def __init__(self, civilization):
        self.soldados = []
        self.puntuacion=0
        self.presupuesto = 3
        self.habilidades = [[Habilidad('pesca',5), Habilidad('nautuca',5),Habilidad('navegacion',5)],
                            [Habilidad('escalada',5), Habilidad('mineria',5), Habilidad('herreria',5)],
                            [Habilidad('organizacion',5), Habilidad('agricultura',5), Habilidad('milicias',5)]]
        self.civilization=civilization

    def play():
        pass