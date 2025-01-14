from problem import Numeric

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    p = Numeric()
    p.setVariables() # 파일로부터 정보 받아오기
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describe() #현재 문제 나열
    displaySetting(p) #지정 사항 출력
    # Report results
    p.report()
    
def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)     #현재값 < succesor이면 현재값을 변경 
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC)

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())
    print("Max evaluations with no improvement: {0:,} iterations".format(LIMIT_STUCK))

main()

