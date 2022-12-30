from mimetypes import init
from Game.minimax import Game
from clases import map


class Action():
    def __init__(self) -> None:
        pass

class Civilization(Game):
    #players es una lista de jugadores
    def __init__(self, players) -> None:
        self.map = map(10,10,10,10,10,10,10,10)# cambiar estos numeros
        self.game_over = False
        self.players = players
        self.turn = 0
        self.actual_player=-1

    def actions(self, state):
        current_player = self.players[self.actual_player]
        return avaiable_moves(self.map,current_player) # debe ser posible a partir del id del jugador sacar el submapa correspondiente y encontrar las acciones correspondientes


    def result(self, state, move):
        pass

    def utility(self, state, player):
        pass 

    def is_terminal(self, state):
        return self.game_over

    def play_game(self):
        return super().play_game(self.players)                


def avaiable_moves(environment,current_player):
    pass     