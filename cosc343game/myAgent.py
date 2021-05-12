import random

import numpy as np

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 5    #This is the number of actionss

# Train against random for 5 generations, then against self for 1 generations
trainingSchedule = [('random', 100),('hunter', 100)]

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
#expects a sorted array, returns the largest index
def tourment(fitness, cutOff):
    np.random.shuffle(fitness)
    #print("shuffled fitness: ")
    #print(fitness)
    #print("\n\n")
    fitness = fitness[cutOff:]
    #print("cut fitness: ")
    #print(fitness)
    #print("\n\n")
    fitness = np.sort(fitness, order='value')
    #print("sorted fitness: ")
    #print(fitness)
    #print("\n\n")
    fitness[-1]['value'] = -100
    return fitness[-1]['index']




# function pre-pare an array for the roulte wheel by normalising and then acculmating the values.
def accumulate(fitness):


    fitness_sum = sum(fitness['value'])
    if(fitness_sum == 0):
        return  fitness
    normalized_fitness = fitness['value'] / fitness_sum



    accumulated_fitness = fitness
    accumulated_fitness[0]['value'] = normalized_fitness[0]
    for i in range(0, len(accumulated_fitness) - 1):
        accumulated_fitness[i + 1]['value'] = accumulated_fitness[i]['value'] + normalized_fitness[i + 1]
    return accumulated_fitness


#spin the roulte wheel.
def roultewheel(accumulated_fitness):

    R = random.random()


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

    #create a numpy array that keeps track of our index so we can sort
    dtype = [('index', int), ('value', float)]
    values = []
    for i in range(0, N):
        values.append((i, 0.0))

    fitness = np.array(values, dtype=dtype)
    fitnessOrignal = np.array(values, dtype=dtype)

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
        fitness[n]['value'] = 0.0

        fitness[n]['value'] += creature.strawb_eats*400 + creature.enemy_eats*200 + creature.squares_visited

        fitnessOrignal[n]['value'] = 0.0
        fitnessOrignal[n]['value'] += creature.strawb_eats*400 + creature.enemy_eats*200 + creature.squares_visited
    #sort our fitness by there value.
    #print("our fitness  :")
    #print(fitness)
    #print("\n\n")
    fitness = np.sort(fitness, order='value')

    #print("sorted fitness  :")
    #print(fitness)
    #print("\n\n")

    #fitness = accumulate(fitness)

    #print("accumulated fitness  :")
    #print(fitness)
    #print("\n\n")


    parent_1_index = tourment(fitness,20)
    parent_2_index = tourment(fitness,20)


    # re-pick index 2 until they are different
    while parent_1_index == parent_2_index:
        parent_2_index = tourment(fitness, 15)

    #print("parent 1 index : " + str(parent_1_index) + "value:" + str(fitnessOrignal[parent_1_index]["value"]))
    #print("parent 2 index : " + str(parent_2_index) + "value:" + str(fitnessOrignal[parent_2_index]["value"]))
    #print("\n\n")
    # now we have 2 parents time to preform crossover

    chrome_1 = old_population[parent_1_index].chromosome
    chrome_2 = old_population[parent_2_index].chromosome


    new_population = []
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
                        child_chromosome[i, j, k] = chrome_1[i, j, k]

                    else:
                        child_chromosome[i, j, k] = chrome_2[i, j, k]



        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        r = random.random()
        if r > 0.99:
            ##print("mutation")
            ##print("\n\n")
            a = random.randrange(0, 5)
            b = random.randrange(0, 5)
            c = random.randrange(0, 3)
            child_chromosome[a, b, c] = random.random() - 0.5

        # Add the new agent to the new population
        new_creature.chromosome = child_chromosome
        new_population.append(new_creature)

        # At the end you neet to compute average fitness and return it along with your new population
    new_population[0].chromosome = old_population[tourment(fitness, 32)].chromosome

    avg_fitness = np.mean((fitnessOrignal['value']+fitnessOrignal['value']+fitnessOrignal['value']))
    f = open("f1.txt", "a")
    f.write(str(avg_fitness)+"\n")
    f.close()
    return (new_population, avg_fitness)


