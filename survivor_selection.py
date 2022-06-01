#imports
import random


def replacement(current_pop, current_fitness, offspring, offspring_fitness):
    """replacement selection"""

    population = []
    fitness = []

    #Initialize variables
    pooledCurrent=[]
    pooledOffspring=[]
    mu=len(current_pop)
    lamb=len(offspring)

    #Create two 2d lists containing either current individuals paired with their fitness or offspring pair with their fitness
    for x in range(mu):
        pooledCurrent.append([])
        pooledCurrent[x].append(current_pop[x])
        pooledCurrent[x].append(current_fitness[x])
    for x in range(lamb):
        pooledOffspring.append([])
        pooledOffspring[x].append(offspring[x])
        pooledOffspring[x].append(offspring_fitness[x])

    #Sort both lists in decreasing order based on fitness
    sortedbyfitCurrent=sorted(pooledCurrent, key=lambda l:l[1], reverse=False)
    sortedbyfitOffspring=sorted(pooledOffspring, key=lambda l:l[1], reverse=False)

    #Delete weakest lambda elements from the end of current population
    del sortedbyfitCurrent[-lamb:]

    #Add all lambda elements from offspring
    for x in sortedbyfitOffspring:
        sortedbyfitCurrent.append(x)

    #Create population and fitness lists from 2d list
    for x in range(len(sortedbyfitCurrent)):
        population.append(sortedbyfitCurrent[x][0])
        fitness.append(sortedbyfitCurrent[x][1])
    
    return population, fitness