from Game.Civilization import *
from Players.MC_D_Player import *
from Players.MC_Player import *
from Players.MCTS_Player import *
from Players.Player import *
from Players.RandomPlayer import *
import sys

count=1
vsc=0
if vsc:
    player1="MCTSPlayer"
    player2="MC_Player"
    player3="RandomPlayer"
    ID="0"
else:
    player1=sys.argv[1]
    player2=sys.argv[2]
    player3=sys.argv[3]
    ID=sys.argv[4]

vikings='vikings'
romans='romans'
chineese='chineese'
players=[player1+'(vikings)',player2+'(romans)',player3+'(chineese)']

#count=3
#for i in range(len(players)):
#    if not players[i].find('MCTSPlayer'):
#        count+=2
#        H = int(sys.argv[count-1])
#        B = int(sys.argv[count])
#    if not players[i].find('MC_D_Player'):
#        count+=4
#        Td = int(sys.argv[count-3])
#        Gd = int(sys.argv[count-2])
#        Bd = int(sys.argv[count-1])
#        D = int(sys.argv[count])
#    if not players[i].find('MC_Player'):
#        count+=2
#        T = int(sys.argv[count-1])
#        G = int(sys.argv[count])


a = Civilization([eval(players[0]),eval(players[1]),eval(players[2])])
a.play_game(ID)
with open('resultados/scoresID', 'a') as f:
    f.write(ID+'\t'+str(a.players[0].puntuacion)+'\t'+str(a.players[1].puntuacion)+'\t'+str(a.players[2].puntuacion)+'\n')

