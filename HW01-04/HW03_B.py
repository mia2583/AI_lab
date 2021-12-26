def populateDictionary():
    #단위가 적힌 파일 열기
    infile = open('Units.txt', 'r')
    unitDic = {}
    #한줄을 읽어서 ,를 기준으로 단위와 값으로 변환
    #이를 딕셔너리에 추가
    for line in infile :
        (unit, value) = line.split(',')
        unitDic[unit] = float(value)
    return unitDic

def getInput():
    #변환하고자하는 단위와 길이, 그리고 변환결과 단위 입력받기
    orig = input("Unit to convert from: ")
    dest = input("Unit to convert to: ")
    length = int(input("Enter length in {}: ".format(orig)))
    return (orig, dest, length)
    
def main():
    feet = populateDictionary() #기존 파일에서 단위정보를 딕셔너리로 만들기
    orig, dest, length = getInput() #필요한 상수 및 단위 입력받기
    ans = length * feet[orig] / feet[dest] #단위변환 계산 공식
    print("Length in {0}: {1:,.4f}".format(dest, ans))
    
main()

