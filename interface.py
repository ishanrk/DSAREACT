import pygame
import random
import heapq
import math
import time
import pandas as pd

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK=(255,192,203)
RED=(255,0,0)


BACK_IMAGE= pygame.image.load("brain2.png")


def row_to_neuron(row):
    return {
        "index": row["index"],
        "location": row["location"],
        "connection_bias": row["connection_bias"],
        "error": row["error"],
        "neuron_size": row["neuron_size"],
        "connections": row["connections"]
    }
class Neuron:
    def __init__(self, neuron_dict):
        self.index = neuron_dict["index"]
        self.location= neuron_dict["location"]
        self.connection_bias = neuron_dict["connection_bias"]
        self.error=neuron_dict["error"]
        self.neuron_size=neuron_dict["neuron_size"]
        self.connections = []
        self.x_coord = 0
        self.y_coord = 0
        self.color = YELLOW

    def set_x(self, x):
        self.x_coord = x
    
    def set_y(self,y):
        self.y_coord=y
    
    def connection_add(self, neuron_index):
        self.connections.append(neuron_index)



def generate_subset_neurons(subset_number):
    neuron_dataframe = pd.read_json('data.json') # THIS IS THE PLACE WHERE NEW DATA WILL GO
    neurons = [row_to_neuron(row) for _, row in neuron_dataframe.iterrows()]
    print(len(neurons))
    in_graph=[]
    in_graph = set(in_graph)
    first_neuron = neurons[random.randint(0,100000)]
    in_graph.add(first_neuron["index"])

    current_Subset_lenght = 1
    random.seed(422) #random seed

    while(current_Subset_lenght!=subset_number):
        random_neuron = neurons[random.randint(0,99999)]
        if random_neuron["index"] not in in_graph:
            in_graph.add(random_neuron["index"])
            current_Subset_lenght+=1

    print("debug")
    neuron_list=[]
    
    in_graph = list(in_graph)
    for neuron in in_graph:
        num_edges = random.randint(1,2)
        x=0
        new_neuron = Neuron(neurons[neuron])
        while(x!=num_edges):
            random_neuron = in_graph[random.randint(0,len(in_graph)-1)]
            if(random_neuron!=neuron):
                x+=1
                
                new_neuron.connection_add(random_neuron)
        neuron_list.append(new_neuron)

    return neuron_list
    

def main():
    neurons = generate_subset_neurons(500)
    pos_dict={}

    for neuron in neurons:
        if(neuron.location=="occipital_lobe"):
            xmin=70
            xmax=500
            ymin=500
            ymax=734

            x_loc = random.randint(xmin,xmax)
            y_loc = random.randint(ymin, math.floor(600+(134/600)*x_loc))
            pos_dict[neuron.index] = (x_loc,y_loc)
            neuron.set_x(x_loc)
            neuron.set_y(y_loc)
        if(neuron.location=="temporal_lobe"):
            xmin=70
            xmax=500
            ymin=200
            ymax=500
            
            x_loc = random.randint(xmin,xmax)
            
            y_loc= random.randint(math.floor(450+(-250/430)*x_loc),ymax)
            pos_dict[neuron.index] = (x_loc,y_loc)

            neuron.set_x(x_loc)
            neuron.set_y(y_loc) 
        if(neuron.location=="parietal_lobe"):
            xmin=500
            xmax=950
            ymin=500
            ymax=700
            
            x_loc = random.randint(xmin,xmax)
            
            y_loc= random.randint(ymin,math.floor(935+(-134/400)*x_loc))
            
            pos_dict[neuron.index] = (x_loc,y_loc)
            neuron.set_x(x_loc)
            neuron.set_y(y_loc)
        if(neuron.location=="frontal_lobe"):
            xmin=500
            xmax=950
            ymin=250
            ymax=500
            
            x_loc = random.randint(xmin,xmax)
            
            y_loc= random.randint(math.floor(-83.3+(1/2)*x_loc),ymax)
            
            pos_dict[neuron.index] = (x_loc,y_loc)
            neuron.set_x(x_loc)
            neuron.set_y(y_loc)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 834 ))
    pygame.display.set_caption("Brain Interface")
    
    font = pygame.font.SysFont(None, 50)
    running = True

    
    while running:
        screen.fill((230, 230, 255))
        screen.blit(BACK_IMAGE,(0,0))
        hi_render = font.render("Brain Interface", True, WHITE)
        screen.blit(hi_render, (400, 100))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
               

        for neuron in neurons:
            if(neuron.location=="occipital_lobe"):
                pygame.draw.circle(screen, YELLOW, (neuron.x_coord,neuron.y_coord), neuron.neuron_size)
            if(neuron.location=="temporal_lobe"):
                pygame.draw.circle(screen, GREEN, (neuron.x_coord,neuron.y_coord), neuron.neuron_size)
            if(neuron.location=="parietal_lobe"):
                pygame.draw.circle(screen, PINK, (neuron.x_coord,neuron.y_coord), neuron.neuron_size)
            if(neuron.location=="frontal_lobe"):
                pygame.draw.circle(screen, RED, (neuron.x_coord,neuron.y_coord), neuron.neuron_size)
            

        
        
        pygame.display.flip()
        clock.tick(60)
    





# Define node class


if __name__ =="__main__":
    main()
