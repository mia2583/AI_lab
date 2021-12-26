import random
import math

NumEval = 0    # Total number of evaluations


def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table

def calcDistanceTable(numCities, locations):
    ###
    table = []
    #모든 행(변수)에 대해
    for i in range(numCities):
        row = []
        #모든 열(변수)을 돌면서 행i, 열j에 i와 j점 사이의 거리를 계산
        for j in range(numCities):
            #pow는 각 점을 제곱한 값, result는 거리를 소수점1의 자리수까지 표현
            powX = (locations[i][0]-locations[j][0])*(locations[i][0]-locations[j][0])
            powY = (locations[i][1]-locations[j][1])*(locations[i][1]-locations[j][1])
            result = round(math.sqrt(powX + powY), 1)
            row.append(result)
        table.append(row)
    ###
    return table # A symmetric matrix of pairwise distances

def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init

def evaluate(current, p):
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
    global NumEval
    NumEval +=1
    cost=0
    i= 1
    while i < len(current) :
        cost += p[2][current[i-1]][current[i]]
        i +=1
    return cost

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()

