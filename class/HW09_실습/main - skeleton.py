from problem import Numeric, Tsp
from problem import *
from optimizer import *


def main():
    p, alg = readPlanAndCreate()  # Setup and create (problem, algorithm)
    conductExperiment(p, alg)     # Conduct experiment & produce results
    p.describe()                  # Describe the problem solved
    alg.displayNumExp()           # Total number of experiments
    #alg.displaySetting(p)          # Show the algorithm settings
    p.report()                    # Report result

def readPlanAndCreate():
    parameters = readValidPlan()  # Read and store in 'parameters'
    p = createProblem(parameters)
    alg = createOptimizer(parameters)
    return p, alg

def readValidPlan():  # Gradient Descent cannot solve TSP
    while True:
        parameters = readPlan()
        if parameters['pType'] == 2 and parameters['aType'] == 4:
            print("You cannot choose Gradient Descent")
            print("       unless your want a numerical optimization.")
        else:
            break
    return parameters

def readPlan():
    fileName = input("Enter the file name of experimental setting: ")
    infile = open(fileName, 'r')
    parameters = { 'pType':0, 'pFileName':'', 'aType':0, 'delta':0,
                   'limitStuck':0, 'alpha':0, 'dx':0, 'numRestart':0,
                   'limitEval':0, 'popSize':0, 'resolution':0, 'uXp':0,
                   'mrF':0, 'XR':0, 'mR':0, 'numExp':0 }
    parNames = list(parameters.keys())
    for i in range(len(parNames)):
        line = lineAfterComments(infile)
        #print(line)
        if parNames[i] == 'pFileName':
            parameters[parNames[i]] = line.rstrip().split(':')[-1][1:]
        else:
            parameters[parNames[i]] = eval(line.rstrip().split(':')[-1][1:])
    infile.close()
    return parameters             # Return a dictionary of parameters

def lineAfterComments(infile):    # Ignore lines beginning with '#'
    line = infile.readline()      # and then return the first line
    while line[0] == '#':         # with no '#'
        line = infile.readline()
    return line

def createProblem(parameters): ###
    # Create a problem instance (a class object) 'p' of the type as 
    # specified by 'pType', set the class variables, and return 'p'.
    pType = parameters['pType'] #problem 종류 선택
    if pType == 1:
        p = Numeric()
    elif pType == 2:
        p = Tsp()
    p.setVariables(parameters)
    return p

def createOptimizer(parameters): ###
    # Create an optimizer instance (a class object) 'alg' of the type  
    # as specified by 'aType', set the class variables, and return 'alg'.
    optimizers = {1: 'SteepestAscent()',
                  2: 'FirstChoice()',
                  3: 'Stochastic()',
                  4: 'GradientDescent()',
                  5: 'SimulatedAnnealing()',
                  6: 'GA()' }
    aType = parameters['aType'] #알고리즘 종류 선택
    alg = eval(optimizers[aType])
    alg.setVariables(parameters)
    return alg


def conductExperiment(p, alg):
    aType = alg.getAType()
    if 1 <= aType <= 4:
        alg.randomRestart(p)
    else:
        alg.run(p)
    bestSolution = p.getSolution()
    bestMinimum = p.getValue()    # First result is current best
    numEval = p.getNumEval()
    #print('bestSolution', bestSolution)
    #print('bestMinimum', bestMinimum)
    #print('numEval', numEval)
    sumOfMinimum = bestMinimum    # Prepare for averaging
    sumOfNumEval = numEval        # Prepare for averaging
    sumOfWhen = 0                 # When the best solution is found
    if 5 <= aType <= 6:
        sumOfWhen = alg.getWhenBestFound()
    numExp = alg.getNumExp()
    for i in range(1, numExp):
        if 1 <= aType <= 4:
            alg.randomRestart(p)
        else:
            #print("restart")
            alg.run(p)
        newSolution = p.getSolution()
        newMinimum = p.getValue()  # New result
        numEval = p.getNumEval()
        sumOfMinimum += newMinimum
        sumOfNumEval += numEval
        if 5 <= aType <= 6:
            sumOfWhen += alg.getWhenBestFound()
        if newMinimum < bestMinimum:
            bestSolution = newSolution  # Update the best-so-far
            bestMinimum = newMinimum
    avgMinimum = sumOfMinimum / numExp
    avgNumEval = round(sumOfNumEval / numExp)
    avgWhen = round(sumOfWhen / numExp)
    results = (bestSolution, bestMinimum, avgMinimum,
               avgNumEval, sumOfNumEval, avgWhen)
    p.storeExpResult(results)

main()

