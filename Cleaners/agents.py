import mesa


class Cleaner(mesa.Agent):
    """An agent that cleans dirty cells"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        "Moves the cleaner to a random valid space"
        self.move()

        "Checks for dirt in current cell, if so takes action"
        position = self.model.grid.get_cell_list_contents([self.pos])
        dirt = [obj for obj in this_cell if isinstance(obj, Dirt)]
        if len(dirt) > 0:
            dirt_remove = self.random.choice(dirt)
            self.model.grid.remove_agent(dirt_remove)
            self.model.schedule.remove(dirt_remove)

        
    
    def move():
        possible_steps = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        cleaner = [obj for obj in this_cell if isinstance(obj, Cleaner)]
        if len(cleaner) < 1:
            self.model.grid.move_agent(self, chosen_step)


class Dirt(mesa.Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)
    
    