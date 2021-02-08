import pandas as pd
import numpy as np
import create_dataframe
import random
from tqdm import tqdm

def main(population, max_generations, mutations_per_generation, max_salary):
    df = create_dataframe.create()
    print("Darwinning...")
    curr_population = population
    for i in tqdm(range(max_generations)):
        ## Calculate fitness
        ## Determine mating pool
        ## Pair up parents
        ## Mating Crossover
        ## Mutation
        ## new_generation = get offspring

def init_population(pop_size):
    population = []
    
    print("Creating initial population...")
    for index in tqdm(range(pop_size)):
        
        individual = np.zeros(403)
        player_indices = get_random_indices()
        
        for player_index in player_indices:
            individual[player_index] = 1
            
        population.append(individual)
        
    return population
        
def get_random_indices(roster_size=15):
    
    players = []   
    for roster_spot in range(roster_size):
        while True:
            add_player_index = random.randint(0, 402)
            if add_player_index not in players:
                players.append(add_player_index)
                break
            
    return players


def calculate_fitness(population, df):
    fitness_dict = {}
    for individual in population:
        
        
if __name__ == "__main__":
    population = init_population(100)
    max_generations = 70
    mutations_per_generation = 1
    max_salary = 109140000
    main(population, max_generations, mutations_per_generation, max_salary)