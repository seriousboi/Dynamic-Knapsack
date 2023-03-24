from dynarray import *
from dyngraph import *
from dynpack import *
import os



def main():
    items,maxCapacity = readInstance("kplib_student/01WeaklyCorrelated/wkcorr_50_s001.kpbd")
    print(len(items)-1,"items,",maxCapacity,"capacity")
    profit, states, arrayRunTime = solveDynArrayPack(items,maxCapacity)
    print("Array finds",profit,"in",round(arrayRunTime,2),"seconds")
    distances, predecessors, graphRunTime = solveDynGraphPack(items,maxCapacity)
    print("Graph finds",-distances[0][None],"in",round(graphRunTime,2),"seconds")
    distances, predecessors, unboundedRunTime = solveDynGraphPack(items,maxCapacity,True)
    print("Unbounded relaxation finds",-distances[0][None],"in",round(unboundedRunTime,2),"seconds")

    #runTests()



def runTests(maxSampleSize = 100):
    correlations = {"00Uncorrelated":"Uncorrelated","01WeaklyCorrelated":"Weakly correlated","02StronglyCorrelated":"Strongly correlated"}
    namesDict = getFileNamesSorted()

    for size in [50,100]:
        for directory in namesDict:
            fileNames = namesDict[directory][size]
            nbInstances = min(maxSampleSize,len(fileNames))
            fileNames = fileNames[0:nbInstances]

            print("############################################")
            print(correlations[directory],"instances of size",size)
            print()

            totalArrayRunTime = 0
            totalGraphRunTime = 0
            totalUnboundedTime = 0

            for fileName in fileNames:
                filePath = "kplib_student/"+directory+"/"+fileName
                print("Instance",fileName)
                items,maxCapacity = readInstance(filePath)
                print(len(items)-1,"items,",maxCapacity,"capacity")

                profit, states, arrayRunTime = solveDynArrayPack(items,maxCapacity)
                print("Array finds",profit,"in",round(arrayRunTime,2),"seconds")
                totalArrayRunTime += arrayRunTime

                distances, predecessors, graphRunTime = solveDynGraphPack(items,maxCapacity)
                print("Graph finds",-distances[0][None],"in",round(graphRunTime,2),"seconds")
                totalGraphRunTime += graphRunTime

                distances, predecessors, unboundedRunTime = solveDynGraphPack(items,maxCapacity,True)
                print("Unbounded relaxation finds",-distances[0][None],"in",round(unboundedRunTime,2),"seconds")
                totalUnboundedTime += unboundedRunTime

                print()

            averageArrayRunTime = totalArrayRunTime/nbInstances
            averageGraphRunTime = totalGraphRunTime/nbInstances
            averageUndoundedRunTime = totalUnboundedTime/nbInstances
            print("Results on",correlations[directory],"instances of size",size)
            print("Average array time:",round(averageArrayRunTime,2),"seconds")
            print("Average graph time:",round(averageGraphRunTime,2),"seconds")
            print("Average unbounded relaxation time:",round(averageUndoundedRunTime,2),"seconds")
            print("############################################")
            print()



def getFileNamesSorted():
    namesDict = {"00Uncorrelated":{},"01WeaklyCorrelated":{},"02StronglyCorrelated":{}}

    for directory in namesDict:
        dirPath = "kplib_student/"+directory+"/"
        fileNames = next(os.walk(dirPath), (None, None, []))[2] #one-liner qui donne la liste des fichiers dans un répertoire

        for fileName in fileNames:
            splitedName = fileName.split("_")
            size = int(splitedName[1])

            if size not in namesDict[directory]:
                namesDict[directory][size] = [fileName]
            else:
                namesDict[directory][size] += [fileName]

    return namesDict



main()
