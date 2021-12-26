# 반환계수와 시작높이 입력받기
restitution = float(input("Enter coefficient of restitution: "))
height = int(input("Enter initial height in meters: "))

bounces = 0
newHeight = height
#while 문을 이용하여 높이가 0.1m이하가 되기 전까지 bounce 횟수 구하기
while(newHeight > 0.1) :
    newHeight *= restitution
    bounces+=1

# 위에서 구한 bounces 수를 통해 이동한 거리 계산
# 등비수열 공식 이용 + 올라갔다 내려갔다한 거리 고려-> 2배
travels = height + 2*(height*restitution)*\
          (1-pow(restitution, bounces-1))/(1-restitution)

#format을 이용하여 소수점 둘째자리까지 출력하기
print('Number of bounces: {0}'.format(bounces))
print('Meters traveled: {:.2f}'.format(travels))
