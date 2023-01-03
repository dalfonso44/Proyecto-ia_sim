from Game.Civilization import *
from Players.MC_D_Player import *
from Players.MC_Player import *
from Players.MCTS_Player import *
from Players.Player import *
from Players.RandomPlayer import *



a = Civilization([MCTSPlayer('vikings'),MC_Player('romans'),RandomPlayer('chineese')])
a.play_game() 