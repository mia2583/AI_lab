def main() :
    #필요한 상수 입력받기
    annualRateOfInterest = int( input("annual rate of interest: ") )
    monthlyPayment = int( input("Enter monthly payment: ") )
    begBalance = int( input("Enter beg. of month balance: ") )
    info = calculateValues(annualRateOfInterest, monthlyPayment, begBalance)
    printInfo(info)

#입력받은 값으로 계산식에 넣어 계산하기
def calculateValues(annualRateOfInterest, monthlyPayment, begBalance):
    intForMonth = ( annualRateOfInterest/12 ) * begBalance /100
    redOfPrincipal = monthlyPayment - intForMonth
    endBalance = begBalance - redOfPrincipal
    # intForMonth: Interest paid for the month
    # redOfPrincipal: Reduction of principal
    # endBalance: End of month balance
    return (intForMonth, redOfPrincipal, endBalance)

#format으로 소수점 둘째자리까지 출력, 세자리마다 ',' 표시하여 출력
def printInfo(info) :
    print("Interest paid for the month: ${:,.2f}".format(info[0]))
    print("Reduction of principal: ${:,.2f}".format(info[1]))
    print("End of month balance: ${:,.2f}".format(info[2]))
main()

