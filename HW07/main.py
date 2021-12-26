from problem import *
from optimizer import *

#풀고자하는 문제 입력
def selectProblem():
    print("Select the problem type:")
    print(" 1. Numerical Optimization")
    print(" 2. TSP")
    pType = int(input("Enter the number: "))
    if pType == 1:
        p = Numeric()
    elif pType == 2 :
        p = Tsp()
    return p, pType

#사용하고자하는 알고리즘 선택
def selectAlgorithm(pType):
    print()
    print("Select the search algorithm:")
    print(" 1. Steepest-Ascent")
    print(" 2. First-Choice")
    print(" 3. Gradient Descent")
    aType = int(input("Enter the number: "))
    optimizers = { 1: 'SteepestAscent()',
                   2: 'FirstChoice()',
                   3: 'GradientDescent()'}
    invalid(pType, aType) # tsp+gradient가 선택되었을 때
    alg = eval(optimizers[aType])
    alg.setVariables(aType, pType)
    return alg

#tsp문제는 gradient descent에 적용하지 못함.
def invalid(pType, aType):
    if pType == 2 and aType == 3 :
        print("You cannot choose Gradient Descent with TSP")
        exit()

def main() :
    p, pType = selectProblem() 
    p.setVariables() # 문제 파일 입력받기
    alg = selectAlgorithm(pType)
    alg.run(p) #알고리즘 실
    p.describe() #현재 문제 나열
    alg.displaySetting(p)
    p.report() #결과 출력
    

main()
