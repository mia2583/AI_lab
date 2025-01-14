class Setup:
    def __init__(self):
        self._delta = 0.01
    def getDelta(self) :
        return self._delta

#Setup을 상속
class Problem(Setup):
    def __init__(self):
        pass

#Setup을 상속
class HillClimbing(Setup):
    def __init__(self):
        pass
