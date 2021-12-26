from setup import Setup
import random
import math

#Setup의 상속을 받음
class HillClimbing(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0 # _pType : 문제 종류
        self._aType = 0 # _aType : 알고리즘 종류
        self._numExp = 0
        self._limitStuck = 0
        
    def setVariables(self, parameters) :
        self._pType = parameters['pType']
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']
        self._numExp = parameters['numExp']

    #accessor
    def getPType(self):
        return self._pType
    def getAType(self):
        return self._aType
    def getLimitStuck(self):
        return self._limitStuck
    def getNumExp(self):
        return self._numExp

    #모든 알고리즘의 공통 출력 사항
    def displaySetting(self,p):
        print()
        print("Number of random restarts:", self._numRestart)
        print()
        print("Mutation step size:", self._delta)
        ##

    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)

    def run(self):
        pass

    def randomRestart(self, p):
        pass

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
        p.setNumEval(0)
        valueC = p.evaluate(current)
        f = open('steepest.txt', 'w')
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            f.write(str(round(valueC,1))+'\n')
            if valueS >= valueC: #현재값 < succesor이면 현재값을 변경
                break
            else:
                current = successor
                valueC = valueS
        f.close()
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

    def randomRestart(self, p):
        for i in range(1, self._numRestart):
            self.run(p)

#HillClimbing의 상속을 받음
class FirstChoice(HillClimbing):
    def __init__(self):
        super().__init__()

    #여러 알고리즘 중 FirstChoice임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        super().displaySetting(p)
        print("Max evaluations with no improvement:", self._limitStuck, "iterations")

    def run(self, p):
        current = p.randomInit()   # 'current' is a list of values
        p.setNumEval(0)
        valueC = p.evaluate(current)
        i = 0
        f = open('first.txt', 'w')
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)     #현재값 < succesor이면 현재값을 변경 
            f.write(str(round(valueC,1))+'\n')
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        f.close()
        p.storeResult(current, valueC)

    def randomRestart(self, p):
        for i in range(1, self._numRestart):
            self.run(p)


#HillClimbing의 상속을 받음
class Stochastic(HillClimbing):
    def __init__(self):
        super().__init__()

    #여러 알고리즘 중 Stochastic임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: Stochastic Hill Climbing")
        super().displaySetting(p)
        print("Max evaluations with no improvement:", self._limitStuck, "iterations")

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        p.setNumEval(0)
        i = 0
        valueC = p.evaluate(current)
        f = open('stochastic.txt', 'w')
        while i < self._limitStuck:
            f.write(str(round(valueC,1))+'\n')
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS < valueC: #더 나은 선택이면 현재값을 업데이트
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
        f.close()
        p.storeResult(current, valueC)

# Stochastic hill climbing generates multiple neighbors and then selects
# one from them at random by a probability proportional to the quality.
# You can use the following code for this purpose.

    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]


    def randomRestart(self, p):
        for i in range(1, self._numRestart):#numRestart만큼 새로 시행
            self.run(p)

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
        print()
        print("alpha:", self._alpha)
        print("dx:", self._dx)
    
    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        p.setNumEval(0)
        valueC = p.evaluate(current)
        f = open('gradient.txt', 'w')
        i=0
        while i < self._limitEval:
            f.write(str(round(valueC,1))+'\n')
            nextP = p.takeStep(current, valueC) #deriavative, alpha
            valueN = p.evaluate(nextP)
            #서로 차이가 매우 작을때까지 반복
            if valueC - valueN < self._increment :
                break
            #아니라면 업데이트
            else :
                current = nextP
                valueC = valueN
        f.close()
        p.storeResult(current, valueC)

    def randomRestart(self, p):
        for i in range(1, self._numRestart):
            self.run(p)

#Setup의 상속을 받음
class MetaHeuristics(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0 # _pType : 문제 종류
        self._aType = 0 # _aType : 알고리즘 종류
        self._numExp = 0
        self._limitStuck = 0
        self._numSample = 0

    def setVariables(self, parameters) :
        self._pType = parameters['pType']
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']
        self._limitEval = parameters['limitEval']
        self._numExp = parameters['numExp']
        self._numSample = 100
    
    #accessor
    def getPType(self):
        return self._pType
    def getAType(self):
        return self._aType
    def getLimitStuck(self):
        return self._limitStuck
    def getNumExp(self):
        return self._numExp
    def getLimitEval(self):
        return self._limitEval

    #모든 알고리즘의 공통 출력 사항
    def displaySetting(self,p):
        print()
        print("Mutation step size:", self._delta)
        print("Max evaluations with no improvement:", self._limitStuck, "iterations")

    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)

    def run(self):
        pass

#MetaHeuristics의 상속을 받음
class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        super().__init__()
        self._temp = 0

# Simulated annealing calls the following methods.
# initTemp returns an initial temperature such that the probability of
# accepting a worse neighbor is 0.5, i.e., exp(–dE/t) = 0.5.
# tSchedule returns the next temperature according to an annealing schedule.
    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t
    
    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

    #여러 알고리즘 중 Simulated Annealing임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: Simulated Annealing")
        super().displaySetting(p)
        print("Init Temperature:", self._temp)

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        p.setNumEval(0)
        valueC = p.evaluate(current)
        self._temp = self.initTemp(p) #temp 초기화
        temp = self._temp
        i = 0
        f = open('anneal.txt', 'w')
        while i < self._limitEval:
            f.write(str(round(valueC,1))+'\n')
            temp = self.tSchedule(temp)
            if temp == 0 : #temp가 0일때까지 반복
                break
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            deltaE = valueS - valueC
            if deltaE < 0 : #현재값 < succesor이면 현재값을 변경 
                current = successor
                valueC = valueS
            else : #아니면 특정 확률로 업데이트
                probablity = random.random()
                if probablity < math.exp(-deltaE/temp) : 
                    current = successor
                    valueC = valueS
            i +=1
        f.close()
        p.storeResult(current, valueC)


class GA(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        MetaHeuristics.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        MetaHeuristics.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

    def run(self, p):
        popSize = self._popSize
        pop = p.initializePop(popSize)
        print('pop',pop)
        best = self.evalAndFindBest(pop, p)
        #par1, par2 = self.selectParents(pop)

        newPop = []
        i=0
        while i < self._popSize:
            print('i ', i)
            par1, par2 = self.selectParents(pop)
            ch1, ch2 = p.crossover(par1, par2, self._pC)
            #mutation
            newPop.extend([ch1, ch2])
            i+=2
            print('newPop', newPop)
        #ch1, ch2 = p.crossover(par1, par2, self._pC)
        #print('par', par1, par2)
        #print('ch', ch1, ch2)

    '202055516 김명서 2021.11.25 출석체크'
    def evalAndFindBest(self, pop, p):
        best = pop[0]
        p.evalInd(best)
        bestValue = best[0]
        #print('best',best, 'bestValue', bestValue)
        return best
        #제일 낮은것이 return되도록 함

    def selectParents(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1, ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1, ind2)
        #print('pop', pop, ' parent', par1, par2)
        return par1, par2

    def selectTwo(self, pop):
        popCopy = pop[:]
        random.shuffle(popCopy)
        return popCopy[0], popCopy[1]

    def binaryTournament(self, ind1, ind2):
        if ind1[0] < ind2[0]:
            return ind1
        else : 
            return ind2