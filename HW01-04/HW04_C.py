class Quizzes:
    #클래스 생성자 작성
    def __init__(self, listOfGrades):
        self._listOfGrades = listOfGrades
    #리스트의 평균 구하기(합/길이)
    def average(self):
        return sum(self._listOfGrades) / len(self._listOfGrades)
    #점수 평균 결과 출력하기
    def __str__(self):
        return "Quiz average: " + str( self.average() )
        
def main():
    listOfGrades = []
    #퀴즈 결과들 입력받아서 리스트에 추가하기
    for i in range(1, 7) :
        grade = int( input("Enter grade on quiz 1: ") )
        listOfGrades.append(grade)
    lowestScore = min(listOfGrades)
    #가장 낮은 점수를 리스트에서 제거하기
    listOfGrades.remove(lowestScore)
    #Quizzes 객체 생성하기
    q = Quizzes(listOfGrades)
    #탈락자를 제외한 나머지 점수들의 평균 출력하기
    print (q)
    
main()
