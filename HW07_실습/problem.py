import random
import math

class Problem():
    def __init__(self):
        self._solution = []
        self._value = 0
        self._numEval = 0

    # accessor
    def getNumEval(self):
        return self._numEval
    def getSolution(self):
        return self._solution
    def getValue(self):
        return self._value
    
    #mutator
    def setNumEval(self, cnt=0) :
        self._numEval += cnt
    def storeResult(self, solution, value) :
        self._solution = solution
        self._value = value
    #결과 출력
    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))




class Numeric(Problem) :
    def __init__(self):
        super().__init__()
        self._domain = []
        self._expression = ' '
        self._delta = 0.01

        #gradient Descent
        self._dx = 0.01
        self._alpha = 0.01
        
    # accessor
    def getDomain(self):
        return self._domain
    def getExpression(self):
        return self._expression
    def getDelta(self):
        return self._delta
    def getDx(self):
        return self._dx
    def getAlpha(self) :
        return self._alpha

    #mutator
    def setDomain(self, domain):
        self._domain = domain
    def setExpression(self, expression):
        self._expression = expression
    def getDelta(self, delta):
        self._delta = delta
    def getDx(self, dx):
        self._dx = dx
    def getAlpha(self, alpha) :
        self._alpha = alpha

    def takeStep(self, current):
        #미분값을 구한후 알파를 곱해 범위확인
        expr = self.gradient(current)
        current = self.isLegal(expr, current)
        return current

    def functionF(self, expr, current) :
        #numEval을 증가시키지 않는 evaluate함수
        domain = self._domain
        varNames = domain[0]  # domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def gradient(self, current):
        domain = self._domain
        expr = '0'      #gradient한 후의 expression
        expression = self._expression
        varNames = domain[0]  # domain: [varNames, low, up]
        #모든 변수에 대해 gradient
        for i in range(len(varNames)):
            replacement = "(" + varNames[i] + "+" + str(self._dx) + ")"
            expr += "+("+expression.replace(varNames[i], replacement)+ \
                    "-("+self._expression+")) /"+ str(self._dx)
        return expr #gradient한 후의 expression
        ###

    def isLegal(self, expr, current) :
        domain = self._domain        # [VarNames, low, up]
        curCopy = current[:]
        #모든 변수들에 대해 범위에 존재하는지 확인
        for i in range(len(domain[0])) :
            l = domain[1][i]     # Lower bound of i-th
            u = domain[2][i]     # Upper bound of i-th
            if l <= current[i] - self._alpha*self.functionF(expr, current) <= u:
                curCopy[i] = current[i] - self._alpha*self.functionF(expr, current)
        return curCopy
        
        
    def setVariables(self):
        fileName = input("Enter the file name of a function: ")
        infile = open(fileName, 'r')
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
        self.setNumEval(1)
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
        print("Solution found:")
        print(self.coordinate( self._solution ))  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value) )
        super().report()

    def coordinate(self, solution):
        c = [round(value, 3) for value in solution]
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

    def setVariables(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
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
        self.setNumEval(1)
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

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        super().report()

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
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

