import random
import math
from setup import Setup

#Setup의 상속을 받음
class Problem(Setup):
    def __init__(self):
        super().__init__()
        #self._solution = []
        #self._value = 0
        self._numEval = 0
        self._avgMinimum =0
        self._avgNumEval =0
        self._sumOfNumEval = 0
        self._avgWhen = 0
        self._pFileName =""
        self._bestSolution = []
        self._bestMinimum = 0


    # accessor
    def getSolution(self):
        return self._bestSolution
    def getValue(self):
        return self._bestMinimum
    def getNumEval(self):
        return self._numEval
    
    #mutator
    def setNumEval(self, numEval) :
        self._numEval = numEval
    def addNumEval(self, cnt=0) :
        self._numEval += cnt
    def storeResult(self, solution, value) :
        self._bestSolution = solution
        self._bestMinimum = value

    #필요 변수들 저장하기
    def storeExpResult(self, results):
        self._bestSolution = results[0]
        self._bestMinimum = results[1]
        self._avgMinimum =results[2]
        self._avgNumEval =results[3]
        self._sumOfNumEval = results[4]
        self._avgWhen = results[5]

    #필요 변수들 읽어오기
    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pFileName = parameters['pFileName']

    #결과 출력
    def report(self):
        aType = self._aType
        if 1 <= aType <= 4:
            print("Average number of evaluations: {0:,}"
                  .format(round(self._avgNumEval)))
        if 5 <= aType <= 6:
            print("Average iteration of finding the best: {0:,}"
                  .format(round(self._avgWhen)))
        print()
        
    def reportNumEvals(self):
        if 1 <= self._aType <= 4:
            print()
            print("Total number of evaluations: {0:,}"
                  .format(self._sumOfNumEval))

class Numeric(Problem) :
    def __init__(self):
        super().__init__()
        self._domain = []
        self._expression = ' '

        #gradient Descent
        #self._dx = 0.01
        #self._alpha = 0.01
        
    # accessor
    def getDomain(self):
        return self._domain
    def getExpression(self):
        return self._expression

    #mutator
    def setDomain(self, domain):
        self._domain = domain
    def setExpression(self, expression):
        self._expression = expression

    def takeStep(self, x, v) :
        #미분값을 구한후 알파를 곱해 범위확인
        grad = self.gradient(x, v)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self._alpha * grad[i]
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self, x, v) :
        grad = []
        #모든 변수에 대해 gradient
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self._dx
            g = (self.evaluate(xCopyH) - v) / self._dx
            grad.append(g)
        return grad

    def isLegal(self, x) :
        domain = self._domain        # [VarNames, low, up]
        low = domain[1]
        up = domain[2]
        flag = True
        #모든 변수들에 대해 범위에 존재하는지 확인
        for i in range(len(low)) :
            if x[i] < low[i] or up[i] < x[i]:
                flag = False
                break
        return flag
        
    def setVariables(self, parameters):
        Problem.setVariables(self, parameters)
        infile = open(self._pFileName, 'r')
        #expression에 object function을 string 형태로 저장
        self._expression = infile.readline()
        varNames=[]
        low=[]
        up = []
        line = infile.readline()
        #파일의 각줄을 읽어서 ,를 기준으로 varName과 low, up에 각각 저장
        while line != '':
            lineList = line.split(',')
            varNames.append(lineList[0])
            low.append(float(lineList[1]))
            up.append(float(lineList[2]))
            line = infile.readline()
        #다 읽은 파일 닫기
        infile.close()
        #domain으로 저장
        self._domain = [varNames, low, up]

    def randomInit(self): # Return a random initial point as a list
        ###
        domain = self._domain
        low, up = domain[1], domain[2]
        init = []
        #변수 수만큼 각 범위 사이에서 임의의 값을 선택
        for i in range(len(low)):
            init.append(random.uniform(low[i], up[i]))
        ###
        return init    # list of values

    def evaluate(self, current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        self.addNumEval(1)
        domain = self._domain
        expr = self._expression      # function expression
        varNames = domain[0]  # domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain        # [VarNames, low, up]
        l = domain[1][i]     # Lower bound of i-th
        u = domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        domain = self._domain
        varNames = domain[0] # p[1] is domain: [VarNames, low, up]
        low = domain[1]
        up = domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 

    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        Problem.report(self)
        print("Best solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self._bestMinimum) )
        Problem.reportNumEvals(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)  # Convert the list to a tuple

    #FCHC-N
    def randomMutant(self, current):
        ###
        #0부터 변수 수 사이에서 무작위로 한개의 숫자 선택
        domain = self._domain
        i= random.randrange(len(domain[0]))
        sign = [-1, 1]
        #델타의 부호를 선택
        d= random.choice(sign)*self._delta
        ###
        return self.mutate(current, i, d)

    #SAHC-N
    def mutants(self, current):
        ###
        neighbors = []
        sign = [-1, 1]
        domain = self._domain
        #모든 변수에 대해서
        for i in range(len(domain[0])) :
            #델타의 +,-를 모두 포함한 neighbors를 생성
            for j in sign :
                neighbors.append(self.mutate(current,i,j*self._delta))
        ###
        return neighbors

    def initializePop(self, size):
        pop = []
        for i in range(size):
            chromosome = self.randBinStr()
            #pop.append([0, chromosome])
            pop.append([0, chromosome])
            # 앞에 0은 fitness(=evaluation값)
        return pop

    def randBinStr(self):
        k = len(self._domain[0]) * self._resolution
        chromosome = []
        for i in range(k):
            allele = random.randint(0,1)
            chromosome.append(allele)
        #print(chromosome)
        return chromosome
    #allele = 대립 유전자

    def evalInd(self, ind): #ind = [fitness, chromosome]
        ind[0] = self.evaluate(self.decode(ind[1]))

    def decode(self, chromosome):
        r = self._resolution
        low = self._domain[1]
        up = self._domain[2]
        genotype = chromosome[:]
        phenotype = []
        start=0
        end =r
        for var in range(len(self._domain[0])):
            value = self.binaryToDecimal(genotype[start:end],
                            low[var], up[var])
            phenotype.append(value)
            start += r
            end += r
        #print('chromosome', chromosome, '=>phenotype', phenotype)
        return phenotype
        #genotype = 유전자형(binary), phenotype = 표현형(decimal)

    def binaryToDecimal(self, binCode, l, u):
        r = len(binCode)
        decimalValue = 0
        for i in range(r):
            decimalValue += binCode[i] * (2 ** (r- 1 - i))
            #print('binCode',binCode,' decimalValue', decimalValue)
            #print('decimalValue', decimalValue, l + (u - l) * decimalValue / 2 ** r)
        return l + (u - l) * decimalValue / 2 ** r

    def crossover(self, ind1, ind2, uXp):
        chr1, chr2 = self.uXover(ind1[1], ind2[1], uXp)
        return [0, chr1], [0, chr2]

    def uXover(self, chrInd1, chrInd2, uXp):
        chr1 = chrInd1[:]
        chr2 = chrInd2[:]
        for i in range(len(chr1)):
            if random.uniform(0,1) < uXp:
                chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2

    def mutation(self, ind, mrF):
        L = len(self._domain[0]) * self._resolution
        if random.uniform(0,1) < mrF/L:
            i = random.randrange(0,len(ind[1]))
            if ind[1][i]==0 :
                ind[1][i] = 1
            else :
                ind[1][i] = 0
        return ind

    def indToSol(self, ind):
        self._bestSolution = self.decode(ind[1])
        self._bestMinimum = ind[0]



class Tsp(Problem):
    def __init__(self):
        super().__init__()
        self._numCIties = 0
        self._locations = []
        self._table = []

    # accessor
    def getNumCities(self):
        return self._numCities
    def getLocations(self):
        return self._locations
    def getTable(self):
        return self._table 

    #mutator
    def setNumCities(self, numCities):
        self._numCities = numCities
    def setLocation(self, line):
        self._locations.append(eval(line))
    def setTable(self, row):
        self._table.append(row)

    def setVariables(self, parameters):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        Problem.setVariables(self, parameters)
        infile = open(self._pFileName, 'r')
        # First line is number of cities
        self._numCities = int(infile.readline())
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self.setLocation(line) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.calcDistanceTable()
        #return numCities, locations, table

    def calcDistanceTable(self):
        ###
        #모든 행(변수)에 대해
        for i in range(self._numCities):
            row = []
            #모든 열(변수)을 돌면서 행i, 열j에 i와 j점 사이의 거리를 계산
            for j in range(self._numCities):
                #pow는 각 점을 제곱한 값, result는 거리를 소수점1의 자리수까지 표현
                powX = (self._locations[i][0]-self._locations[j][0])*(self._locations[i][0]-self._locations[j][0])
                powY = (self._locations[i][1]-self._locations[j][1])*(self._locations[i][1]-self._locations[j][1])
                result = round(math.sqrt(powX + powY), 1)
                row.append(result)
            self.setTable(row)
        ###
        #return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self._numCities
        init = list(range(n)) #무작위로 생성
        random.shuffle(init)
        return init

    def evaluate(self, current):
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        self.addNumEval(1)
        cost=0
        i= 1
        while i < len(current) :
            cost += self._table[current[i-1]][current[i]]
            i +=1
        return cost

    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()
        print()

    def report(self):
        print()
        print("Average tour cost: {0:,}".format(round(self._avgMinimum)))
        Problem.report(self)
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._bestMinimum)))
        Problem.reportNumEvals(self)

    def tenPerRow(self):
        for i in range(len(self._bestSolution)):
            print("{0:>5}".format(self._bestSolution[i]), end='')
            if i % 10 == 9:
                print()

    #FCHC-Tsp
    def randomMutant(self, current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self._numCities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    #SAHC-Tsp
    def mutants(self, current): # Inversion only
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors


    def initializePop(self, size):   # Return a random initial tour
        pop = []
        for i in range(size): # 사이즈 만큼 chromosome생성
            chromosome = self.randomInit()
            pop.append([0, chromosome])
        #print('pop',pop)
        return pop
    
    def evalInd(self, ind): #ind = [fitness, chromosome]
        ind[0] = self.evaluate(ind[1]) #fitness값 구하기
        #print(ind)

    def crossover(self, ind1, ind2, XR):
        chr1, chr2 = self.oXover(ind1[1], ind2[1])
        return [0, chr1], [0, chr2]

    def oXover(self, chrInd1, chrInd2) :
        chr1 = chrInd1[:]
        chr2 = chrInd2[:]
        cut1 = random.randrange(len(chr1))
        cut2 = random.randrange(len(chr1))
        #자를 두 위치 선정
        while cut1 == cut2:
            cut2 = random.randrange(len(chr1))
        if cut1 > cut2 :
            (cut1, cut2) = (cut2, cut1)
        for i in range(len(chr1)):
            if cut1 <= i <=  cut2 : #두 위치 사이면 서로 교환 
                chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2

    def mutation(self, ind, mR):
        L = len(ind[1]) * self._resolution
        if random.uniform(0,1) < mR/L: #매우 적은 확률로 교환(mutate)
            i1 = random.randrange(0,len(ind[1]))
            i2 = random.randrange(0,len(ind[1]))
            (ind[1][i1], ind[1][i2]) = (ind[1][i2], ind[1][i1])
        return ind

    def indToSol(self, ind): #결과 저장
        self._bestSolutionn = ind[1]
        self._bestMinimum = ind[0]
