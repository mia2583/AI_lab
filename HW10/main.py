import numpy as np

def main():
    print("Which learning algorithm do you want to use?")
    print(" 1. Linear Regression")
    print(" 2. k-NN")
    aType = int(input("Enter the number: ")) #알고리즘 선택
    if aType == 1:
        ml = LinearRegression()
    elif aType == 2 :
        ml = KNN()
    fileName = input("Enter the file name of training data: ")
    ml.setData('train', fileName)
    fileName = input("Enter the file name of test data: ")
    ml.setData('test', fileName)
    ml.buildModel()
    ml.testModel()
    ml.report()

class ML:
    def __init__(self):
        self._trainDX = np.array([]) # Featulre value matrix (training data)
        self._trainDy = np.array([]) # Target column (training data)
        self._testDX = np.array([])  # Feature value matrix (test data)
        self._testDy = np.array([])  # Target column (test data)
        self._testPy = np.array([])  # Predicted values for test data

    def setData(self, dtype, fileName): # set class variables
        XArray, yArray = self.createMatrices(fileName)
        if dtype == 'train':
            self._trainDX = XArray
            self._trainDy = yArray
        elif dtype == 'test':
            self._testDX = XArray
            self._testDy = yArray
            self._testPy = np.zeros(np.size(yArray)) # Initialize to all 0
            
    def createMatrices(self, fileName): # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]
            features = data[0:-1]
            target = data[-1]
            XSet.append(features)
            ySet.append(target)
        infile.close()
        XArray = np.array(XSet)
        yArray = np.array(ySet)
        return XArray, yArray

    def testModel(self):
        n = np.size(self._testDy)
        for i in range(n):
            self._testPy[i] = self.runModel(self._testDX[i])

    def report(self):
        n = np.size(self._testDy) # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2 
            #실제값과 예측값 차이
            totalSe += se
        rmse = np.sqrt(totalSe) / n #rmse를 계산
        print()
        print("RMSE: ", round(rmse, 2))

class LinearRegression(ML) :
    def __init__(self):
        self._w = np.array([]) # Optimal weights for linear regression

    def buildModel(self): # Do linear regression and return optimal w
        X = self._trainDX
        n = np.size(self._trainDy)
        X0 = np.ones([n, 1])
        nX = np.hstack((X0, X)) # Add a column of all 1's as the first column
        y = self._trainDy
        t_nX = np.transpose(nX)
        self._w = np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)

    def runModel(self, data): # Apply linear regression to a test data
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)

class KNN(ML):
    def __init__(self):
        self._k = 0            # k value for k-NN

    def buildModel(self):
        self._k = int(input("Enter the value for k: "))
    
    def runModel(self, query): #query는 test파일에서 값
        closestK = self.findCK(query)
        predict = self.takeAvg(closestK)
        return predict

    def takeAvg(self, closestK):
        k = self._k
        total = 0
        for i in range(k) :
            j = closestK[i, 0]
            total +=self._trainDy[j]
        return total / k
        #j는 가장 가까운것의 index

    def updateCK(self, closestK, i, query):
    #현재 거리보다 가까우면 update
        d = self.sDistance(self._trainDX[i], query)
        for j in range(len(closestK)):
            if closestK[j, 1] > d:
                closestK[j, 0] = i
                closestK[j, 1] = d
                break

    def findCK(self, query): #가장 가까운 k개의 이웃
        m = np.size(self._trainDy)
        k = self._k
        closestK = np.arange(2 * k).reshape(k,2)
        for i in range(k):
            closestK[i, 0] = i
            closestK[i, 1] = self.sDistance(self._trainDX[i], query)
        for i in range(k, m):
            self.updateCK(closestK, i, query)
        return closestK

    def sDistance(self, dataA, dataB): #거리 계산
        dim = np.size(dataA)
        sumOfSquares = 0
        for i in range(dim) :
            sumOfSquares += (dataA[i] - dataB[i]) **2
        return sumOfSquares

main()