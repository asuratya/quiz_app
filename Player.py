# with attributes: name, scores per category with methods to edit and nicely display these properties
class Player():
    def __init__(self, name):
        # private attributes!
        self._name = name
        self._scores = [] 
        # store scores in list, overlaying QuizGames responsibility to keep track of corresponding category

    def AddScoresCategory(self):
        self._scores.append(0) # add a new category score that starts at 0

    def AddScore(self, index, amount): # add amount to scores[index]
        if ( (index < len(self._scores)) and (index >= 0) ): # make sure index is valid
            self._scores[index] = self._scores[index] + amount

    def __str__(self): # this could be made prettier
        return self._name + ": \n \t" + self._scores.__str__()

# testing the new class:
#p = Player("George") 
# history: 
#p.AddScoresCategory()
#p.AddScore(0,100) # player scored 100 points in history cat
#print(p)