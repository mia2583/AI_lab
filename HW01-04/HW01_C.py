print("The sum of the digits in the numbers")
sum = 0
#for 루프를 이용하여 1부터 백만까지 돌기
for num in range(1, 1000001) :
    #for 루프를 이용하여 각 숫자에서의 자릿수 합 구하기
    for digit in str(num) :
        sum += int(digit)

#format을 이용하여 세자리마다 , 표시하기
print("from 1 to one million is {:,}.".format(sum))
