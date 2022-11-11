# -----
# Descripción Breve:
#   Esta es una simulación de multiagentes con el fin de estudiar las estadísticas 
#   de un robot de limpieza reactivo.
# -----
# Autores:
#   Adrián Bravo López A01752067
#   Sebastián Burgos Alanís A01746459 
# -----
# Fecha de creación:
#   10/11/22
# Fecha de modificación:
#   11/10/22
# -----

import mesa
from mesa import Model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

#-------------#
#--- AGENT ---#
#-------------#

class Cleaner(mesa.Agent):
    # Clase para crear el Agente, definir su acción y su movimiento. 
    # Constructor del agente de limpieza y sus atributos.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # Si la celda tiene Dirt, la limpia. 
    def step(self):
        self.move()
        position = self.model.grid.get_cell_list_contents([self.pos])
        dirt = [obj for obj in position if isinstance(obj, Dirt)]
        if len(dirt) > 0:
            dirt_remove = self.random.choice(dirt)
            self.model.grid.remove_agent(dirt_remove)
            self.model.schedule.remove(dirt_remove)

    # Función para mover al agente a una posición aleatoria disponible.
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        cleaner = [obj for obj in position if isinstance(obj, Cleaner)]
        if len(cleaner) < 1:
            self.model.grid.move_agent(self, chosen_step)

class Dirt(mesa.Agent):
    # Constructor para la creación de la Dirt. 
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)

#-------------#
#--- MODEL ---#
#-------------#

class cleaningModel(Model):
    # Clase para definir el Modelo, asiganción de variables, creación de 1 o más Agentes. 
    # Constructor del Modelo con las variables requeridas
    def __init__(self,width,height,x,p,e):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        d = (p*(width*height))/100

        # Creación de los Agentes
        for i in range(x):
            clean = Cleaner(self.next_id(),self)
            self.schedule.add(clean)
            self.grid.place_agent(clean,(1,1))
            
        # Colocación aleatoria de la Dirt. 
        for i in range(round(d)):
            dirty = Dirt(self.next_id(),self)
            self.schedule.add(dirty)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(dirty,(x,y))
        
    def step(self):
        self.schedule.step()

#--------------#
#--- SERVER ---#
#--------------#

def cleaning_port(agent):
    # Función para crear el servidor, el Canvas, asignar el puerto de servidor,
    #   definir los colores y figuras de los agentes así como la asiganción de los valores para 
    #   crear Numero de Agentes, Espacio de habitación, Porcentaje de celdas sucias y tiempo de ejecución. 
    portrayal = {"Shape":"circle","Filled":"true", "r":0.5}

    # Diseño de los Agentes
    if type(agent) is Cleaner:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    
    # Diseño de la Dirt. 
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

# Diseño del Canvas y definición de valores. 
grid = CanvasGrid(cleaning_port, 10, 10, 500, 500)
server = ModularServer(cleaningModel,[grid],"cleaningModel",{"width":10,"height":10,"x":10,"p":25,"e":100})

# Puerto de salida de transmisión. 
server.port = 8521 

# Lanzamiento del servidor. 
server.launch()

