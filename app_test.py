from Game.Civilization import *
from Players.MC_D_Player import *
from Players.MC_Player import *
from Players.MCTS_Player import *
from Players.Player import *
from Players.RandomPlayer import *
import sys

count=1
player1=sys.argv[1]
player2=sys.argv[2]
player3=sys.argv[3]

vikings='vikings'
romans='romans'
chineese='chineese'
players=[player1+'(vikings)',player2+'(romans)',player3+'(chineese)']

count=3
for i in range(len(players)):
    if not players[i].find('MCTSPlayer'):
        count+=2
        H = int(sys.argv[count-1])
        B = int(sys.argv[count])
    if not players[i].find('MC_D_Player'):
        count+=4
        Td = int(sys.argv[count-3])
        Gd = int(sys.argv[count-2])
        Bd = int(sys.argv[count-1])
        D = int(sys.argv[count])
    if not players[i].find('MC_Player'):
        count+=2
        T = int(sys.argv[count-1])
        G = int(sys.argv[count])


a = Civilization([eval(players[0]),eval(players[1]),eval(players[2])])
a.play_game() 
with open('resultados/scores', 'a') as f:
    for p in a.players:    
        f.write('\n'+p.civilization+'\t'+str(p.puntuacion)+'\n')

