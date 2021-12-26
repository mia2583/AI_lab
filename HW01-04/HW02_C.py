def main() :
    #리스트를 문자열로 입력받기
    inputStr = input("Input list = ")
    inputList = makeList(inputStr)
    countNumber(inputList)

#문자열로 입력받은 리스트를 실제 리스트로 변환
def makeList(string) :
    inputStr = string[1:-1]
    inputList = list( map(int, inputStr.split(', ')) )
    inputList.sort()
    return inputList

#각각의 숫자의 반복 횟수 세기
def countNumber(listIn) :
    listOut = []
    #numNew : 찾고자하는 값(0-9), index : listIn를 참조하기 위한 인덱스
    #count : 특정 숫자를 찾은 횟수
    numNew = index = count = 0
    while(numNew <= 9) :
        #만약 참조 인덱스가 리스트 길이보다
        #큰 경우 결과리스트에 numNew와 count를 추가
        if(index >= len(listIn) ) :
            listOut.append([numNew, count])
            count = 0
            numNew += 1
        #numNew와 참조하는 리스트의 값이 같은 경우 count증가
        elif(numNew == listIn[index]) :
            count +=1
            index += 1
            continue
        #numNew와 참조하는 리스트의 값이 다른 경우
        #결과리스트에 numNew와 count를 추가
        else :
            listOut.append([numNew, count])
            count =0
            numNew += 1
    
    print("Encoded list = {}".format(listOut))
        
main()
