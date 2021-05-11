import random

import numpy as np

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 5    #This is the number of actionss

# Train against random for 5 generations, then against self for 1 generations
trainingSchedule = [('random', 30)]

# This is the class for your creature/agent

class MyCreature:

    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values

        # .
        # .
        # .
        self.chromosome = np.random.random(size=(5, 5, 3))
        self.chromosome = self.chromosome - 0.5

    def AgentFunction(self, percepts):
        #lement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 5-dim numpy vector or a
        # list with 5 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 4 - eat
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # .
        # .
        # .

        #generate new list of actions
        actions = [0, 0, 0, 0, 0]
        # get the chance of eating(only need to be found in one dimention)
        actions[4] = percepts[2, 2, 1] * self.chromosome[2, 2, 1] 

        # check both the fruit array and the oppoent array
        for i in range(0, 5):
            for j in range(0, 5):
                for k in range(0, 2):

                    p_value = percepts[i, j, k]

                    if k == 0:
                        p_value = (percepts[i, j, k]*-1) - percepts[2, 2, 0]
                    if i < 2:
                        actions[1] += p_value * self.chromosome[i, j, k]
                    if i > 2:
                        actions[3] += p_value * self.chromosome[i, j, k]
                    if j < 2:
                        actions[0] += p_value * self.chromosome[i, j, k]
                    if j > 2:
                        actions[2] += p_value * self.chromosome[i, j, k]



        return actions

# function to select the index corrosponding to which chromozone to pick
def selection(fitness):

    # quoted from wikipedia,  this is step 1 of 4 to select the pairs to breed
    # The fitness function is evaluated for each individual, providing fitness values, which are then normalized.
    # Normalization means dividing the fitness value of each individual by the sum of all fitness values,
    # so that the sum of all resulting fitness values equals 1.
    fitness_sum = sum(fitness['value'])
    print(fitness['value'])
    if(fitness_sum == 0):
        return  fitness
    normalized_fitness = fitness['value'] / fitness_sum

    # quoted from wikipedia,  this is step 2 of 4 to select the pairs to breed
    # Accumulated normalized fitness values are computed: the accumulated fitness value of an individual
    # is the sum of its own fitness value plus the fitness values of all the previous individuals;
    # the accumulated fitness of the last individual should be 1,
    # otherwise something went wrong in the normalization step.

    accumulated_fitness = fitness
    accumulated_fitness[0]['value'] = normalized_fitness[0]
    for i in range(0, len(accumulated_fitness) - 1):
        accumulated_fitness[i + 1]['value'] = accumulated_fitness[i]['value'] + normalized_fitness[i + 1]
    return accumulated_fitness



def re_selection(accumulated_fitness):
    # quoted from wikipedia,  this is step 3 of 4 to select the pairs to breed
    # A random number R between 0 and 1 is chosen.
    R = random.random()

    # quoted from wikipedia,  this is step 4 of 4 to select the pairs to breed
    # The selected individual is the first one whose accumulated normalized value is greater than or equal to R.
    for i in accumulated_fitness:
        if i['value'] >= R:
            return i['index']
    if R > 0.5:
        return 0
    return 1


def newGeneration(old_population):
    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)
    # Fitness for all agents

    dtype = [('index', int), ('value', float)]
    values = []
    for i in range(0, N):
        values.append((i, 0.0))

    strawb_fitness = np.array(values, dtype=dtype)
    eats_fitness = np.array(values, dtype=dtype)
    wall_fitness = np.array(values, dtype=dtype)

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order


    for n, creature in enumerate(old_population):

        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game enginne:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        # creature.squares_visited - how many different squares the creature visited
        # creature.bounces - how many times the creature bounced

        # .
        # .
        # .

        # This fitness functions just considers length of survival.  It's probably not a great fitness
        # function - you might want to use information from other stats as well
        #fitness[n][1] = 0.0
        #print(creature.strawb_eats)
        strawb_fitness[n]['value'] = 0.0

        strawb_fitness[n]['value'] += creature.strawb_eats*20 + creature.enemy_eats*5 +creature.size


    # At this point you should sort the agent according to fitness and create new population
    strawb_sorterd_fitness = np.sort(strawb_fitness, order='value')


    new_population = list()

    strawb_normalised = selection(strawb_sorterd_fitness)


    # use the a function to select to indexs to pick

    stawb_parent_1_index = re_selection(strawb_normalised)
    stawb_parent_2_index = re_selection(strawb_normalised)

    # re-pick index 2 until they are different
    while stawb_parent_1_index != stawb_parent_2_index:
        stawb_parent_2_index = re_selection(strawb_normalised)


    # now we have 2 parents time to preform crossover
    strab_chrome_1 = old_population[stawb_parent_1_index].chromosome
    strab_chrome_2 = old_population[stawb_parent_2_index].chromosome

    for n in range(N):

    # Create new creature
        new_creature = MyCreature()

        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        child_chromosome = np.zeros((5, 5, 3))

        #use uniform crossover to mix the chromosomes(generate probabilities and
        # if they are less that 0.5 use parent one otherwise use parent 2
        for i in range(0, 5):
            for j in range(0, 5):
                for k in range(0,3):
                    r = random.random()
                    if r < 0.5:
                        child_chromosome[i, j, k] = strab_chrome_1[i, j, k]

                    else:
                        child_chromosome[i, j, k] = strab_chrome_2[i, j, k]



        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.
        r = random.random()
        if r > 0.98:
            a = random.randrange(0, 5)
            b = random.randrange(0, 5)
            c = random.randrange(0, 3)
            child_chromosome[a, b, c] = random.random() - 0.5

        # Add the new agent to the new population
        new_creature.chromosome = child_chromosome
        new_population.append(new_creature)

        # At the end you neet to compute average fitness and return it along with your new population
    new_population[0].chromosome = old_population[strawb_sorterd_fitness[-1]['index']].chromosome
    print(strawb_sorterd_fitness[-1]['value'])
    avg_fitness = np.mean(strawb_fitness['value']+eats_fitness['value']+wall_fitness['value'])
    f = open("f1.txt", "a")
    f.write(str(avg_fitness)+"\n")
    f.close()
    return (new_population, avg_fitness)


