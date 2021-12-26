from problem import Tsp

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    p = Tsp()
    p.setVariables() # 파일로부터 정보 받아오기
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()
    
def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)  #현재값 < succesor이면 현재값을 변경
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC)

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")

main()

