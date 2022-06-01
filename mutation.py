# imports
import random

def permutation_swap (individual):
    """Mutate a permutation"""

    mutant = individual.copy()

    #Pick two random locations
    locations=random.sample(range(0, len(individual)), 2)
    #Swap their values
    mutant[locations[0]],mutant[locations[1]] = mutant[locations[1]],mutant[locations[0]]
    
    return mutant

