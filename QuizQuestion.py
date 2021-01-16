# method to display the question/possible answers and method checkifcorrect(answer)
class QuizQuestion():
    # question is a str, answers is list of str, correct_answer is index of correct answer
    def __init__(self, question, answer,answers_list): 
        # private attributes!
        self._question = question
        self._answer = answer
        self._answers_list =answers_list

    def getQuestion(self): #new in my version
        return self._question
    
    def getAnswer(self):
        return self._answer
    
    def getAnswersList(self):
        return self._answers_list

    '''def getQ(self): #new in my version
        return self._question
    
    def getA(self): #new in my version
        s = []
        for index in range(len(self._answers)):
            s.append(str(index+1) + ") " + self._answers[index])
        return s

    def getCorrectA(self):
        return self._answers[self._correct_answer]

    def __str__(self):
        s = self._question + "\n"
        for index in range(len(self._answers)):
            s = s + "\t" + str(index + 1) +") " + self._answers[index] + "\n"
        return s

    def IsCorrectA(self, A): # A is index of answer in list
        return A == self._correct_answer'''