import random
NUMBER_OF_TRIALS = 10000

def matchTwoDecks():
    #두개의 숫자를 랜덤으로 선택하여 서로 같은 경우에 true로 반환
    num1 = random.randint(1, 52)
    num2 = random.randint(1, 52)
    numMatches = (num1 == num2)
    return numMatches

def main():
    totalMatches = 0
    #NUMBER_OF_TRIALS번 시도중 같은 카드를 뽑은 경우만 셈
    for i in range(NUMBER_OF_TRIALS):
        totalMatches += matchTwoDecks()
    #전체 횟수중 같은 카드를 뽑는 확률 계산
    averageMatches = totalMatches / NUMBER_OF_TRIALS
    print ("Average number of matched cards: {:.3f}".format(averageMatches) )

main()
