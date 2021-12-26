class Setup:
    def __init__(self):
        self._aType = 0
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
    def getAType(self):
        return self._aType

    def setDx(self, dx):
        self._dx = dx
    def setAlpha(self, alpha) :
        self._alpha = alpha

    def setVariables(self, parameters) :
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']
        self._resolution = parameters['resolution']
#Setup을 상속
class Problem(Setup):
    def __init__(self):
        pass

#Setup을 상속
class Optimizer(Setup):
    def __init__(self):
        pass
