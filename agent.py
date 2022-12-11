from environnement import Environnement
from abc import ABC,abstractclassmethod, abstractmethod


class Agent(ABC):
    """Abstract class for an agent"""
    def __init__(self, id: int) -> None:
        self.id = id
        self.knowledgebase = dict()

    @abstractmethod
    def See(self, environnement):
        """This function has the hability of observing the environnement and return a Perception of it""" 
        pass   


    @abstractmethod
    def Next(self,perception, internal_state):
        """This function change the state of the environnrment that the agent has from the environnement
        based on the perception and the old state"""
        pass


    @abstractmethod
    def conduct_layer(self,social_knoledge):
        """this layer has the responsability of the reactive behavior of the agent"""
        pass
     
    @abstractmethod
    def planing_layer(self,planing_knoledge):
        """this layer has the responsability of the planing for achieve the agent goals"""
        pass
     
    @abstractmethod 
    def cooperative_layer(self,environnement_model):
        """this layer has the responsability of social interactions"""
        pass

    

    @abstractmethod    
    def Action(sefl,internal_state):
        """This function represents the agent actions based in the perceptions of the environnement"""
        pass    



