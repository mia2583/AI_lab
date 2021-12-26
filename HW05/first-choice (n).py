from numeric import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': [expr, domain]
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)     #현재값 < succesor이면 현재값을 변경 
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC

def randomMutant(current, p):
    ###
    #0부터 변수 수 사이에서 무작위로 한개의 숫자 선택
    i= random.randrange(len(p[1][0]))
    sign = [-1, 1]
    #델타의 부호를 선택
    d= random.choice(sign)*DELTA
    ###
    return mutate(current, i, d, p)

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

main()

