from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from epidemic.agents import Susceptible, Infected, Hospital, Recovered
from epidemic.schedule import RandomActivationByType


class Epidemic(Model):
    height = 30
    width = 30

    initial_susceptible = 100
    initial_infected = 50
    initial_recovered = 0
    hospital=1
    mortalityRate=0.1
    
    social_isolation=False

    verbose = False

    description = 'A model for simulating spread of Corona Virus using SIR modelling.'

    def __init__(self, height=30, width=30,
                 initial_susceptible=100, initial_infected=50 ,hospital=1, social_isolation=False,mortalityRate=0.1):
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_susceptible = initial_susceptible
        self.initial_infected = initial_infected
        self.hospital=hospital
        self.social_isolation= social_isolation
        self.mortalityRate=mortalityRate
        self.schedule = RandomActivationByType(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        #Collecting the data for Agents
        self.datacollector = DataCollector(
            {"Infected": lambda m: m.schedule.get_type_count(Infected),
             "Susceptible": lambda m: m.schedule.get_type_count(Susceptible),
             "Recovered": lambda m: m.schedule.get_type_count(Recovered)})

        #Creating Susceptibles
        for i in range(self.initial_susceptible):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            newSusceptible = Susceptible(self.next_id(), (x, y), self,social_isolation)
            self.grid.place_agent(newSusceptible, (x, y))
            self.schedule.add(newSusceptible)

        #Creating Infected
        for i in range(self.initial_infected):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            newInfected = Infected(self.next_id(), (x, y), self,social_isolation,mortalityRate)
            self.grid.place_agent(newInfected, (x, y))
            self.schedule.add(newInfected)
            
        #Creating Hospitals
        for i in range(self.hospital):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            newHospital = Hospital(self.next_id(), (x, y), self,social_isolation)
            self.grid.place_agent(newHospital, (x, y))
            self.schedule.add(newHospital)



        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_type_count(Infected),
                   self.schedule.get_type_count(Susceptible),
                   self.schedule.get_type_count(Recovered)])

    def run_model(self, step_count=200):
        if self.verbose:
            print('Initial number infected: ',
                  self.schedule.get_type_count(Infected))
            print('Initial number susceptible: ',
                  self.schedule.get_type_count(Susceptible))
            print('Initial number recovered: ',
                  self.schedule.get_type_count(Recovered))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number infected: ',
                  self.schedule.get_type_count(Infected))
            print('Final number susceptible: ',
                  self.schedule.get_type_count(Susceptible))
            print('Final number recovered: ',
                  self.schedule.get_type_count(Recovered))
