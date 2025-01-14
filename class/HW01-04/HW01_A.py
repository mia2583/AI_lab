#필요한 상수 입력받기
purchase = int(input("Enter purchase price: "))
selling = int(input("Enter selling price: "))

#입력받은 값으로 계산식에 넣어 계산하기
markup = selling - purchase
PercentageMarkup = (markup/purchase)*100
ProfitMargin = (markup/selling)*100

#소수점 첫째자리 혹은 둘째자리까지 출력하기
print('Markup: ${:.1f}'.format(markup))
print('Percentage markup: {:.1f}%'.format(PercentageMarkup))
print('Profit margin: {:.2f}%'.format(ProfitMargin))
