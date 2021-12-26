from tsp import *
def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': [numCities, locations]
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def mutants(current, p): # Inversion only
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def bestOf(neighbors, p):
    ###
    #임의로 첫번째 이웃을 best로 설정
    best = neighbors[0]
    bestValue = evaluate(neighbors[0],p)
    i =1
    #이웃을 돌면서 가장 적은 cost을 가진 이웃을 best로 설정
    while i < len(neighbors) :
        evalVal = evaluate(neighbors[i], p)
        if(bestValue > evalVal) :
            best = neighbors[i]
            bestValue = evalVal
        i += 1
    ###
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
