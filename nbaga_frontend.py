from flask import Flask
from flask import render_template, request, redirect, url_for
import nba_genetic_algorithm
import ast
app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def homepage(built=None):
    built = False
    if request.method == "POST":
        req = request.form
        population_size = int(req.get("PopSize"))
        max_salary = int(req.get("MaxSalary"))
        max_generations = int(req.get("MaxGenerations"))
        mutation_rate = float(req.get("MutationRate"))
        fitness_strategy = convert_fitness(req.get("FitnessStrategy"))
        pairing_strategy = convert_pairing(req.get("PairingStrategy"))
        mating_strategy = convert_mating(req.get("MatingStrategy"))
        team = nba_genetic_algorithm.run(population_size, max_generations, mutation_rate, max_salary, fitness_strategy, pairing_strategy, mating_strategy)
        print(req)
        return redirect(url_for('displayTeam', teamList=team))
    return render_template('homepage.html', built=built)

@app.route("/team/<teamList>")
def displayTeam(teamList, built=None):
    built = True
    team = ast.literal_eval(teamList)
    return render_template('teampage.html', team=team)

def convert_fitness(strategy):
    if strategy == 'Balanced':
        return 0
    if strategy == 'Starting Five':
        return 1
    
def convert_pairing(strategy):
    if strategy == 'Top-Down':
        return 0
    
def convert_mating(strategy):
    if strategy == 'Random Crossover':
        return 0
    if strategy == 'Positionwise':
        return 1
    