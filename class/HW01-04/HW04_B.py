def displaySequenceNumbers(m,n):
    #m이 n보다 작으면 그대로 출력하고
    #m+1을 출력하기 위해 recursive함수 호출
    if m < n :
        print(m)
        return displaySequenceNumbers(m+1,n)
    #m이 n과 같으면 출력만
    if m == n :
        return m
    

def main():
    #함수 결과 출력하기
    print ("output of print (displaySequenceNumbers(2,4))")
    print (displaySequenceNumbers(2,4))
    print ("output of print (displaySequenceNumbers(3,3))")
    print (displaySequenceNumbers(3,3))

main()
