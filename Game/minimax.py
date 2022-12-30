import math
from unittest import result 
infinity = math.inf

class Game:
    """A game is similar to a problem, but it has a terminal test instead of 
    a goal test, and a utility for each terminal state. To create a game, 
    subclass this class and implement `actions`, `result`, `is_terminal`, 
    and `utility`. You will also need to set the .initial attribute to the 
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)
    
    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def play_game(self,players):
        current_state = self.initial
        while not self.is_terminal(current_state):
            for player in players:
                move = player.play()
                current_state = result(current_state,move)
                winner, utility = player, self.utility(current_state,player)
                if self.is_terminal(current_state):
                    break
        print(current_state)
        return winner, utility        






def minimax_search_solutions(game,state):
    """Search game tree to determine best move; return (value, move) pair."""

    player = state.to_move
    alpha = -infinity

    def max_value(state, alpha, beha):
        if game.is_terminal(state):
            return game.utility(state,player), None
        v, move = - infinity, None    
        for a in game.actions(state):
            v2, _ = min_value(game.result(state,a), v)
            if v2 > v:
                v,move = v2, a
        return v,move   

    def min_value(state,betha):
        if game.is_terminal(state):
            return game.utility(state,player), None

        v, move = infinity, None
        for a in game.actions(state):
            v2,_ = max_value(game.result(state,a),v)
            if v2 > betha:
                break
            if v2 < v:
                v,move = v2,a
        return v,move    

    return max_value(state, alpha)                         

                
