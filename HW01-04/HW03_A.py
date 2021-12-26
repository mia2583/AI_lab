def readSetFromFile():
    #파일 읽기
    infile = open("Names.txt", 'r')
    #한줄씩 읽어서 set에 저장
    nameSet = {name for name in infile}
    #파일 닫기
    infile.close()
    return nameSet

def inputName():
    #추가할 이름 입력받기
    newName = input("Enter a first name to be included: ")
    return newName

def insertSet(mySet, name):
    #만약 이름이 set에 없다면 set에 추가하기
    if name+'\n' not in mySet :
        mySet.add(name + '\n')
        print("{} is added in Names.txt".format(name))
    else :
        print("{} is already in Names.txt".format(name))
    return mySet

def writeToFile(modifiedSet):
    #새로 이름들을 쓸 파일 생성
    outfile = open("Names.txt", 'w')
    #set을 list로 변환해서 sort하기
    modifiedList = list(modifiedSet)
    modifiedList.sort()
    #파일에 리스트 내용 적기
    outfile.writelines(modifiedList)
    outfile.close()
    
def main():
    mySet = readSetFromFile() #기존의 이름 파일을 set으로 읽기
    name = inputName() #추가할 이름 입력
    modifiedSet = insertSet(mySet, name) #set에 새로운 이름 추가
    writeToFile(modifiedSet) #이름들을 파일에 적기
 
main()
