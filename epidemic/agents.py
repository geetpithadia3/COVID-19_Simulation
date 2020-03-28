from mesa import Agent
import random
#Base class to handle movements of Agents
class Walker(Agent):
    
    grid = None
    x = None
    y = None
    agentType=None
    social_isolation=None
    

    def __init__(self, unique_id, pos, model, agentType, social_isolation=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.agentType=agentType
        self.social_isolation=social_isolation
        
    def walk(self):
        #In case of Self Isolation
        if self.social_isolation==False:
            if self.agentType=="Infected":
                next_moves = self.model.grid.get_neighborhood(self.pos, True, True)
                next_move = self.random.choice(next_moves)
                #Move the Agent
                self.model.grid.move_agent(self, next_move)
            else:
                for i in range(0,random.randint(1,10)):
                    next_moves = self.model.grid.get_neighborhood(self.pos, True, True)
                    next_move = self.random.choice(next_moves)
                    #Move the Agent
                    self.model.grid.move_agent(self, next_move)
        else:
            for i in range(0,random.randint(1,2)):
                next_moves = self.model.grid.get_neighborhood(self.pos, True, True)
                next_move = self.random.choice(next_moves)
                self.model.grid.move_agent(self, next_move)
            

class Susceptible(Walker):
    def __init__(self, unique_id, pos, model,social_isolation):
        super().__init__(unique_id, pos, model,"Susceptible", social_isolation)
    
    def step(self):
        self.walk()
        

class Infected(Walker):
    infectedTime=None
    mortalityRate=None

    def __init__(self, unique_id, pos, model,social_isolation, mortalityRate):
        super().__init__(unique_id, pos, model,"Infected",social_isolation)
        self.infectedTime = 0
        self.mortalityRate=mortalityRate

    def step(self):
        self.walk()
        self.infectedTime+=1
        x, y = self.pos
        #Fetching the susceptibles in the neighbourhood
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        susceptibles = [obj for obj in this_cell if isinstance(obj, Susceptible)]
        if len(susceptibles) > 0:
            toInfect = self.random.choice(susceptibles)
            #Removing the Susceptible
            self.model.grid._remove_agent(self.pos, toInfect)
            self.model.schedule.remove(toInfect)
            #Adding the Infected
            newInfected= Infected(self.model.next_id(), self.pos, self.model,self.social_isolation, self.mortalityRate)
            self.model.grid.place_agent(newInfected, newInfected.pos)
            self.model.schedule.add(newInfected)
            
        #Mortality of Infected
        if(self.infectedTime>10/self.mortalityRate):
            newRecovered= Recovered(self.model.next_id(), self.pos, self.model,self.social_isolation)
            self.model.grid.place_agent(newRecovered, newRecovered.pos)
            self.model.schedule.add(newRecovered)
            
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

class Recovered(Walker):

    def __init__(self, unique_id, pos, model,social_isolation):
        super().__init__(unique_id, pos, model,"Recovered",social_isolation)
        

    def step(self):
        self.walk()
            
        
            

class Hospital(Agent):
    social_isolation=None
    def __init__(self, unique_id, pos, model,social_isolation):
        super().__init__(unique_id, model)
        self.social_isolation=social_isolation
        
    def step(self):
        #Getting the Infected from neighbourhood
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        infected = [obj for obj in this_cell if isinstance(obj, Infected)]
        if len(infected) > 0:
            toRecover = self.random.choice(infected)
            #Recovering the Infected
            newRecovered= Recovered(self.model.next_id(), self.pos, self.model,self.social_isolation)
            self.model.grid.place_agent(newRecovered, newRecovered.pos)
            self.model.schedule.add(newRecovered)
            #Removing the Infected
            self.model.grid._remove_agent(self.pos, toRecover)
            self.model.schedule.remove(toRecover)
        
     