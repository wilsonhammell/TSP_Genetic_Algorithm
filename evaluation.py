#imports
import numpy

#calculates distance between two points
def distance(point1, point2):
    return numpy.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)

def route_fitness(individual, cities):
    #value to be minimized
    fitness = 0

    #calc distance to the next city
    for x in range(len(individual)):
        #if at the last city, calc distance to starting city
        if(x==len(individual)-1):
            fitness+=distance(cities[individual[x]], cities[individual[0]])
        else:
            fitness+=distance(cities[individual[x]], cities[individual[x+1]])
    
    return fitness



