from dynarray import *
from dyngraph import *



def main():
    #itemList = [[2,5,2],[3,7,1],[7,9,3]]
    items,maxCapacity = readInstance("kplib_student/01WeaklyCorrelated/wkcorr_50_s004.kpbd")
    #arrayVsGraph(items,maxCapacity)
    distances, predecessors, runTime = solveDynGraphPack(items,maxCapacity)
    print("graph finds",-distances[0][None],"in",round(runTime,5),"seconds")




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
    profit, states, runTime = solveDynArrayPack(items,maxCapacity)
    print("array finds",profit,"in",round(runTime,5),"seconds")

    distances, predecessors, runTime = solveDynGraphPack(items,maxCapacity)
    print("graph finds",-distances[0][None],"in",round(runTime,5),"seconds")



main()
