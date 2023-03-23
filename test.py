from dynpack import *
import os


itemList = [[2,5,2],[3,7,1],[7,9,3]]


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

            for fileName in fileNames:
                filePath = "kplib_student/"+directory+"/"+fileName
                print("Instance",fileName)


                items,maxCapacity = readInstance(filePath)
                arrayRunTime,graphRunTime = arrayVsGraph(items,maxCapacity)
                totalArrayRunTime += arrayRunTime
                totalGraphRunTime += graphRunTime

                print()

            averageArrayRunTime = totalArrayRunTime/nbInstances
            averageGraphRunTime = totalGraphRunTime/nbInstances
            print("Results on",correlations[directory],"instances of size",size)
            print("Average array time:",round(averageArrayRunTime,2),"seconds")
            print("Average graph time:",round(averageGraphRunTime,2),"seconds")
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



runTests(2)
