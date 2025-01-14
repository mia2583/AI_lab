from problem import Numeric

def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()
    # Call the search algorithm
    gradientDescent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def gradientDescent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)

    while True:
        nextP = p.takeStep(current) #deriavative, alpha
        valueN = p.evaluate(nextP)
        #서로 차이가 매우 작을때까지 반복
        if valueC == valueN :
            break
        #아니라면 업데이트
        else :
            current = nextP
            valueC = valueN
    p.storeResult(current, valueC)

def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Alpha rate:", p.getAlpha())

main()

