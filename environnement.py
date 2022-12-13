
from abc import ABC, abstractmethod

class Environnement(ABC):
    """Base class for an Environnement """

    def __init__(self) -> None:

        self.run = False
        self.stop = False
        self.agents = []
        self.initial_state = self.built_environnement()
        self.current_state = self.initial_state

    @abstractmethod   
    def built_environnement(self):
        """Builts the environnemenet"""
        pass

    @abstractmethod
    def perception(self,agent):
        """return the percept that the agent sees at this point"""
        pass

    @abstractmethod
    def execute_action(self,agent,action):
        """Change the world to reflect this action"""
        pass


    @abstractmethod
    def run_environnement(self, agents):
        """Runs the envvironnement until the Stop condition is True"""
        pass



        


        

class CivilizationWorld(Environnement):
    def __init__(self,civilization_agents, size_x, size_y) -> None:
        super().__init__()
        self.agents = civilization_agents
        self.size_x = size_x
        self.size_y = size_y
        self.total_of_cells = size_x * size_y
        self.turns = 30
        


    def built_environnement(self): # Dependiendo de la civilizacion de los agentes es que se genera el mapa
        """"""
        pass

    def run_environnement(self):
        self.run = True
        for turn in self.turns:
            self.run_a_turn()

    def run_a_turn(self):
        for agent in self.agents:
            self.execute_action(agent,agent.agent_program(self.current_state))

        

    


#cells

# Esto es una celda generica que puede tener 1 o mas objetos
# x ej : una celda de agua y tiene peces o una celda de hierba que tiene flores o un caballo o hay un guerrero parado ahi
class CivilizationCell():
    def __init__(self, name) -> None:
        self.name = name
        self.objects = [CivilizationObject] 

    def __str__(self) -> str:
        return self.name 

class Sea(CivilizationCell):
    def __init__(self, name = 'sea') -> None:
        super().__init__(self,name)  

class Ground (CivilizationCell):
    def __init__(self, name='ground') -> None:
        super().__init__(name)  

class Desert(CivilizationCell):
    def __init__(self, name = 'desert') -> None:
        super().__init__(name)                   


# Objects
            
class CivilizationObject(): # esto puede ser un guerrero, un pez, una mina .....
    def __init__(self, name) -> None:
        self.name = name


    
class Warrior(CivilizationObject):
    def __init__(self, name = 'warrior', cord_x = -1, cord_y = -1) -> None:
        super().__init__(name)    
        self.cord_x = cord_x
        self.cord_y = cord_y

    def Move(self, new_x, new_y):
        self.cord_x = new_x
        self.cord_y = new_y    


   







