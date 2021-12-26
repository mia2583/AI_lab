from numeric import *

def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': [expr, domain]
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def mutants(current, p):
    ###
    neighbors = []
    sign = [-1, 1]
    #모든 변수에 대해서
    for i in range(len(p[1][0])) :
        #델타의 +,-를 모두 포함한 neighbors를 생성
        for j in sign :
            neighbors.append(mutate(current,i,j*DELTA,p))
    ###
    return neighbors

def bestOf(neighbors, p):
    ###
    #임의로 첫번째 이웃을 best로 설정
    best = neighbors[0]
    bestValue = evaluate(neighbors[0], p)
    #이웃을 돌면서 가장 적은 값을 가진 이웃을 best로 설정
    for neighbor in neighbors :
        evalVal = evaluate(neighbor, p)
        if(bestValue > evalVal) :
            best = neighbor
            bestValue = evalVal
    ###
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

main()
