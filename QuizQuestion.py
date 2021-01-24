# method to display the question/possible answers and method checkifcorrect(answer)
class QuizQuestion():
    # question is a str, answers is list of str, correct_answer is index of correct answer
    def __init__(self, question, answer, answers_list, category): 
        # private attributes!
        self._question = question
        self._answer = answer
        self._answers_list =answers_list
        self._category = category

    def getQuestion(self): #new in my version
        return self._question
    
    def getAnswer(self):
        return self._answer
    
    def getAnswersList(self):
        return self._answers_list
    
    def getCategory(self):
        return self._category