import mesa
from mesa import Model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

#--- AGENT ---#
class Cleaner(mesa.Agent):
    """An agent that cleans dirty cells"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        "Moves the cleaner to a random valid space"
        self.move()

        "Checks for dirt in current cell, if so takes action"
        position = self.model.grid.get_cell_list_contents([self.pos])
        dirt = [obj for obj in position if isinstance(obj, Dirt)]
        if len(dirt) > 0:
            dirt_remove = self.random.choice(dirt)
            self.model.grid.remove_agent(dirt_remove)
            self.model.schedule.remove(dirt_remove)

        
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        cleaner = [obj for obj in position if isinstance(obj, Cleaner)]
        if len(cleaner) < 1:
            self.model.grid.move_agent(self, chosen_step)


class Dirt(mesa.Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)

#--- MODEL ---#
class cleaningModel(Model):
    def __init__(self,width,height,x,p,e):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        d = (p*(width*height))/100

        #Create Cleaners
        for i in range(x):
            clean = Cleaner(self.next_id(),self)
            self.schedule.add(clean)
            self.grid.place_agent(clean,(1,1))
            
        
        for i in range(5):
            dirty = Dirt(self.next_id(),self)
            self.schedule.add(dirty)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(dirty,(x,y))
            

    def step(self):
        self.schedule.step()
#--- SERVEVR ---#
def cleaning_port(agent):
    portrayal = {"Shape":"circle","Filled":"true", "r":0.5}

    if type(agent) is Cleaner:
        
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        
    
        print(agent.unique_id)
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

grid = CanvasGrid(cleaning_port, 10, 10, 500, 500)
server = ModularServer(cleaningModel,[grid],"cleaningModel",{"width":10,"height":10,"x":10,"p":25,"e":100})
server.port = 8521 
server.launch()

