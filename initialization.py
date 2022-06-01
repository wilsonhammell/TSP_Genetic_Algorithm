#imports
import random


def permutation (pop_size, city_count):
    population = []

    for x in range(pop_size):
        #Append permutations representing city index, not necessary to append origin city to the end of permutation can be accounted for elsewhere
        population.append(random.sample(range(0, city_count), city_count))
    
    return population      
              
