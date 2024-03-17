import tkinter as tk
import statistics
import itertools
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter
import random
import math
from statistics import stdev
from statistics import mean

class Cell :


    def __init__(self ,x ,y, type , wind = [0.5, 'N'], cloud = 0, air_pollution=0 , city_pollution = 0):
        temperature_dic = {
        "land": [23,24,25,26],
        "sea" : [25 , 26 , 27, 28],
        "iceburg" : [-2 , -10 , -12 , -20], 
        "forest" : [ 20 , 21 , 22 , 23], 
        "city" : [26 , 26, 26 , 26]
        }
        self.x = x 
        self.y = y
        self.type = type  # The possible values ​​of type : { land, sea, clouds , iceburg, forest, city }
        index = random.choice([0, 1, 2, 3])
        self.temperature = temperature_dic[type][index]  # temperature in celsius 
        self.wind_speed, self.wind_direction = wind # Wind represented as [speed, direction]
        self.cloud =  cloud # 0 -> no cloud , 1 -> cloud , 2 -> rainy cloud 
        self.air_pollution = air_pollution  # the rate of air pollution
        self.color = self.get_cell_color(type)
        self.city_pollution = city_pollution
        # Saving values ​​for the next generation
        self.next_color = self.color
        self.next_type = self.type
        self.next_temperature = self.temperature
        self.next_wind_speed = self.wind_speed
        self.next_wind_direction = self.wind_direction
        self.next_cloud = self.cloud
        self.next_air_pollution = self.air_pollution

    def get_cell_color(self,type):
        colors_dic = {
        "land": "#7CFC00",     # Green
        "sea": "#00BFFF",      # Deep Sky Blue
        "iceburg": "#FFFFFF",  # White
        "forest": "#228B22",   # Forest Green
        "city": "#FFA500"      # Darker Orange
        }
        return colors_dic[type]

    def update_values(self):
        self.type = self.next_type
        self.color = self.next_color
        self.temperature = self.next_temperature
        self.wind_speed =  self.next_wind_speed
        self.wind_direction = self.next_wind_direction
        self.cloud = self.next_cloud
        self.air_pollution = self.next_air_pollution
        
    
    def generate_next_cell_state(self , neighbors ,air_pollution_effect):
        if random.random() < 0.6:
            self.next_wind_direction = self.wind_direction
        else : 
            self.next_wind_direction = random.choice(["S" , "N" , "W" ,"E"])

        self.neighbors_effect(neighbors , air_pollution_effect)

        # if it is raining then the temperature will decrease
        if self.cloud == 2 and self.next_temperature > 20 : 
            self.next_temperature = self.next_temperature - 1
        
        # If there is wind then the pollution is spread to nearby areas
        if self.wind_speed != 0 :
            self.next_air_pollution = self.next_air_pollution - self.air_pollution * self.wind_speed
        #self.next_air_pollution -= self.air_pollution * self.wind_speed

        # Air pollution contributes to an increase in temperature 
        #if self.next_temperature < 35 :
        self.next_temperature = self.next_temperature + self.air_pollution * air_pollution_effect 

        if self.type == "city":
            self.next_air_pollution += self.city_pollution
        
        if self.next_air_pollution > 1:
            self.next_air_pollution = 1
        if self.next_air_pollution < 0:
            self.next_air_pollution = 0

        # change cells's type according to it's temperature
        if self.type == "sea" and self.next_temperature <= 0:
            self.next_type = "iceburg"
            self.next_color = "#FFFFFF"
        elif self.type == "iceburg" and self.next_temperature > 0:
            self.next_type = "sea"
            self.next_color = "#00BFFF"
    
        
    def neighbors_effect(self , neighbors , air_pollution_effect):
        effect = 0
        for neighbor in neighbors :
            if neighbor != None and neighbor.wind_speed != 0:
                effect += neighbor.air_pollution * air_pollution_effect
                self.move_cloud(neighbor)
        #for index , neighbor in enumerate(neighbors, start=1) :
        #    if index in {1,2,3} and neighbor != None and neighbor.wind_direction == "S":
        #       self.move_cloud(neighbor)
        #       effect += neighbor.air_pollution * neighbor.wind_speed * air_pollution_effect
        #   elif index in {6,7,8} and neighbor != None and neighbor.wind_direction == "N" :
        #       effect += neighbor.air_pollution * neighbor.wind_speed * air_pollution_effect
        #       self.move_cloud(neighbor)
        #   if index == 4 and neighbor != None and neighbor.wind_direction == "E" :
        #        effect += neighbor.air_pollution * neighbor.wind_speed * air_pollution_effect
        #        self.move_cloud(neighbor)
        #    if index == 5 and neighbor != None and neighbor.wind_direction == "W" :
        #        effect += neighbor.air_pollution * neighbor.wind_speed * air_pollution_effect
        #        self.move_cloud(neighbor)
        
        self.next_air_pollution += effect

    def move_cloud( self , neighbor):
        if neighbor.next_cloud != 0 and self.next_cloud == 0 :
            #If the cell is near the sea, the likelihood that the cloud will rain is greater 
            # due to the higher humidity associated with proximity to the sea
            if neighbor.type == "sea" and random.random() < 0.7 :
                self.next_cloud = 2 # rainy
            else : 
                self.next_cloud =  neighbor.next_cloud 
            neighbor.next_cloud = 0
            
class World :
    def __init__(self):
        self.map_size = 15
        self.world_file  = "world.txt"
        self.air_pollution_effect = 0.3
        self.cells_matrix = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.initalize_map()

    def initalize_map(self):
        air_pollution_dic = {
            "sea": 0.1,      # Low pollution near open sea
            "land": 0.2,      # Moderate pollution in general land areas
            "forest": 0.01,   # Lower pollution in forested areas
            "city": 0.3,      # High pollution in urban/city environments
            "iceburg": 0.1  # Low pollution in remote icy regions
        }   
        wind_direction_dic = { 0 : "N" , 1 : "S" , 2 : "W" , 3 : "E" }
        cells_types = self.load_data(self.world_file)
        for x in range(self.map_size):
            for y in range(self.map_size):

                cell_type = cells_types[x][y]

                cloud = random.choice([0, 1 ,2])

                if random.random() < 0.2 :
                    wind_speed = 0 # 20% chance of no wind
                else : 
                    wind_speed = random.randint(1, 20)
                
                wind_direction = wind_direction_dic[random.choice([0,1,2,3])]

                
                self.cells_matrix[x][y] = Cell( x, y,cell_type,[wind_speed,wind_direction],cloud,air_pollution_dic[cell_type], city_pollution = 0.001)

    def next_gen(self): 

        for x in range(self.map_size):
            for y in range(self.map_size):
                cell = self.cells_matrix[x][y]
                neighbours = self.get_neighbours(cell)
                cell.generate_next_cell_state(neighbours ,self.air_pollution_effect)
        
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.cells_matrix[x][y].update_values()

        
    def load_data(self, file):
        cells_types = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        options_dic = {
            "S" : "sea",
            "L" : "land",
            "F" : "forest",
            "C" : "city" ,
            "I" : "iceburg"
        }
        with open(file , 'r') as f :
            for x in range(self.map_size):
                for y in range(self.map_size):
                    temp = f.read(1)
                    while temp not in {"S" , "L" , "F" , "C" , "I"}:
                        temp = f.read(1)
                    cells_types[x][y] = options_dic[temp] 
        return cells_types


    
    def get_neighbours(self , cell):
        # It's important to return the neighbors in the exact way because the index of each neighbor will help us in calculating the wind. 
        x = cell.x 
        y = cell.y
        neighbours = []
        # first cell
        if x-1 >= 0 and y-1 >= 0:
                neighbours.append(self.cells_matrix[x-1][y-1])
        else : neighbours.append(None)
        # second cell
        if x-1 >= 0:
            neighbours.append(self.cells_matrix[x-1][y])
        else : neighbours.append(None)
        # third cell
        if x-1 >= 0 and y+1 < self.map_size:
                neighbours.append(self.cells_matrix[x-1][y+1])
        else : neighbours.append(None)
        # fourth cell
        if y-1 >= 0:
            neighbours.append(self.cells_matrix[x][y-1])
        else : neighbours.append(None)
        # fivth cell
        if y+1 < self.map_size:
            neighbours.append(self.cells_matrix[x][y+1])
        else : neighbours.append(None)
        # sexth cell
        if x+1 < self.map_size and y-1 >= 0:
            neighbours.append(self.cells_matrix[x+1][y-1])
        else : neighbours.append(None)
        # sevnth cell
        if x+1 < self.map_size :
            neighbours.append(self.cells_matrix[x+1][y])
        else : neighbours.append(None) 
        # eighth cell
        if x+1 < self.map_size and y+1 < self.map_size:
            neighbours.append(self.cells_matrix[x+1][y+1])
        else : neighbours.append(None)

        return neighbours

    def temperature_average(self):
        sum = 0
        num_of_cells = self.map_size * self.map_size
        for x in range(self.map_size):
            for y in range(self.map_size):
                sum += self.cells_matrix[x][y].temperature
        return sum / num_of_cells

    def air_pollution_average(self) :
        sum = 0
        num_of_cells = self.map_size * self.map_size
        for x in range(self.map_size):
            for y in range(self.map_size):
                sum += self.cells_matrix[x][y].air_pollution
        return sum / num_of_cells
        
    def temperature_std_dev(self):
        sum_squared_diff = 0
        num_of_cells = self.map_size * self.map_size
        mean_temperature = self.temperature_average()
        for x in range(self.map_size):
            for y in range(self.map_size):
                diff = self.cells_matrix[x][y].temperature - mean_temperature
                sum_squared_diff += diff ** 2
        # Calculate the variance
        variance = sum_squared_diff / num_of_cells
        # Calculate the standard deviation (square root of variance)
        standard_deviation = math.sqrt(variance)
        return standard_deviation

    def air_pollution_std_dev(self):
        sum_squared_diff = 0
        num_of_cells = self.map_size * self.map_size
        mean_temperature = self.air_pollution_average() 
        for x in range(self.map_size):
            for y in range(self.map_size):
                diff = self.cells_matrix[x][y].temperature - mean_temperature
                sum_squared_diff += diff ** 2
        # Calculate the variance
        variance = sum_squared_diff / num_of_cells
        # Calculate the standard deviation (square root of variance)
        standard_deviation = math.sqrt(variance)
        return standard_deviation
class Graphics:
    def __init__(self) :
        self.grid_size = 15
        self.cell_size = 50
        self.refresh_rate = 10
        self.total_generations = 365 # one year
        self.counter_generations = 0
        self.grid = World()
        self.canvas_grid = [[0 for _ in range(self.grid_size)] for i in range(self.grid_size)]
        self.temperature_over_year = []
        self.air_pollution_over_year = []

        self.root = tkinter.Tk()
        self.root.title("Maman 11 ~ A Dynamic Exploration through Cellular Automata")
        self.label = tkinter.Label(self.root)
        self.label.pack()
        self.canvas = tkinter.Canvas(self.root, height=self.grid_size*self.cell_size, width=self.grid_size*self.cell_size)
        self.canvas.pack()
        self.items = self.update_grid(self.canvas_grid)
        self.root.after(self.refresh_rate, self.update_screen)
        self.root.mainloop()

    def update_screen(self):
        self.temperature_over_year.append(self.grid.temperature_average())
        self.air_pollution_over_year.append(self.grid.air_pollution_average())

        self.grid.next_gen()
        
        if self.counter_generations < self.total_generations :
            self.counter_generations += 1
            self.update_grid(self.canvas_grid) 
            self.label.config(text="Generation {}".format(self.counter_generations))
            self.root.after(self.refresh_rate, self.update_screen)
        else :
            #self.update_grid(canvas_grid=self.canvas_grid)
            self.label.config(text="Generation {} DONE !".format(self.counter_generations))
            print("Temperature Data -> \t  min: {:.2f}\t max: {:.2f}\t avg: {:.2f}\t std: {:.2f}".format(min(self.temperature_over_year), max(self.temperature_over_year), mean(self.temperature_over_year), stdev(self.temperature_over_year)))
            print("Air Pollution Data -> \t  min:  {:.2f}\t max: {:.2f}\t avg: {:.2f}\t std: {:.2f}".format(min(self.air_pollution_over_year), max(self.air_pollution_over_year), mean(self.air_pollution_over_year), stdev(self.air_pollution_over_year)))

          
    def update_grid(self, canvas_grid):
        cell_items = self.grid.cells_matrix
        if self.counter_generations != self.total_generations:
            for x in range(self.grid_size):
                for y in range(self.grid_size):

                    cell = cell_items[x][y]
                    cell_label = int(cell.temperature)
                    body = self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, (x+1)*self.cell_size, (y+1)*self.cell_size, fill=cell.color)
                    label = self.canvas.create_text((x+0.5)*self.cell_size, (y+0.5)*self.cell_size, text=cell_label, font="Arial 8 bold")
                    canvas_grid[x][y] = (body, label)

            return canvas_grid

        
if __name__ == '__main__':
    run = Graphics()

    f = open('temperature.txt', 'w')
    for temp in run.temperature_over_year : 
        f.write("{}\n".format(temp))
    f.close()

    f = open('air_pollution.txt', 'w')
    for air in run.air_pollution_over_year: 
        f.write("{}\n".format(air))
    f.close()
    
        

        