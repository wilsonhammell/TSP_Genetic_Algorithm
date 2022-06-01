# imports
import random


def tournament(fitness, mating_pool_size, tournament_size):
    """Tournament selection without replacement"""

    selected_to_mate = []

    #List to store available indexes
    indexes=list(range(0, len(fitness)))

    #Loop while the number of selected mates is less than the mating pool size
    while(len(selected_to_mate)<mating_pool_size):
        #The number of remaining indexes
        remaining=len(indexes)
        #If the number of remaining indexes is less than the tournament size, reduce the tournament size
        if(remaining<tournament_size):
            tournament_size=remaining
        #Select set of unique indexes 
        participants=(random.sample(indexes, tournament_size))
        #Track winning index
        winner=participants[0]
        #Loop through participants and find the index which corresponds to the greatest fitness
        for p in participants:
            if fitness[p]<fitness[winner]:
                winner=p
        #Sort the participants in descreasing order so we can remove the selected
        indexes.remove(winner)
        selected_to_mate.append(winner)

    return selected_to_mate
