import pandas as pd

p1='vikings'
p2='romans'
p3='chineese'
filas=['i',p1,p2,p3]

with open('resultados/scores/scoresID', 'r') as f:
    data=pd.DataFrame([{filas[i]:int(v) for i,v in enumerate(l.split())} for l in f.readlines()])
    data.set_index('i',inplace=True)

print("Se jugaron",len(data),"partidos")
print('Las puntuaciones medias fueron:')
print(data.mean(axis=0))

maximos=data.max(axis=1)
data[p1]=data[p1]==maximos
data[p2]=data[p2]==maximos
data[p3]=data[p3]==maximos
suma=data.sum(axis=1)
data[p1]=data[p1]/suma
data[p2]=data[p2]/suma
data[p3]=data[p3]/suma
print('los juegos ganados por judadores fueron:')
print(data.sum(axis=0))