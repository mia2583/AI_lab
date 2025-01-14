import matplotlib.pylab as plt
import numpy as np

data1= np.loadtxt('first.txt') #좌표 가져오기
x1 = np.arange(len(data1)) #x좌표 범위
y1 = data1

data2= np.loadtxt('anneal.txt') #좌표 가져오기
x2 = np.arange(len(data2))
y2 = data2

plt.figure()
plt.plot(x1,y1) #first-choice 그래프 그리기
plt.plot(x2,y2) #simulated Annealing 그래프 그리기
plt.xlabel('Number of Evaluations') #x축
plt.ylabel('Tour Cost') #y축
plt.title('Search Performance(TSP-100)') #그래프 제목
plt.legend(['First-Choice HC','Simulatd Annealing']) #선 이름
plt.show()
