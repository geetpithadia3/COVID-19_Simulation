from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from epidemic.agents import Infected, Susceptible, Hospital, Recovered
from epidemic.model import Epidemic


def corona_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Susceptible:
        portrayal["Shape"] = "epidemic/resources/blue.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Infected:
        portrayal["Shape"] = "epidemic/resources/red.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"
    
    elif type(agent) is Recovered:
        portrayal["Shape"] = "epidemic/resources/green.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"
        
    elif type(agent) is Hospital:
        portrayal["Shape"] = "epidemic/resources/hospital.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    
    return portrayal


canvas_element = CanvasGrid(corona_portrayal, 30, 30, 500, 500)
chart_element = ChartModule([{"Label": "Infected", "Color": "#AA0000"},
                             {"Label": "Susceptible", "Color": "#666666"},
                              {"Label": "Recovered", "Color": "#32CD32"}])

model_params = {"initial_susceptible": UserSettableParameter('slider', 'Population',100, 1, 700, 10),
                "initial_infected": UserSettableParameter('slider', 'Initial Infected People',5, 1, 70, 1),
                "hospital": UserSettableParameter('slider', 'Hospitals', 1, 1, 10),
                "mortalityRate": UserSettableParameter('slider', 'Mortality Rate', 1, 1,10 ),
                "social_isolation": UserSettableParameter('checkbox', 'Social Isolation', False)
               }

server = ModularServer(Epidemic, [canvas_element, chart_element], "Corona Epidemic Simulation", model_params)
server.port = 8521
