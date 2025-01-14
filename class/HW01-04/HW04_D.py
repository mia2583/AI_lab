class Fraction:
    #클래스 생성자 작성
    def __init__(self, numerator=0, denominator=1):
        self._numerator = numerator
        self._denominator = denominator

    #self._numerator을 원하는 값으로 지정
    def setNumerator(self, numerator):
        self._numerator = numerator

    #self._numerator 반환
    def getNumerator(self):
        return self._numerator

    #self._denominator을 원하는 값으로 지정
    def setDenominator(self, denominator):
        self._denominator = denominator

    #self._denominator 반
    def getDenominator(self):
        return self._denominator

    #m과 n의 GCD 구하기
    def GCD(self, m, n):
        while n != 0:
            t = n
            n = m % n
            m = t
        return m

    #분자와 분모를 각각 GCD로 나누어 서로소로 만들기
    def reduce(self):
        numer = int( self._numerator/self.GCD(self._numerator, self._denominator) )
        denomin = int( self._denominator/self.GCD(self._numerator, self._denominator) )
        return str(numer) + "/" + str(denomin)

def main():
    #numerator와 denominator 입력받기
    numerator = int( input("Enter numerator of fraction: ") )
    denominator = int( input("Enter denominator of fraction: ") )
    #객체 생성하기
    frac = Fraction(numerator, denominator)
    #기약분수꼴로 출력하기
    print( "Reduction to lowest terms: {0}".format(frac.reduce()) )

main()
