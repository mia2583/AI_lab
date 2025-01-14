from problem import Numeric

def main():
    p = Numeric()
    p.setVariables() # 파일로부터 정보 받아오기
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe() #현재 문제 나열
    displaySetting(p) #지정 사항 출력
    # Report results
    p.report()
    
def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC: #현재값 < succesor이면 현재값을 변경
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)
    #return current, valueC

def bestOf(neighbors, p):
    ###
    #임의로 첫번째 이웃을 best로 설정
    best = neighbors[0]
    bestValue = p.evaluate(neighbors[0])
    #이웃을 돌면서 가장 적은 값을 가진 이웃을 best로 설정
    for neighbor in neighbors :
        evalVal = p.evaluate(neighbor)
        if(bestValue > evalVal) :
            best = neighbor
            bestValue = evalVal
    ###
    return best, bestValue

def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()
