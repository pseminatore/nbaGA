import pandas as pd
import numpy as np
import create_dataframe
import random
from tqdm import tqdm
from itertools import zip_longest

_population = []

def run(max_generations, mutation_rate, max_salary, fitness_strategy, pairing_strategy, mating_strategy, built=False):
    df = create_dataframe.create()
    #df2 = create_dataframe.read()
    """  print(df1)
    print(df2)
    print(df1.info(verbose=True))
    print(df2.info(verbose=True))
    df3 = df1.compare(df2, align_axis=0)
    print(df3)
    print(df1.equals(df2)) """
    #df1_diff = df3[[df3['_merge'] == 'right_only']]
    #df2_diff = df3[[df3['_merge'] == 'left_only']]
    #df3 = pd.concat([df1, df2]).drop_duplicates(keep=False)
    #print(df1_diff)
    #print(df2_diff)
    population = init_population(100, df, max_salary)
    best_team = [0, [0]]
    
    print("Darwinning...")
    curr_population = population
    ### TODO -- Include some sort of cutoff when result is good enough
    for i in tqdm(range(max_generations)):
        ## Calculate fitness
        population_fitness_tuple = calculate_fitness(curr_population, df, max_salary, fitness_strategy)
        ## Determine mating pool
        sorted_population_tuple = sorted(population_fitness_tuple, key=lambda item: item[0], reverse=True)
        ## Pair up parents
        paired_population_tuple = pair_parents(sorted_population_tuple, pairing_strategy)
        ## Mating Crossover
        ## Mutation
        curr_population = mate_parents(df, paired_population_tuple, mating_strategy, mutation_rate)
    
        ## Get best team (individual)
        population_fitness_tuple = calculate_fitness(curr_population, df, max_salary, fitness_strategy)
        sorted_population_tuple = sorted(population_fitness_tuple, key=lambda item: item[0], reverse=True)
        if sorted_population_tuple[0][0] > best_team[0]:
            best_team[0] = sorted_population_tuple[0][0]
            team = extract_team(sorted_population_tuple[0][1], df)
            best_team[1] = team
    
    ## Build starting 5
    best_team = build_starting_five(best_team[1])
    
    ## Display Roster
    display(best_team, sorted_population_tuple[0][0])    
    print("")
    return best_team
    
def display(team, fitness):
    print("")
    print("Fitness: %d" % fitness)
    print("Starting 5: ")
    for player in team[:5]:
        print(player)
        
    print("Bench: ")
    for player in team[5:]:
        print(player)
        
        
def build_starting_five(team):
    positions = ['C', 'PF', 'SF', 'SG', 'PG']
    for position in positions:
        for player in team:
            if player[2] == position:
                team.insert(0, team.pop(team.index(player)))
                break
    return team

def i_build_starting_five(team, player_idcs):
    positions = ['C', 'PF', 'SF', 'SG', 'PG']
    zpd_team = list(zip(team, player_idcs))
    for position in positions:
        for player in zpd_team:
            if player[0][2] == position:
                zpd_team.insert(0, zpd_team.pop(zpd_team.index(player)))
                break
    return zpd_team

def mate_parents(df, paired_population_tuple, mating_strategy, mutation_rate):
    if mating_strategy == 0:
        child_population = base_mating(paired_population_tuple, mutation_rate)
    elif mating_strategy == 1:
        child_population = positionwise_mating(df, paired_population_tuple, mutation_rate)    
    return child_population

def positionwise_mating(df, paired_population_tuple, mutation_rate):
    new_generation = []
    for mating_pair in paired_population_tuple:
        
        ## Extract mother and father genomes
        mother = mating_pair[0][1]
        father = mating_pair[1][1]

        mother_team = extract_team(mother, df)
        father_team = extract_team(father, df)
        
        mother_gene_idcs = list(np.where(mother == 1)[0])
        father_gene_idcs = list(np.where(father == 1)[0])
        
        mother_pos_team = i_build_starting_five(mother_team, mother_gene_idcs)
        father_pos_team = i_build_starting_five(father_team, father_gene_idcs)
        
        ## Holders for indices of child rosters
        child1_idcs = []
        child2_idcs = []
        
        ## Iterate over each position, the better player goes to child1, lesser goes to child2
        for idx in range(len(mother_pos_team)):
            if mother_pos_team[idx][0][1] > father_pos_team[idx][0][1]:
                child1_idcs.append(mother_pos_team[idx][1])
                child2_idcs.append(father_pos_team[idx][1])
            else:
                child2_idcs.append(mother_pos_team[idx][1])
                child1_idcs.append(father_pos_team[idx][1])
                
                
        ## Blank Child arrays        
        child1 = np.zeros(403)
        child2 = np.zeros(403)
        
        ## Set the player indices to 1
        np.put(child1, child1_idcs, 1)
        np.put(child2, child2_idcs, 1)
        
        child1_gene_idcs = list(np.where(mother == 1)[0])
        child2_gene_idcs = list(np.where(father == 1)[0])
        
        ## Do mutations
        if random.random() < mutation_rate or len(child1_gene_idcs) < 15:
            mutate(child1)           
        if random.random() < mutation_rate or len(child2_gene_idcs) < 15:
            mutate(child2)
            
        ## Add children to new generation
        new_generation.append(child1)
        new_generation.append(child2)
    
    return new_generation
            
        
        
def base_mating(paired_population_tuple, mutation_rate):
    new_generation = []
    for mating_pair in paired_population_tuple:
        
        ## Extract mother and father genomes
        mother = mating_pair[0][1]
        father = mating_pair[1][1]
        
        ## Crossover mating
        crossover_idx = random.randint(1, 14)
        
        mother_gene_idcs = list(np.where(mother == 1)[0])
        father_gene_idcs = list(np.where(father == 1)[0])
        
        child1_idcs = mother_gene_idcs[:crossover_idx]
        child1_idcs += father_gene_idcs[crossover_idx:]
        
        child2_idcs = father_gene_idcs[:crossover_idx]
        child2_idcs += mother_gene_idcs[crossover_idx:]
        
        ## Blank Child arrays
        child1 = np.zeros(403)
        child2 = np.zeros(403)
        
        ## Set the player indices to 1
        np.put(child1, child1_idcs, 1)
        np.put(child2, child2_idcs, 1)
        
        
        ## Do mutations
        if random.random() < mutation_rate:
            mutate(child1)           
        if random.random() < mutation_rate:
            mutate(child2)
        
        ## Add children to new generation
        new_generation.append(child1)
        new_generation.append(child2)
        
    return new_generation

def mutate(child):
    gene_idcs = list(np.where(child == 1)[0])
    if len(gene_idcs) == 15:
        idx_out = random.randint(0, 14)
        gene_idx_out = gene_idcs[idx_out]
        child[gene_idx_out] = 0
    
    while True:    
        gene_idx_in = random.randint(0, 402)
        if gene_idx_in not in gene_idcs:
            break
            
    child[gene_idx_in] = 1
    gene_idcs_p = list(np.where(child == 1)[0])
    return child
    
        
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

def pair_parents(sorted_population_tuple, pairing_strategy):
    paired_tuple = []
    if pairing_strategy == 0:
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
    if fitness_strategy == 1:
        fitness = starting_five_weighted_fitness(individual, df)
    return fitness

def starting_five_weighted_fitness(individual, df):
    fitness = 0
    team = extract_team(individual, df)
    team = build_starting_five(team)
    for player in team[:5]:
        fitness += (int(int(player[1]) * 3))
    for player in team[5:10]:
        fitness += int(int(player[1]) * 2)
    for player in team[10:]:
        fitness += int(int(player[1]) * 0.2)
    return fitness

def find_balanced_total_rating(individual, df):
    fitness = 0
    player_indices = np.where(individual == 1)[0]
    for player_index in player_indices.tolist():
        player_row = df.iloc[player_index] 
        fitness += int(player_row.Rating)   
    return fitness

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

def extract_team(individual, df):
    players = []
    player_indices = np.where(individual == 1)[0]
    for player_index in player_indices:
        player_row = df.iloc[player_index]
        name = player_row.Name
        position = player_row.Position
        rating = player_row.Rating
        salary = player_row.Salary
        player = [name, rating, position, salary]
        players.append(player)
        
    return players
    
if __name__ == "__main__":
    max_salary = 109140000
    max_generations = 8
    mutation_rate = 0.1
    fitness_strategy = 1
    pairing_strategy = 0
    mating_strategy = 1
    run(max_generations, mutation_rate, max_salary, fitness_strategy, pairing_strategy, mating_strategy)