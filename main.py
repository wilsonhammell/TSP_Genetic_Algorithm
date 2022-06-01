"""
A genetic algorithm for travelling salesmen problem
"""

# imports
import random
import numpy
import time
import networkx
import matplotlib.pyplot
from python_tsp.exact import solve_tsp_dynamic_programming

# import your own modules
import initialization
import evaluation
import parent_selection
import recombination
import mutation
import survivor_selection

#function to read city coordinates
def readData(filename):
    with open(filename) as doc:
        lines = doc.readlines()
    cities=[]

    for line in lines[1:]:
        temp=line.split()
        cities.append((int(temp[0]), int(temp[1])))
    
    return cities

#function to create random city coordinates
def randomCities(num):
    cities=[]
    for x in range(num):
        cities.append((random.randint(0,100), random.randint(0,100)))
    return cities

dp_cities=[]
#flag for random city generation and number of random cities
def main(user_inputs):
    random.seed()
    numpy.random.seed()

    global dp_cities

    #generate or read cities
    if(user_inputs[0]==2):
        selectedFile=''
        while True:
            selectedFile = input("Enter the file name containing city coordinates with file extension, leave blank for default:")
            if(selectedFile==''):
                cities=readData('examplecitydata/example.txt')
                break
            else:
                try:
                    cities=readData('examplecitydata/'+selectedFile)
                    break
                except:
                    print("No such file, please try again")
    else:
        cities=randomCities(user_inputs[1])
    dp_cities=cities.copy()
    city_count = len(cities)

    #create a dict of cities for node labeling later
    citydict = {}
    for x in range(city_count):
        citydict[len(citydict)]=cities[x]

    #set specifications
    popsize = user_inputs[3]  
    mating_pool_size = int(popsize*0.2)
    tournament_size = 4
    xover_rate = user_inputs[5]
    mut_rate = user_inputs[4]
    gen_limit = user_inputs[2]

    #track the time and generation count
    start = time.time()
    gen = 0 
    #initialize population
    population = initialization.permutation(popsize, city_count)
    #get initial fitness values
    fitness = []
    for i in range (0, popsize):
        fitness.append(evaluation.route_fitness(population[i], cities))
    print("\n\nGenetic algorithm approach:")
    print("Generation Limit:", user_inputs[2])
    print("Population Size:", user_inputs[3])
    print("Mutation Rate:", user_inputs[4])
    print("Crossover Rate:", user_inputs[5])
    print("Generation", gen, ": Best fitness", min(fitness), "\tAverage fitness", sum(fitness)/len(fitness))

    #append to the graph the current shortest distance
    graphgrowth=[]
    graphgrowth.append(min(fitness))
    #evolution begins
    while gen < gen_limit:
        #pick parents 
        parents_index = parent_selection.tournament(fitness, mating_pool_size, tournament_size)

        #shuffle order
        random.shuffle(parents_index)
    
        #reproduction
        offspring =[]
        offspring_fitness = []
        i= 0 
        
        #offspring are generated using selected parents in the mating pool
        while len(offspring) < mating_pool_size:
            #recombination
            if random.random() < xover_rate:           
                off1,off2 = recombination.permutation_cut_and_crossfill(population[parents_index[i]], population[parents_index[i+1]])
            else:
                off1 = population[parents_index[i]].copy()
                off2 = population[parents_index[i+1]].copy()
            #mutation
            if random.random() < mut_rate:
                off1 = mutation.permutation_swap(off1)
            if random.random() < mut_rate:
                off2 = mutation.permutation_swap(off2)
        
            #store offspring
            offspring.append(off1)
            offspring_fitness.append(evaluation.route_fitness(off1, cities))
            offspring.append(off2)
            offspring_fitness.append(evaluation.route_fitness(off2, cities))

            i = i+2 
        #perform replacement with offspring
        population, fitness = survivor_selection.replacement(population, fitness, offspring, offspring_fitness)
        
        #graph the current best distance
        graphgrowth.append(min(fitness))
        #update generation count
        gen = gen + 1

        #print updates every 100 generations
        if(gen%100==0):
            print("generation", gen, ": best fitness", min(fitness), "average fitness", sum(fitness)/len(fitness))
    #record time when evolution ended
    end = time.time()
    #find the unique routes with the lowest distance
    solutions=[]
    for i in range (0, popsize):
        if fitness[i] == min(fitness):
            if not (population[i] in solutions):
                solutions.append(population[i])

    #if cities were randomly generated provide their coordinates
    if(user_inputs[0]==1):
        print("The randomly generated city coordinates were:")
        i=0
        for x in cities:
            print("City:", i, x)
            i+=1

    #output run results
    print("The shortest distance found to travel to all cities was", min(fitness))
    print("Routes with this distance:")
    for i in range(len(solutions)):
        print(solutions[i])
    print("Total time elapsed:", round(end-start, 2), "seconds\n\n\n")

    #create a directed graph to allow for visual inspection of provided route
    graph = networkx.DiGraph()
    #add nodes
    for x in solutions[0]:
        graph.add_node(x, pos=citydict[x])

    #add edges
    for i in range(len(solutions[0])):
        if (i==len(solutions[0])-1):
            graph.add_edge(solutions[0][i], solutions[0][0])
        else:
            graph.add_edge(solutions[0][i], solutions[0][i+1])

    pos=networkx.get_node_attributes(graph, 'pos')

    matplotlib.pyplot.figure(1,figsize=(8,8)) 
    networkx.draw_networkx_nodes(graph, pos, node_size=100)
    networkx.draw_networkx_labels(graph, pos, font_size=6)
    networkx.draw_networkx_edges(graph, pos, arrows=True)
    matplotlib.pyplot.xlabel('Directed graph of one of shortest routes found\nClose to see progress graph')
    matplotlib.pyplot.show()

    #graph the fitness progress with respect to generations to visualize details like convergence
    matplotlib.pyplot.plot(graphgrowth)
    matplotlib.pyplot.ylabel('Distance of shortest route')
    matplotlib.pyplot.xlabel('Generations')
    matplotlib.pyplot.show()

# end of main

#alternative DP approach to find exact answer
def tspDP(user_inputs):
    random.seed()
    numpy.random.seed()

    #get the same set of cities the genetic algorithm used
    cities=dp_cities.copy()
    city_count = len(cities)

    #creating a dictornary of cities for node labeling later
    citydict = {}
    for x in range(city_count):
        citydict[len(citydict)]=cities[x]

    #create a distance matrix from the cities provided
    distance_matrix=numpy.zeros((city_count,city_count))
    for x in range(city_count):
        for y in range(city_count):
            distance_matrix[x][y]=evaluation.distance(cities[x],cities[y])

    print("Exact approach using dynamic programming:")
    #track start time
    start=time.time()
    if(city_count>15):
        print("Calculating optimal path, this may time a while")

    #calculate the optimal path using dynamic programming
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)

    #record end time
    end=time.time()

    #print city coordinates if generated
    if(user_inputs[0]==1):
        print("The randomly generated city coordinates were:")
        i=0
        for x in cities:
            print("City:", i, x)
            i+=1    

    #print results
    print("The optimal route has distance", distance, "and is:")
    print(permutation)
    print("Total time elapsed:", round(end-start, 2), "seconds")

    #graph the optimal route found above
    graph = networkx.DiGraph()
    #add nodes
    for x in permutation:
        graph.add_node(x, pos=citydict[x])

    #add edges
    for i in range(len(permutation)):
        if (i==len(permutation)-1):
            graph.add_edge(permutation[i], permutation[0])
        else:
            graph.add_edge(permutation[i], permutation[i+1])

    pos=networkx.get_node_attributes(graph, 'pos')

    matplotlib.pyplot.figure(1,figsize=(8,8)) 
    networkx.draw_networkx_nodes(graph, pos, node_size=100)
    networkx.draw_networkx_labels(graph, pos, font_size=6)
    networkx.draw_networkx_edges(graph, pos, arrows=True)
    matplotlib.pyplot.xlabel('Directed graph of one of optimal routes found')
    matplotlib.pyplot.show()



user_inputs=[0,0,1000,200,0.8,0.8]
while(True):
    user_in=input("Enter 1 for randomly generated cities or 2 to read coordinates from a file:")

    if(user_in=="1" or user_in=="2"):
        user_inputs[0]=int(user_in)
        break
    else:
        print("Invalid selection")
if(user_inputs[0]==1):
    while(True):
        user_in=input("\nEnter the number of random cities you want generated (Value must be greater than 2, 20+ may require more generations and a larger population for good results):")
        if(user_in.isnumeric() and int(user_in)>2):
            user_inputs[1]=int(user_in)
            break
        else:
            print("Invalid input, please enter a numeric value that is greater than 2")
custom_settings=False
while(True):
    user_in=input("\nEnter 1 for to use default algorithm settings or enter 2 to choose custom values:")
    if(user_in=="1"):
        break
    elif(user_in=="2"):
        custom_settings=True
        break
    else:
        print("Invalid selection")
if(custom_settings):
    while(True):
        user_in=input("\nEnter the number of generations (Default is 1000):")
        if(user_in.isnumeric() and int(user_in)>0):
            user_inputs[2]=int(user_in)
            break
        else:
            print("Invalid input, please enter a numeric value that is greater than 0")
    while(True):
        user_in=input("\nEnter the population size (Default is 200):")
        if(user_in.isnumeric() and int(user_in)>10):
            user_inputs[3]=int(user_in)
            break
        else:
            print("Invalid input, please enter a numeric value that is greater than 10")
    while(True):
        user_in=input("\nEnter the mutation rate, increasing this can reduce premature convergence (Default is 0.8 representing an 80% mutation rate):")
        if(user_in.isnumeric() and int(user_in)>=0 and int(user_in)<=1):
            user_inputs[4]=int(user_in)
            break
        else:
            print("Invalid input, please enter a numeric value that is between 0 and 1")
    while(True):
        user_in=input("\nEnter the crossover rate, increasing this can reduce premature convergence (Default is 0.8 representing an 80% crossover rate):")
        if(user_in.isnumeric() and int(user_in)>=0 and int(user_in)<=1):
            user_inputs[5]=int(user_in)
            break
        else:
            print("Invalid input, please enter a numeric value that is between 0 and 1")
use_DP=True
print("\n\nAlso find the exact answer using dynamic programing?")
print("Note:Using dynamic programming to solve TSP problem with more than 20 cities will almost certainly stall youre computer\nOnly use values this high with a powerful processor, lots of memory and time to kill")
while(True):
    user_in=input("Enter 1 to also solve with DP enter 2 to skip solving with DP:")
    if(user_in=="1"):
        break
    elif(user_in=="2"):
        custom_settings=False
        break
    else:
        print("Invalid selection")

main(user_inputs)
if(use_DP):
    tspDP(user_inputs)
input('Press ENTER to exit')



