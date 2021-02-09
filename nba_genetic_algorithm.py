import pandas as pd
import numpy as np
import create_dataframe
import random
from tqdm import tqdm
from itertools import zip_longest

def main(df, population, max_generations, mutations_per_generation, max_salary, fitness_strategy, mating_strategy):
    
    print("Darwinning...")
    curr_population = population
    for i in tqdm(range(max_generations)):
        ## Calculate fitness
        population_fitness_tuple = calculate_fitness(curr_population, df, max_salary, fitness_strategy)
        ## Determine mating pool
        sorted_population_tuple = sorted(population_fitness_tuple, key=lambda item: item[0], reverse=True)
        ## Pair up parents
        paired_population_tuple = pair_parents(sorted_population_tuple, mating_strategy)
        ## Mating Crossover
        ## Mutation
        ## new_generation = get offspring

def init_population(pop_size, df, max_salary):
    population = []
    
    print("Creating initial population...")
    for index in tqdm(range(pop_size)):
        
        while True:
            individual = np.zeros(403)
            player_indices = get_random_indices()
            for player_index in player_indices:
                individual[player_index] = 1
            if has_complete_lineup(individual, df) and (extract_salaries(individual, df) < max_salary):
                break
            
        population.append(individual)
        
    return population

def pair_parents(sorted_population_tuple, mating_strategy):
    paired_tuple = []
    if mating_strategy == 0:
        parent_pairs = top_down_pairing(sorted_population_tuple)
    return parent_pairs

def top_down_pairing(mating_pool):
    parent_pairs = grouper(mating_pool)
    return parent_pairs
    
def grouper(parent_pool, n=2, fillvalue=None):
    args = [iter(parent_pool)] * n        
    return list(zip_longest(*args, fillvalue=fillvalue))


def get_random_indices(roster_size=15):
    
    players = []   
    for roster_spot in range(roster_size):
        
        while True:
            
            add_player_index = random.randint(0, 402)
            
            if add_player_index not in players:
                
                players.append(add_player_index)
                break
            
    return players


def calculate_fitness(population, df, max_salary, fitness_strategy):
    fitness_dict = []
    for individual in population:
               
        total_salary = extract_salaries(individual, df)
        
        if total_salary > max_salary:
            fitness = 0
        elif not has_complete_lineup(individual, df):
            fitness = 0
        else:
            fitness = find_weighted_fitness(individual, df, fitness_strategy)
        fitness_dict.append([fitness, individual])
    return fitness_dict

def find_weighted_fitness(individual, df, fitness_strategy):
    if fitness_strategy == 0:
        fitness = find_balanced_total_rating(individual, df)   
    return fitness

def find_balanced_total_rating(individual, df):
    total_ovr = 0
    player_indices = np.where(individual == 1)[0]
    for player_index in player_indices.tolist():
        player_row = df.iloc[player_index] 
        total_ovr += int(player_row.Rating)   
    return total_ovr

def has_complete_lineup(individual, df):
    positions = get_positions(individual, df)
    req_positions = ['PG', 'SG', 'SF', 'PF', 'C']
    for req_position in req_positions:
        if req_position not in positions.values():
            return False
    return True
            
def get_positions(individual, df):
    
    positions = {}
    player_indices = np.where(individual == 1)[0]
    
    for player_index in player_indices.tolist():
        
        player_row = df.iloc[player_index]
        position = player_row.Position
        positions[player_row.Name] = position
        
    return positions
    
def extract_salaries(individual, df):
    salaries = {}
    total_salary = 0
    player_indices = np.where(individual == 1)[0]
    
    for player_index in player_indices.tolist():
        
        player_row = df.iloc[player_index]
        salary = player_row.Salary
        
        ### TODO -- Come up with better way to handle null salaries.  Maybe ensure in init population?
        if salary == '':
            int_salary = 109140000
        else:    
            int_salary = int(salary.replace(',', ''))
            
        total_salary += int_salary    
        
        salaries[player_row.Name] = int_salary # For debugging purposes -- and it's kinda fun to see what teams get built
        
    return total_salary
    
if __name__ == "__main__":
    df = create_dataframe.create()
    max_salary = 109140000
    population = init_population(100, df, max_salary)
    max_generations = 70
    mutations_per_generation = 1
    fitness_strategy = 0
    mating_strategy = 0
    main(df, population, max_generations, mutations_per_generation, max_salary, fitness_strategy, mating_strategy)