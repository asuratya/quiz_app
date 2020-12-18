# method to display the question/possible answers and method checkifcorrect(answer)
class QuizQuestion():
    # question is a str, answers is list of str, correct_answer is index of correct answer
    def __init__(self, question, answers, c_answer): 
        # private attributes!
        self._question = question
        self._answers = answers
        self._correct_answer = c_answer

    def __str__(self):
        s = self._question + "\n"
        for index in range(len(self._answers)):
            s = s + "\t" + str(index + 1) +") " + self._answers[index] + "\n"
        return s

    def IsCorrectA(self, A): # A is index of answer in list
        return A == self._correct_answer

# testing the new class:
#c = QuizQuestion("What is Robins age?", ["19","22","25","109"],1)
#print(c)
#print(c.IsCorrectA(3))
#print(c.IsCorrectA(1))