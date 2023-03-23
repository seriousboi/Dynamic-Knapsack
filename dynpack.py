from dynarray import *
from dyngraph import *



#classe d'un objet
class Item:
    def __init__(self,weight,profit,amount):
        self.weight = weight
        self.profit = profit
        self.amount = amount



#retourne une liste d'objets à partir d'une liste de triplets <poids,profit,quantité>
def getItemsFromList(itemList):
    items = [None] # /!\ l'objet 0 existe /!\
    for item in itemList:
        items += [Item(item[0],item[1],item[2])]
    return items



def readInstance(fileName):
    itemList = []
    file = open(fileName,"r")
    lines = file.readlines()
    file.close()

    nbItems = int(lines[0])
    maxCapacity = int(lines[1])
    for index,line in enumerate(lines[2:]):
        line = line.split()
        itemList += [[int(line[1]),int(line[0]),int(line[2])]]

    return getItemsFromList(itemList),maxCapacity



def arrayVsGraph(items,maxCapacity):
    print(len(items)-1,"items,",maxCapacity,"capacity")
    profit, states, arrayRunTime = solveDynArrayPack(items,maxCapacity)
    print("Array finds",profit,"in",round(arrayRunTime,2),"seconds")

    distances, predecessors, graphRunTime = solveDynGraphPack(items,maxCapacity)
    print("Graph finds",-distances[0][None],"in",round(graphRunTime,2),"seconds")
    return arrayRunTime,graphRunTime
