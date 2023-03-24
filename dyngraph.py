from time import time



#classe d'un sommet état
class VertexState():
    def __init__(self,itemIndex,capacity):
        self.itemIndex = itemIndex
        self.capacity = capacity
        self.outArcs = []
        self.inArcs = []



#classe d'un arc de selection d'objets
class ItemArc():
    def __init__(self,itemIndex,amount,cost,start,end):
        self.itemIndex = itemIndex
        self.amount = amount
        self.cost = cost
        self.start = start
        self.end = end



#résout un sac à dos borné avec un PCC dans un grahe créé de manière dynamique
def solveDynGraphPack(items,maxCapacity,unbounded=False):
    startTime = time()
    if not unbounded:
        states = createGraph(maxCapacity,items)
    else:
        states = createUnboundedGraph(maxCapacity,items)
    distances, predecessors = bellman(states)
    runTime = time() - startTime
    return distances, predecessors, runTime



#crée le graphe d'état dynamiquement
def createGraph(maxCapacity,items):
    nbItems = len(items)-1 # /!\ l'objet 0 existe /!\

    startVertex = VertexState(nbItems,maxCapacity)
    states = {} #on utilise un dictionaire de dictionaire pour n'avoir que l'information qui nous intéresse
    states[nbItems] = {} #la première coordonée est l'indice de l'objet à prendre
    states[nbItems][maxCapacity] = startVertex #la seconde coordonée est la capacité restante

    for itemIndex in range(nbItems,0,-1): #états pour chaque objet
        item = items[itemIndex]
        states[itemIndex-1] = {}

        for capacity in states[itemIndex]: #états pour chaque capacité
            vertexState = states[itemIndex][capacity]

            maxAmount = min(capacity//item.weight,item.amount)

            for amount in range(maxAmount+1): #arcs pour chaque quantité d'objet possible à prendre

                if capacity-amount*item.weight in states[itemIndex-1]: # on ne recrée pas les état déjà existants
                    newVertex = states[itemIndex-1][capacity-amount*item.weight]
                else:
                    newVertex = VertexState(itemIndex-1,capacity-amount*item.weight)
                    states[itemIndex-1][capacity-amount*item.weight] = newVertex

                newArc = ItemArc(itemIndex,amount,-amount*item.profit,vertexState,newVertex) # coût négatif pour faire un PCC
                vertexState.outArcs += [newArc]
                newVertex.inArcs += [newArc]

    superSink = VertexState(0,None) #état super-puit
    for capacity in states[0]: #on relie tout les état qui ne peuvent plus prendre d'objets (itemIndex=0) au super-puit
        vertexState = states[0][capacity]
        newArc = ItemArc(0,0,0,vertexState,superSink)
        vertexState.outArcs += [newArc]
        superSink.inArcs += [newArc]
    states[0][None] = superSink

    return states



#crée le graphe d'état du sac à dos non-borné dynamiquement
def createUnboundedGraph(maxCapacity,items):
    nbItems = len(items)-1 # /!\ l'objet 0 existe /!\

    startVertex = VertexState(None,maxCapacity) #les états n'ont plus d'indice d'objet associé (None à la place) car on peut prendre d'importe quel objet à chaque étape
    states = {} #on utilise un dictionaire de dictionaire pour n'avoir que l'information qui nous intéresse
    states[None] = {} #la première coordonée est l'indice de l'objet à prendre
    states[None][maxCapacity] = startVertex #la seconde coordonée est la capacité restante

    for capacity in range(maxCapacity,0,-1): #on regarde chaque capacité dans l'odre décroissant

        if capacity in states[None]: #on ignore les états qui n'ont pas été créés
            vertexState = states[None][capacity]

            for itemIndex in range(1,nbItems+1):
                item = items[itemIndex]

                if item.weight <= capacity:

                    if capacity-item.weight in states[None]: # on ne recrée pas les état déjà existants
                        newVertex = states[None][capacity-item.weight]
                    else:
                        newVertex = VertexState(None,capacity-item.weight)
                        states[None][capacity-item.weight] = newVertex

                    newArc = ItemArc(itemIndex,1,-item.profit,vertexState,newVertex) # coût négatif pour faire un PCC
                    vertexState.outArcs += [newArc]
                    newVertex.inArcs += [newArc]

    superSink = VertexState(0,None) #état super-puit
    for capacity in states[None]: #on relie tout les état au super-puit car on peut s'arrêter de prendre des objets à tout état
        vertexState = states[None][capacity]
        newArc = ItemArc(0,0,0,vertexState,superSink)
        vertexState.outArcs += [newArc]
        superSink.inArcs += [newArc]
    states[0] = {}
    states[0][None] = superSink

    return states



#crée l'ordre topologique d'un graphe d'état
def getTopo(states):
    verticesToExplore = []

    degrees = {} #initialisation des degrés
    for itemIndex in states:
        degrees[itemIndex] = {}
        for capacity in states[itemIndex]:
            degrees[itemIndex][capacity] = len(states[itemIndex][capacity].inArcs)
            if degrees[itemIndex][capacity] == 0:
                verticesToExplore += [states[itemIndex][capacity]]

    topo = [] #construction de l'orde topologique
    while verticesToExplore != []:
        currentVertex = verticesToExplore.pop(0)
        topo += [currentVertex]

        for arc in currentVertex.outArcs:
            neighbor = arc.end
            degrees[neighbor.itemIndex][neighbor.capacity] -= 1

            if degrees[neighbor.itemIndex][neighbor.capacity] == 0:
                verticesToExplore += [neighbor]

    return topo



#fait un PCC dans un graphe d'états entre l'état ayant l'étiquette la plus basse et l'état ayant l'étiquette la plus grande
def bellman(states):
    topo = getTopo(states)

    distances = {} #initialisation des distances
    predecessors = {}
    for itemIndex in states:
        distances[itemIndex] = {}
        predecessors[itemIndex] = {}
        for capacity in states[itemIndex]:
            distances[itemIndex][capacity] = 1000000000
            predecessors[itemIndex][capacity] = None

    start = topo[0]
    distances[start.itemIndex][start.capacity] = 0

    for vertexState in topo: #PCC
        for arc in vertexState.outArcs:
            neighbor = arc.end
            if distances[neighbor.itemIndex][neighbor.capacity] > distances[vertexState.itemIndex][vertexState.capacity] + arc.cost:
                distances[neighbor.itemIndex][neighbor.capacity] = distances[vertexState.itemIndex][vertexState.capacity] + arc.cost
                predecessors[neighbor.itemIndex][neighbor.capacity] = vertexState

    return distances,predecessors
