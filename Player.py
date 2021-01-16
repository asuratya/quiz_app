# with attributes: name, scores per category with methods to edit and nicely display these properties
class Player():
        def __init__(self, name):
                # private attributes!
                self._name = name
                self._score=0
                self._finalScore = [] 
                # store scores in list, overlaying QuizGames responsibility to keep track of corresponding category
        def getName(self): # was new in my version
                return self._name
        
        def getScore(self):
            return self._score
        
        def addScore(self):
            self._score = self._score + 100
        
        def subScore(self):
            self._score = self._score - 50
        
        def updateFinalScore(self, my_score):
            self._finalScore.append(my_score)
            
        def getFinalScore(self):
            return self._finalScore[-1]
            
                
        '''def AddScoresCategory(self):
                self._scores.append(0) # add a new category score that starts at 0

        def AddScore(self, index, amount): # add amount to scores[index]
                if ( (index < len(self._scores)) and (index >= 0) ): # make sure index is valid
                        self._scores[index] = self._scores[index] + amount

        def __str__(self): # this could be made prettier
                return self._name + ": \n \t" + self._scores.__str__()'''