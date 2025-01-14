class Setup:
    def __init__(self):
        self._delta = 0.01
        self._alpha = 0.01
        self._dx = 10 **(-4)
        self._resolution = 0
    def getDelta(self) :
        return self._delta
    def getDx(self):
        return self._dx
    def getAlpha(self) :
        return self._alpha

    def setDx(self, dx):
        self._dx = dx
    def setAlpha(self, alpha) :
        self._alpha = alpha

#Setup을 상속
class Problem(Setup):
    def __init__(self):
        pass

#Setup을 상속
class HillClimbing(Setup):
    def __init__(self):
        pass

#Setup을 상속
class MetaHeuristics(Setup) :
    def __init(self):
        pass
