from setup import Setup
import random
import math

class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0 # _pType : 문제 종류
        self._numExp = 0

    def getPType(self):
        return self._pType
    def getNumExp(self):
        return self._numExp

    def run(self):
        pass

    def setVariables(self, parameters) :
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numRestart = parameters['numRestart']
        self._numExp = parameters['numExp']

    def displaySetting(self):
        if self._pType==1 and self._aType != 4 and self._aType != 6:
            print("Mutation step size:", self._delta)

    def displayNumExp(self):
        print("Number of experiments:", self._numExp)

#Optimizer의 상속을 받음
class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__()
        self._limitStuck = 0
        self._numRestart = 0
        
    def setVariables(self, parameters) :
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    #accessor
    def getLimitStuck(self):
        return self._limitStuck
    def getNumExp(self):
        return self._numExp

    #모든 알고리즘의 공통 출력 사항
    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2<= self._aType <=3:
            print("Max evaluations with no improvement: {0:,} iterations"
                  .format(self._limitStuck))
        ##

    def run(self):
        pass

    def randomRestart(self, p):
        i=1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        while i < self._numRestart: 
            self.run(p) #매번 새로 시도
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval = p.getNumEval()
            if newMinimum < bestMinimum:
                bestSolution = newSolution
                bestMinimum = newMinimum
            i +=1
        p.storeResult(bestSolution, bestMinimum)

#HillClimbing의 상속을 받음
class SteepestAscent(HillClimbing):
    def __init__(self):
        super().__init__()
    
    #여러 알고리즘 중 steepestAscent임을 출력
    def displaySetting(self,p):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)
        

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

#HillClimbing의 상속을 받음
class FirstChoice(HillClimbing):
    def __init__(self):
        super().__init__()

    #여러 알고리즘 중 FirstChoice임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        HillClimbing.displaySetting(self)

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

#HillClimbing의 상속을 받음
class Stochastic(HillClimbing):
    def __init__(self):
        super().__init__()

    #여러 알고리즘 중 Stochastic임을 출력
    def displaySetting(self, p):
        print()
        print("Search algorithm: Stochastic Hill Climbing")
        HillClimbing.displaySetting(self)
        
    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS < valueC: #더 나은 선택이면 현재값을 업데이트
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1
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
        i=0
        f = open('gradient.txt', 'w')
        while i < self._limitStuck:
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

#Setup의 상속을 받음
class MetaHeuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitEval = 0
        self._whenBestFound = 0

    def setVariables(self, parameters) :
        Optimizer.setVariables(self, parameters)
        self._limitEval = parameters['limitEval']
    
    #accessor
    def getLimitEval(self):
        return self._limitEval
    def getWhenBestFound(self):
        return self._whenBestFound

    #모든 알고리즘의 공통 출력 사항
    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self._limitEval))

    def run(self):
        pass

#MetaHeuristics의 상속을 받음
class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._numSample = 100

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
        print()
        MetaHeuristics.displaySetting(self)

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        best, valueBest = current, valueC
        whenBestFound = i = 1
        t = self.initTemp(p)
        f = open('anneal.txt', 'w')
        while True:
            t = self.tSchedule(t)
            if t == 0 or i==self._limitEval: #temp가 0일때까지 반복
                break
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            i +=1
            deltaE = valueS - valueC
            if deltaE < 0 : #현재값 < succesor이면 현재값을 변경 
                current = successor
                valueC = valueS
            #아니면 특정 확률로 업데이트
            elif random.uniform(0,1) < math.exp(-deltaE/t) : 
                current = successor
                valueC = valueS
            if valueC < valueBest:
                (best, valueBest) = (current, valueC)
                whenBestFound = i
                f.write(str(round(valueC,1))+ '\n')
        self._whenBestFound = whenBestFound
        f.close()
        p.storeResult(best, valueBest)

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

    def displaySetting(self, p):
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
        popBest = self.evalAndFindBest(pop, p)
        #print('pop',pop)
        best, valueBest = pop, popBest
        whenBestFound = j = 1
        while True:
            if j == self._limitEval:
                break
            newPop = []
            i=0
            while i < self._popSize: #해당 수만큼 child 생성
                par1, par2 = self.selectParents(pop)
                ch1, ch2 = p.crossover(par1, par2, self._pC)
                #mutation
                ch1 = p.mutation(ch1, self._pM)
                ch2 = p.mutation(ch2, self._pM)
                #print('ch1',ch1)
                newPop.extend([ch1, ch2])
                i+=2
            #print(newPop)
            newBest = self.evalAndFindBest(newPop, p)
            if newBest < popBest : #더 좋으면 업데이트
                pop = newPop
                popBest = newBest
            if popBest < valueBest: #가장 좋은 때 업데이트
                (best, valueBest) = (pop, popBest)
                whenBestFound = j
            j += 1
        #print('new',pop)
        self._whenBestFound = whenBestFound
        #print(valueBest)
        p.indToSol(valueBest)
        #p.storeResult(p.decode(valueBest[1]), valueBest[0])

    def evalAndFindBest(self, pop, p):
        best = pop[0]
        #print('best',best)
        p.evalInd(best)
        bestValue = best[0]
        for i in range(len(pop)):#모든 chromosome에 대해
            #print('i',i)
            ch = pop[i]
            p.evalInd(ch)
            value = ch[0]
            #print(value)
            if value < bestValue :
                best = pop[i]
                bestValue = value
        #print(bestValue)
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
