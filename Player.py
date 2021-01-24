# with attributes: name, scores per category with methods to edit and nicely display these properties
class Player():
        def __init__(self, name):
                # private attributes!
                self._name = name
                self._score=0
                self._finalScore = {'history': [], 'computer science': [], 'economics':[], 'politics':[]} 
                # store scores in list, overlaying QuizGames responsibility to keep track of corresponding category
        def getName(self): # was new in my version
                return self._name
        
        def getScore(self):
            return self._score
        
        def addScore(self):
            self._score = self._score + 100
        
        def subScore(self):
            self._score = self._score - 50
        
        def updateFinalScore(self, category, my_score):
            self._finalScore[category].append(my_score)
            
        def getFinalScore(self):
            return self._finalScore
        
        def clearScore(self):
            self._score = 0