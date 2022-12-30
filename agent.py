from environnement import Environnement
from abc import ABC,abstractclassmethod, abstractmethod



class Agent(ABC):
    """Abstract class for an agent"""
    def __init__(self, id: int) -> None:
        self.id = id


    @abstractmethod
    def see(self,environnement):
        pass


    @abstractmethod    
    def action(sefl,perception):
        """This function represents the agent actions based in the perceptions of the environnement"""
        pass    


class knowledgebase_agent(Agent):
    def __init__(self, id: int, knowledgebase) -> None:
        super().__init__(id)
        self.id = id
        self.knowledgebase = knowledgebase

    def action(sefl, perception):
        pass
          


class ReactiveAgent(Agent):
    """this agent takes action based only on the percept"""
    def __init__(self, id: int) -> None:
        super().__init__(id)


class PlanningAgent(Agent):
    """"""
    def __init__(self, id: int) -> None:
        super().__init__(id)

class SocialAgent(Agent):
    def __init__(self, id: int) -> None:
        super().__init__(id) 


class TouringMachine(ReactiveAgent,PlanningAgent,SocialAgent):
    def __init__(self, id: int) -> None:
        super().__init__(id)                      

class CivilizationAgent(Agent):
    def __init__(self, id: int) -> None:
        super().__init__(id)
