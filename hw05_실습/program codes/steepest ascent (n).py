import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    fileName = input("Enter the file name of a function: ")
    infile = open(fileName, 'r')
    expression = infile.readline()
    #print(expression)
    varNames =[]
    low=[]
    up=[]
    #while문 사용할 
    line = infile.readline()
    varNames.append(line.split(',')[0])
    low.append(float(line.split(',')[1]))
    up.append(float(line.split(',')[2]))

    line2 = infile.readline()
    varNames.append(line2.split(',')[0])
    low.append(float(line2.split(',')[1]))
    up.append(float(line2.split(',')[2]))
    
    #print(varNames, low, up)
    domain = [varNames, low, up]
    return expression, domain


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


def randomInit(p): ###
    init=[-5,19]
    return init    # Return a random initial point
                   # as a list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        #print('assignment', assignment)
        exec(assignment)
    #print('eval(expr)', eval(expr))
    return eval(expr)


def mutants(current, p): ###
    #mutate함수를 이용할 것
    neighbors = []
    neighbors.append(mutate(current, 0, DELTA, p))
    neighbors.append(mutate(current, 0, -DELTA, p))
    neighbors.append(mutate(current, 1, DELTA, p))
    neighbors.append(mutate(current, 1, -DELTA, p))
    print(neighbors)
    #print(current)
    #m1=mutate(current, 0, DELTA, p)
    #print(m1)
    return neighbors     # Return a set of successors


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    #evaluate를 이용할 것
    eval1 =evaluate(neighbors[0], p)
    eval2 =evaluate(neighbors[1], p)
    eval3 =evaluate(neighbors[2], p)
    eval4 =evaluate(neighbors[3], p)
    #print(eval1, eval2, eval3, eval4)
    best = neighbors[3]
    bestValue=385.6200
    return best, bestValue

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple


main()
