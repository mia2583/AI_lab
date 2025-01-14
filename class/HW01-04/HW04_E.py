import random

class Contestant:
    #클래스 생성자 작성
    def __init__(self, name="", score=0):
        self._name = name
        self._score = score

    #self._name 반환
    def getName(self):
        return self._name

    #self._score 반환
    def getScore(self):
        return self._score

    #점수 1증가
    def incrementScore(self):
        self._score += 1

#Contestant의 subclass 생성1
class Human(Contestant):
    #가위바위보 중 하나 입력 받아서 선택 결과 반환
    def makeChoice(self):
        rsp = ["rock", "scissors", "paper"]
        while True :
            choose = input("{}, enter your choice: ".format(self._name))
            #리스트 rsp에 있는 원소들중에서만 입력가능하게 함
            if(choose in rsp) :
                break
        return choose

#Contestant의 subclass 생성2
class Computer(Contestant):
    def makeChoice(self):
        #가위바위보중 랜덤으로 선택하여 결과 반환
        rsp = ["rock", "scissors", "paper"]
        choose = random.choice(rsp)
        print( self._name + " chooses " + choose )
        return choose

def playGames(h,c):
    #총 세번 게임 진행
    for i in range(3):
        choiceH = h.makeChoice()
        choiceC = c.makeChoice()
        #이긴쪽의 점수를 1 증가, 같으면 변화 없음
        if choiceH == choiceC:
            pass
        elif higher(choiceH, choiceC):
            h.incrementScore()
        else:
            c.incrementScore()
        #매 게임마다 현재 점수 결과 출력
        print(h.getName() + ":", h.getScore(),
            c.getName() + ":", c.getScore())
        print()
    
def higher(c1, c2):
    if ((c1 == 'rock' and c2 == 'scissors') or
        (c1 == 'paper' and c2 == 'rock') or
        (c1 == 'scissors' and c2 == 'paper')):
        return True
    else:
        return False

def main():
    #사람과 컴퓨터 이름 입력
    humanName = input("Enter name of human: ")
    computerName = input("Enter name of computer: ")
    #각각의 객체 생성
    human = Human(humanName)
    computer = Computer(computerName)
    print()
    #게임 시작
    playGames(human, computer)
    #전체 결과 출력
    if human.getScore() == computer.getScore() :
        print("TIE")
    elif human.getScore() > computer.getScore() :
        print("{} WINS".format(human.getName()))
    else : 
        print("{} WINS".format(computor.getName()))
        
main()

