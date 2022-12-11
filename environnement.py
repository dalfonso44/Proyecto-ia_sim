
from abc import ABC, abstractmethod

class Environnement:
    """Base class for an Environnement """

    def __init__(self, name:str,agents,*args,**kwargs) -> None:

        self.run = False
        self.stop = False
        self.agents = agents
        self.initial_state = self.built_environnement()
        self.current_state = self.initial_state
        self.history = []

    @abstractmethod   
    def built_environnement(self):
        """Builts the environnemenet"""
        pass

    @abstractmethod
    def run_environnement(self, agents):
        """Runs the envvironnement until the Stop condition is True"""
        pass


    





            



    
   






