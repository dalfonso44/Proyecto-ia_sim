from world.map_csp import *
from world.map_test import *

#m = map(10,10,['viking','indian'])

m = create_map(5,5,['viking','indian','chinese','american'])

def pri(m):
    s=''
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if isinstance(m[i,j],ocean):
                s +='O'
            elif isinstance(m[i,j],mine):
                s+='K'
            elif isinstance(m[i,j],fruits):
                s +='F'
            elif isinstance(m[i,j],city):
                s +='X'
            elif isinstance(m[i,j],town):
                s +='T'
            elif isinstance(m[i,j],fish):
                s +='P'
            elif isinstance(m[i,j],farm):
                s +='G'
            elif isinstance(m[i,j],planting):
                s+='Y'
            elif isinstance(m[i,j], port):
                s+='R'
            elif isinstance(m[i,j],plain):
                s+='L'
            elif isinstance(m[i,j],mountain):
                s +='M'
            elif isinstance(m[i,j],beach):
                s +='B'
                

            if m[i,j].soldado == None:
                s+='_ '
            elif isinstance(m[i,j].soldado,Guerrero):
                s+='g '
            elif isinstance(m[i,j].soldado,Defensor):
                s+='d '
            elif isinstance(m[i,j].soldado,Espadachin):
                s+='e '
        s+='\n'
        return s


a = pri(m)
print(m)        