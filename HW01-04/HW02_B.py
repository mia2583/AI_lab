def main() :
    abcd = findSpecial()
    printSpecial(abcd)
    
#특별한 숫자를 찾아서 반환
def findSpecial() :
    #네자리 숫자를 일의 자리수부터 1씩 증가하면서 abcd를 구성
    after = 0
    for a in range(1, 10) :
        for b in range(0, 10) :
            for c in range(0, 10) :
                for d in range(0, 10) :
                    #생성한 abcd를 reverse 하기위해 각각의 원소로 리스트에 저장
                    before = [str(a), str(b), str(c), str(d)]
                    before.reverse()
                    #4 x abcd의 값을 after에 대입
                    after = ( a*1000 + b*100 + c*10 + d ) * 4
                    #dcba값과 abcd의 값이 동일한지 비교
                    if(''.join( before ) == str(after) ) :
                        before.reverse()
                        #형식에 맞게 출력
                        print('Since 4 x {} is {},'.format(''.join( before ) , after))
                        return after
   

#결과창 출력
def printSpecial(found) :
    print('the special number is {}.'.format(found))

main()

