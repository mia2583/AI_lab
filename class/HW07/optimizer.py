from setup import Setup

#Setup의 상속을 받음
class HillClimbing(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0 # _pType : 문제 종류
        self._aType = 0 # _aType : 알고리즘 종류
        self._limitStuck = 100
        
    def setVariables(self, aType, pType) :
        self._pType = pType
        self._aType = aType

    def setLimitStuck(self, limit):
        self._limitStuck = limit

    #accessor
    def getPType(self):
        return self._pType
    def getAType(self):
        return self._aType
    def getLimitStuck(self):
        return self._limitStuck

    #모든 알고리즘의 공통 출력 사항
    def displaySetting(self,p):
        print()
        print("Mutation step size:", self._delta)

#HillClimbing의 상속을 받음
class SteepestAscent(HillClimbing):
    def __init__(self):
        super().__init__()
    
    #여러 알고리즘 중 steepestAscent임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        super().displaySetting(p)

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC: #현재값 < succesor이면 현재값을 변경
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
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

#HillClimbing의 상속을 받음
class FirstChoice(HillClimbing):
    def __init__(self):
        super().__init__()

    #여러 알고리즘 중 FirstChoice임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        super().displaySetting(p)

    def run(self, p):
        current = p.randomInit()   # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)     #현재값 < succesor이면 현재값을 변경 
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        p.storeResult(current, valueC)

#HillClimbing의 상속을 받음
class GradientDescent(HillClimbing):
    def __init__(self):
        super().__init__()
        self._increment = 0.0001

    #accessor
    def getIncrement(self) :
        return self._increment

    #mutator
    def setIncrement(self, incr) :
        self._increment = incr

    #여러 알고리즘 중 GradientDescent임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: Gradient-Descent Hill Climbing")
        super().displaySetting(p)
        print("Increment for calculating derivative:", self._increment)
    
    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)

        while True:
            nextP = p.takeStep(current, valueC) #deriavative, alpha
            valueN = p.evaluate(nextP)
            #서로 차이가 매우 작을때까지 반복
            if valueC - valueN < self._increment :
                break
            #아니라면 업데이트
            else :
                current = nextP
                valueC = valueN
        p.storeResult(current, valueC)
