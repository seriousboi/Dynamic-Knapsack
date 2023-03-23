from copy import copy
from time import time



#classe d'un état
class State():
    def __init__(self,profit,itemsTaken):
        self.profit = profit
        self.itemsTaken = itemsTaken



#résout un problème de sac à dos en remplissant un tableau d'états dynamiquement
def solveDynArrayPack(items,maxCapacity):
    startTime = time()

    nbItems = len(items)-1 # /!\ l'objet 0 existe /!\
    states = [[None]*(maxCapacity+1) for capacity in range(nbItems+1)]

    for itemIndex in range(nbItems+1):
        for capacity in range(maxCapacity+1):

            if  states[itemIndex][capacity] == None:
                states[itemIndex][capacity] = getState(itemIndex,capacity,items,states)

    runTime = time() - startTime
    return states[nbItems][maxCapacity].profit, states, runTime



#calcule un état
def getState(itemIndex,capacity,items,states):
    nbItems = len(items)
    item = items[itemIndex]

    if capacity == 0 or itemIndex == 0:
        return State(0,[0]*nbItems)

    bestProfit = -1
    maxAmount = min(capacity//item.weight,item.amount)
    for amount in range(maxAmount+1):

        capacityLeft = capacity - item.weight*amount
        neighborState = states[itemIndex-1][capacityLeft]

        profit = item.profit*amount + neighborState.profit
        if profit > bestProfit:
            bestProfit = profit
            bestState = neighborState
            amountToTake = amount

    itemsTaken = copy(bestState.itemsTaken)
    itemsTaken[itemIndex] += amountToTake
    return State(bestProfit,itemsTaken)
