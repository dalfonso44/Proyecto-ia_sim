from world.clases2 import map
from world.clases2 import myMapConstraint
from world.csp import CSP
from world.csp import AC3
from world.csp import backtracking_search

import numpy as np
from world.clases2 import Jugador

a = Jugador("pepe","viking")
b = Jugador("juan","indian")
c = Jugador("kmfke","dessert")

mapa = map([a,b,c])
print(mapa)
# for i in range(mapa.shape[0]):
#     for j in range(mapa.shape[1]):
#         print(mapa[i,j]) 
#     print(",,,,,")       


