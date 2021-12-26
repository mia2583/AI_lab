from problem import *
from optimizer import *

def selectProblem():
    print("Select the problem type:")
    print(" 1. Numerical Optimization")
    print(" 2. TSP")
    pType = int(input("Enter the number: "))
    if pType == 1:
        p = Numeric()
    return p, pType

'''def selectAlgorithm(pType):
    print()
    print("Select the search algorithm:")
    print(" 1. Steepest-Ascent")
    aType = int(input("Enter the number: "))
    optimizers = { 1: 'SteepestAscent()'}
    alg = optimizers[aType]
    return alg'''

def selectAlgorithm(pType):
    print()
    print("Select the search algorithm:")
    print(" 1. Steepest-Ascent")
    print(" 2. First-Choice")
    print(" 3. Gradient Descent")
    aType = int(input("Enter the number: "))
    optimizers = { 1: 'SteepestAscent()',
                   2: 'First-Choice()',
                   3: 'Gradient Descent()'}
    #alg = optimizers[aType]
    alg = eval(optimizers[aType])
    alg.setVariables(aType, pType)
    return alg
    '2021.11.11 출석체크 202055516 김명서'

'''def invalid(pType, aType):
    ###
    #code
    ###'''

def main() :
    p, pType = selectProblem()
    print(p, pType)
    alg = selectAlgorithm(pType)
    print(alg)
    alg.displaySetting()

main()