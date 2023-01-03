from clases import map
from clases import myMapConstraint
from cps import CSP
from cps import AC3
from cps import backtracking_search

import numpy as np
from clases import Jugador

a = Jugador("pepe","viking")
b = Jugador("juan","indian")
c = Jugador("kmfke","dessert")

mapa = map([a,b,c])
print(mapa)
# for i in range(mapa.shape[0]):
#     for j in range(mapa.shape[1]):
#         print(mapa[i,j]) 
#     print(",,,,,")       


