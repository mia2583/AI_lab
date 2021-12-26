def main() :
    #리스트 문자열로 입력받기
    inputStr = input("Enter a number as list : ")
    inputList = makeList(inputStr)
    #리스트 정렬
    inputList.sort()
    printMedian(inputList)

#문자열로 입력받은 리스트를 실제 리스트로 변환하기
def makeList(string) :
    inputStr = string[1:-1]
    inputList = list( map(int, inputStr.split(', ')) )
    return inputList

#중앙값 구하기
def printMedian(List) :
    index = int( len(List)/2 )
    #받은 수가 홀수냐 짝수냐에 따라 중앙값을 다르게 계산
    if(len(List)%2 == 1) :
        median = List[index]
    else :
        median = ( int(List[index - 1]) + int(List[index]) )/2
    #소수점 첫째자리까지 출력하기
    print('Median: {:.1f}'.format(median))

main()

