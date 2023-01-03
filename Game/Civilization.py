from mimetypes import init
from world.clases import *
from Players.Player import *
import pandas as pd
import csv

class Action():
    def __init__(self, action):
        self.action = action
    

class Civilization():
    #players es una lista de jugadores
    def __init__(self, players) -> None:
        self.map = map(20,20,0.55,0.9,0.98,0.95,0.89,0.87)# cambiar estos numeros
        self.game_over = False
        self.players = players
        self.turn = 0
        self.turns = 30
        self.actual_player=0
        self.precios_guerreros={'Guerrero':2,'Espadachin':3,'Defensor':3}
        self.precios_construir={'planting':2,'beach':2,'mine':5,'farm':5,'port':10}
        self.construcciones={'planting':'fruits','farm':'planting','beach':'fish','port':'beach','mine':'mountain'}
        self.ciudades=[]
        self.intereses=3
        self.add_cities()
        self.deads=[]

    def actions(self):
        current_player = self.players[self.actual_player]
        return self.avaiable_moves(current_player) # debe ser posible a partir del id del jugador sacar el submapa correspondiente y encontrar las acciones correspondientes


    def result(self, state, move):
        pass

    def utility(self, state, player):
        pass 

    def is_terminal(self, state):
        return self.game_over

    def state(self,turn):
        #print(turn)
        table = pd.DataFrame(columns=['money','capital','hab_pesca','hab_esc','hab_org','pob','score'], index=['vikings','romans','chineese'])
        for i in self.players:
            table['pob'][i.civilization]=0
            table['capital'][i.civilization]=[]
            table['money'][i.civilization]=i.presupuesto
            table['score'][i.civilization]=i.puntuacion
            for j in range(len(i.habilidades)):
                table[table.columns[j+2]][i.civilization]=3
                for k in range(len(i.habilidades[j])):
                    if not i.habilidades[j][k].desbloqueada:
                        table[table.columns[j+2]][i.civilization]=k
                        break
        for i in self.ciudades:
            table['pob'][i.civilization]+=i.poblacion
            table['capital'][i.civilization].append((i.row,i.col))
        #print(table)
        #print(self.map)
        #return table

    def play_game(self):
        #print('HISTORIA REAL')
        with open('resultados/mi_fichero', 'a') as f:
            f.write(self.map.__str__()+'\n')
        #self.state(self.turn)
        i=self.turn
        while self.turn<self.turns:
            self.players[self.actual_player].play(self)
            if i!=self.turn:
                i=self.turn
       #         print('HISTORIA REAL')
        #self.state(self.turn).to_csv('mi_fichero', sep=" ")
       

    def play_action(self):
        self.players[self.actual_player].play(self)
    
    def add_cities(self):
        civ = ['vikings','romans','chineese']
        for i in range(self.map.map.shape[0]):
            for j in range(self.map.map.shape[1]):
                if(self.map.map[i,j].__class__ is city):
                    self.ciudades.append(self.map.map[i,j])
                    self.map.map[i,j].poblacion=6
                    x= random.choice(civ)
                    self.map.map[i,j].civilization=x
                    self.map.map[i,j].history.append(x)
                    civ.remove(x)
                    

    dr =[0,0,1,-1,1,1,-1,-1]
    dc =[-1,1,0,0,1,-1,-1,1]

    def avaiable_moves(self,current_player):
        actions = ['termina(0)']
        for i in current_player.soldados:
            if not i.energy:
                continue 
            if self.map.map[i.row,i.col].__class__ is city and self.map.map[i.row,i.col].civilization != current_player.civilization:
                actions.append('tomar_ciudad(*'+str((i.row,i.col))+')')
            if self.map.map[i.row,i.col].__class__ is town:
                actions.append('tomar_pueblo(*'+str((i.row,i.col))+')')
                
            #actions.append('move(*'+str((i.row,i.col,i.row,i.col))+')')
            for j,k in zip(dr,dc):
                if i.row+j<0 or i.row+j>=self.map.map.shape[0] or i.col+k<0 or i.col+k>=self.map.map.shape[1]:
                    continue
                if accesible(self.map.map[i.row,i.col], self.map.map[i.row+j,i.col+k],current_player.habilidades):
                    if self.map.map[i.row+j,i.col+k].soldado != None and self.map.map[i.row+j,i.col+k].soldado.civilization !=current_player.civilization:
                        actions.append('fight(*'+str((i.row,i.col,i.row+j,i.col+k))+')')
                    if self.map.map[i.row+j,i.col+k].soldado == None:
                        actions.append('move(*'+str((i.row,i.col,i.row+j,i.col+k))+')')

        for i in range(len(current_player.habilidades)):
            for j in range(len(current_player.habilidades[i])):
                if not current_player.habilidades[i][j].desbloqueada:
                    if current_player.presupuesto > current_player.habilidades[i][j].precio:
                        actions.append('desarrollar_habilidades(*'+str((i,j))+')')
                    break

        for k,v in self.precios_guerreros.items():
            if current_player.presupuesto>v:
                if k == 'Espadachin' and not current_player.habilidades[1][2].desbloqueada:
                    continue
                if k == 'Defensor' and not current_player.habilidades[2][2].desbloqueada:
                    continue
                for i in self.ciudades:
                    if i.soldado==None and i.civilization == current_player.civilization:
                        actions.append('entrenar(*'+str((k,i.row,i.col))+')')

        for c in self.ciudades:
            if c.civilization == current_player.civilization:
                menu=(
                ('planting',current_player.habilidades[2][0].desbloqueada,'fruits'),
                ('beach',current_player.habilidades[0][0].desbloqueada,'fish'),
                ('mine',current_player.habilidades[1][1].desbloqueada,'mountain'),
                ('farm',current_player.habilidades[2][1].desbloqueada,'planting'),
                ('port',current_player.habilidades[0][1].desbloqueada,'beach'))
                
                for i,j in zip(dr,dc):
                    if c.row+i<0 or c.row+i>=self.map.map.shape[0] or c.col+j<0 or c.col+j>=self.map.map.shape[1]:
                        continue
                    for estructure,hab,terreno in menu:
                        if self.map.map[c.row+i,c.col+j].__class__ == eval(terreno) and hab and current_player.presupuesto>self.precios_construir[estructure]:
                            actions.append('construir(*'+str((c.row+i,c.col+j,c.row,c.col,estructure))+')')
        return actions

    def tomar_pueblo(self,town_row, town_col,ejecuta=False,revierte=False):
        current_player = self.players[self.actual_player]
        if revierte and ejecuta:
            self.ciudades.remove(self.map.map[town_row,town_col])
            sold=self.map.map[town_row,town_col].soldado
            self.map.map[town_row,town_col] = town()
            self.map.map[town_row,town_col].soldado=sold
            self.map.map[town_row,town_col].soldado.energy = True
        elif ejecuta:
            sold=self.map.map[town_row,town_col].soldado
            self.map.map[town_row,town_col] = city(current_player.civilization, town_row,town_col,3)
            self.ciudades.append(self.map.map[town_row,town_col])
            self.map.map[town_row,town_col].soldado=sold
            self.map.map[town_row,town_col].soldado.energy = False
        if ejecuta:
            current_player.puntuacion += 280 * (1-2*revierte)
        return 280 * (1-2*revierte)

    def tomar_ciudad(self,city_row, city_col,ejecuta=False,revierte=False):
        current_player = self.players[self.actual_player]
        if revierte and ejecuta:
            self.map.map[city_row,city_col].soldado.energy=True
            self.map.map[city_row,city_col].history.pop()
            self.map.map[city_row,city_col].civilization = self.map.map[city_row,city_col].history[-1]
            for i in self.players:
                if i.civilization == self.map.map[city_row,city_col].civilization:
                    i.puntuacion-= (280+20*self.map.map[city_row,city_col].poblacion)*(1-2*revierte)

        elif ejecuta:
            for i in self.players:
                if i.civilization == self.map.map[city_row,city_col].civilization:
                    i.puntuacion-= (280+20*self.map.map[city_row,city_col].poblacion)*(1-2*revierte)

            self.map.map[city_row,city_col].soldado.energy=False
            self.map.map[city_row,city_col].civilization = current_player.civilization
            self.map.map[city_row,city_col].history.append( current_player.civilization)
        
        if ejecuta:
            current_player.puntuacion += (280+20*self.map.map[city_row,city_col].poblacion)*(1-2*revierte)
        
        return (280+20*self.map.map[city_row,city_col].poblacion)*(1-2*revierte)


    def move(self,current_x, current_y, new_x, new_y,ejecuta=False,revierte=False):        
        if revierte and ejecuta:
            return self.move(new_x,new_y,current_x,current_y,ejecuta)
        if ejecuta:
            self.map.map[new_x,new_y].soldado=self.map.map[current_x,current_y].soldado
            if current_x!=new_x or current_y!=new_y:
                self.map.map[current_x,current_y].soldado=None
                self.map.map[new_x,new_y].soldado.row=new_x
                self.map.map[new_x,new_y].soldado.col=new_y
                self.map.map[new_x,new_y].soldado.energy=revierte
        return 0

    def fight(self,sold1_x,sold1_y,sold2_x,sold2_y,ejecuta=False, revierte = False):
        puntuacion=0
        inv=(1-2*revierte)
        current_player = self.players[self.actual_player]

        if revierte:
            if self.map.map[sold1_x,sold1_y].soldado==None:
                if current_player.civilization == self.map.map[sold2_x,sold2_y].soldado.civilization:
                    self.map.map[sold1_x,sold1_y].soldado = self.map.map[sold2_x,sold2_y].soldado
                    self.map.map[sold1_x,sold1_y].soldado.row=sold1_x
                    self.map.map[sold1_x,sold1_y].soldado.col=sold1_y
                    self.map.map[sold2_x,sold2_y].soldado = self.deads.pop()   
                    for i in self.players:
                        if i.civilization==self.map.map[sold2_x,sold2_y].soldado.civilization:
                            i.soldados.append(self.map.map[sold2_x,sold2_y].soldado)
                            i.puntuacion+=self.map.map[sold2_x,sold2_y].soldado.costo*5
                else:
                    self.map.map[sold1_x,sold1_y].soldado=self.deads.pop()
                    current_player.soldados.append(self.map.map[sold1_x,sold1_y].soldado)
                    puntuacion=self.map.map[sold1_x,sold1_y].soldado.costo*5
        else:
            if self.map.map[sold2_x,sold2_y].soldado.vida<=self.map.map[sold1_x,sold1_y].soldado.ataque:
                for i in self.players:
                    if i.civilization==self.map.map[sold2_x,sold2_y].soldado.civilization and ejecuta:
                        i.puntuacion-=self.map.map[sold2_x,sold2_y].soldado.costo*5

            elif self.map.map[sold1_x,sold1_y].soldado.vida <= self.map.map[sold2_x,sold2_y].soldado.contraataque:
                puntuacion=-self.map.map[sold1_x,sold1_y].soldado.costo*5
        if ejecuta:
            self.map.map[sold1_x,sold1_y].soldado.energy=not revierte
            self.map.map[sold2_x,sold2_y].soldado.vida-= self.map.map[sold1_x,sold1_y].soldado.ataque*inv
            if self.map.map[sold2_x,sold2_y].soldado.vida>0:
                if not revierte or  self.map.map[sold2_x,sold2_y].soldado.vida > self.map.map[sold1_x,sold1_y].soldado.ataque:
                    self.map.map[sold1_x,sold1_y].soldado.vida -= self.map.map[sold2_x,sold2_y].soldado.contraataque*inv
                if self.map.map[sold1_x,sold1_y].soldado.vida<=0:
                    self.deads.append(self.map.map[sold1_x,sold1_y].soldado)
                    for i in self.players:
                        if i.civilization == self.map.map[sold1_x,sold1_y].soldado.civilization:
                            i.soldados.remove(self.map.map[sold1_x,sold1_y].soldado)
                    self.map.map[sold1_x,sold1_y].soldado=None
            else:
                self.deads.append(self.map.map[sold2_x,sold2_y].soldado)
                for i in self.players:
                    if i.civilization == self.map.map[sold2_x,sold2_y].soldado.civilization:
                        i.soldados.remove(self.map.map[sold2_x,sold2_y].soldado)
                self.map.map[sold2_x,sold2_y].soldado = self.map.map[sold1_x,sold1_y].soldado
                self.map.map[sold1_x,sold1_y].soldado = None

                self.map.map[sold2_x,sold2_y].soldado.row=sold2_x
                self.map.map[sold2_x,sold2_y].soldado.col=sold2_y
            current_player.puntuacion+=puntuacion
        return puntuacion

    def desarrollar_habilidades(self, i,j,ejecuta=False,revierte=False):
        if ejecuta:
            current_player = self.players[self.actual_player]
            current_player.presupuesto-=current_player.habilidades[i][j].precio * (1-2*revierte)
            current_player.habilidades[i][j].desbloqueada= not revierte
            current_player.puntuacion+=100* (1-2*revierte)
        
        return 100* (1-2*revierte)

    def entrenar(self,soldado,city_x,city_y,ejecuta=False, revierte =False):
        current_player = self.players[self.actual_player]
        if revierte and ejecuta:
            current_player.soldados.remove(self.map.map[city_x,city_y].soldado)
            self.map.map[city_x,city_y].soldado = None
            current_player.presupuesto += self.precios_guerreros[soldado] 

        elif ejecuta:
            current_player.presupuesto -= self.precios_guerreros[soldado] 
            new_soldier = eval(soldado)(current_player.civilization,city_x,city_y)
            self.map.map[city_x,city_y].soldado = new_soldier
            current_player.soldados.append(new_soldier)
        if ejecuta:
            current_player.puntuacion += self.precios_guerreros[soldado]*5* (1-2*revierte)

        return self.precios_guerreros[soldado]*5* (1-2*revierte)

    def construir(self,pos_x,pos_y,city_x,city_y,const,ejecuta=False, revierte = False):
        c=eval(const)()
        if ejecuta:
            sold=self.map.map[pos_x,pos_y].soldado
            self.map.map[pos_x,pos_y]=eval(const if not revierte else self.construcciones[const])()
            self.map.map[city_x,city_y].poblacion+=c.poblacion*(1-2*revierte)
            self.players[self.actual_player].presupuesto-=(1-2*revierte)*c.costo
            self.map.map[pos_x,pos_y].soldado=sold
            self.players[self.actual_player].puntuacion += c.poblacion*20* (1-2*revierte)

        return c.poblacion*20* (1-2*revierte)
    
    def termina(self,_,ejecuta=False, revierte = False):
        if ejecuta:
            self.actual_player=self.actual_player+1
            for s in self.players[self.actual_player%3].soldados:
                s.energy=True
            if self.actual_player%3 !=self.actual_player:
                self.actual_player=self.actual_player%3
                for c in self.ciudades:
                    for j in self.players:
                        if c.civilization == j.civilization:
                            j.presupuesto += c.poblacion//self.intereses
                self.turn+=1
                #self.state(self.turn)
                if self.turn%3==0:
                    for j in self.players:
                        for hab in j.habilidades:
                            for h in hab:
                                h.precio+=1
        return 0

def accesible(position, new_position, habilidades):
    if(not habilidades[1][0].desbloqueada) and new_position.__class__ is mountain:
        return False
    if(not habilidades[0][2].desbloqueada) and new_position.__class__ is ocean:
        return False
    if new_position.__class__ is port:  
        return True
    if new_position.__class__ is beach and not (position.__class__ is beach or position.__class__ is ocean):  
        return False
    return True


                

            