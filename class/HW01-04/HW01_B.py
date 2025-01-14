#필요한 상수 입력받기
salary = int(input("Enter begining salary: "))

#10%씩 인상한 salary가격들 구하기
firstSalary = salary*1.1
secondSalary = firstSalary*1.1
threeSalary = secondSalary*1.1

#10%씩 세번 인상한 salay가격이 원래 salary가격으로부터 오른 퍼센트 계산하기
change = (threeSalary - salary)/salary*100

#소수점 둘째자리까지 출력하기
print('New salary: ${:,.2f}'.format(threeSalary)) #세자리수 마다 , 표시하기
print('Change: {:.2f}%'.format(change))

