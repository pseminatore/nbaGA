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
        calculate_fitness(curr_population, df, max_salary)
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


def calculate_fitness(population, df, max_salary):
    fitness_dict = {}
    for individual in population:
        total_salary = extract_salaries(individual, df)
        
        ### TODO -- Continue to calculate fitness
        if total_salary > max_salary:
            fitness = 0
            
        pass
        

def extract_salaries(individual, df):
    salaries = {}
    total_salary = 0
    player_indices = np.where(individual == 1)[0]
    
    for player_index in player_indices.tolist():
        
        player_row = df.iloc[player_index]
        salary = player_row.Salary
        
        int_salary = int(salary.replace(',', ''))
        total_salary += int_salary    
        
        salaries[player_row.Name] = int_salary # For debugging purposes -- and it's kinda fun to see what teams get built
        
    return total_salary
    
if __name__ == "__main__":
    population = init_population(100)
    max_generations = 70
    mutations_per_generation = 1
    max_salary = 109140000
    main(population, max_generations, mutations_per_generation, max_salary)