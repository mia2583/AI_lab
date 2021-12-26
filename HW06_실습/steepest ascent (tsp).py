from problem import Tsp

def main():
    p = Tsp()
    p.setVariables()
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    #Report results
    p.report()
    
def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def bestOf(neighbors, p):
    ###
    #임의로 첫번째 이웃을 best로 설정
    best = neighbors[0]
    bestValue = p.evaluate(neighbors[0])
    i =1
    #이웃을 돌면서 가장 적은 cost을 가진 이웃을 best로 설정
    while i < len(neighbors) :
        evalVal = p.evaluate(neighbors[i])
        if(bestValue > evalVal) :
            best = neighbors[i]
            bestValue = evalVal
        i += 1
    ###
    p.storeResult(best, bestValue)  
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
