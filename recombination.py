#imports
import random

def permutation_cut_and_crossfill (parent1, parent2):
    """cut-and-crossfill crossover for permutation representations"""

    offspring1 = []
    offspring2 = []

    #Random crossover point
    crossoverpoint = random.randint(0, len(parent1))

    #Loop through all indexes
    for x in range(len(parent1)):   
        #If left of the crossover point
        if x<crossoverpoint:
            #Offspring1 at x gets parent1 val at x and Offspring2 at x gets parent2 val at x
            offspring1.append(parent1[x])
            offspring2.append(parent2[x])
        #Else we are right of crossover point
        else:
            #Set index to current index in x
            index=x
            #Loop
            while(True):
                #If the current parent2 value isnt in offspring1 add it to the offspring and exit loop
                if not(parent2[index] in offspring1):
                    offspring1.append(parent2[index])
                    break
                #Increment
                index+=1
                #Reset index if end of parent values is reached
                if index>len(parent2)-1:
                    index=0
                #Increment index
            #Same for offspring2 and parent1
            index=x
            while(True):
                if not(parent1[index] in offspring2):
                    offspring2.append(parent1[index])
                    break
                index+=1
                if index>len(parent1)-1:
                    index=0

    return offspring1, offspring2
