import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations

def createProblem():
    ## Read in an expression and its domain from a file.
    ## Then, return a problem.
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    #파일 읽기
    fileName = input("Enter the file name of a function: ")
    infile = open(fileName, 'r')
    #expression에 object function을 string 형태로 저장
    expression = infile.readline()
    varNames=[]
    low=[]
    up = []
    line = infile.readline()
    #파일의 각줄을 읽어서 ,를 기준으로 varName과 low, up에 각각 저장
    while line != '':
        lineList = line.split(',')
        varNames.append(lineList[0])
        low.append(float(lineList[1]))
        up.append(float(lineList[2]))
        line = infile.readline()
    #다 읽은 파일 닫기
    infile.close()
    #domain 정의
    domain = [varNames, low, up]
    return expression, domain

def randomInit(p): # Return a random initial point as a list
    ###
    init = []
    #변수 수만큼 각 범위 사이에서 임의의 값을 선택
    for i in range(len(p[1][0])) :
        init.append(random.uniform(p[1][1][i], p[1][2][i]))
    ###
    return init    # list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

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

