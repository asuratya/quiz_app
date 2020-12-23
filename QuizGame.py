#  list of players with method to add QuizQuestions to topics or to add topics

#import tkinter as tk  # Tkinter library for GUI
from Player import *
from QuizQuestion import *

#tk._test() #to check if tkinter is working

class QuizGame():
    def __init__(self):
        # private:
        self._topics = [] # fill with names of question topics
        self._questions = [] # will be a nestedlist: contains lists with questions per topic

        self._players = [] 
        # fill with players in record.. maybe link to .txt file to keep player info even when closing game

    def AddQuestion(self, topic_index, question):
        if ( (topic_index < len(self._questions)) and (topic_index >= 0) ): # make sure topic_index is valid
            self._questions[topic_index].append(question)

    def AddTopic(self, topicname):
        self._topics.append(topicname)
        self._questions.append([])
    
    def AddPlayer(self, player):
        self._players.append(player)

    def GetQuesion(self, topicindex):
        # should be based on random number input for question index, now just use first
        return (self._questions[topicindex])[0]
     
# testing: these are just some dumb examples to test

game = QuizGame()
# -> initialize this with all the questions we will create

# could maybe replace doing this manually by some function that processes a .txt file with questions per topic
game.AddTopic("History")
H_index = 0
q1 = QuizQuestion("When did Belgium become independant?", ["1800", "1812", "1830"], 2)
game.AddQuestion(H_index, q1)

game.AddTopic("Science")
Sc_index = 1
q2 = QuizQuestion("What is the first element in the periodic table?", ["Lithium", "Hydrogen", "Uranium"], 1)
game.AddQuestion(Sc_index, q2)

game.AddTopic("Sport")
Sp_index = 2
q3 = QuizQuestion("Who won the world championship soccer in 2018?", ["France", "Kroatia", "Germany"], 0)
game.AddQuestion(Sp_index, q3)


# -> will host the run method for the game something like:”
# running = true
# display screen: load or create player, or quit (closes game)
# currentplayer = ... based on prev user input

# for now for testing: manually
mark = Player("Mark")
mark.AddScoresCategory() #history
mark.AddScoresCategory() #science
mark.AddScoresCategory() # sports

sophie = Player("Sophie")
sophie.AddScoresCategory() #history
sophie.AddScoresCategory() #science
sophie.AddScoresCategory() # sports

game.AddPlayer(mark)
game.AddPlayer(sophie)
currentplayer = mark

#while(running):
	#choose question topic based on user stats, choose random QQ in topic
	#display QQ + option to go to menu (running = false)
	#iscorrectanser(user’s answer)
	#update user stats

# for now for testing: mark's worst topic is science
q = game.GetQuesion(Sc_index)
# display question in GUI
print(q)

# mark's answer is index 2
# his stats get updated based on if the answer was correct
if (q.IsCorrectA(2)):
    currentplayer.AddScore(Sc_index, 100)
else:
    currentplayer.AddScore(Sc_index, -50)

# add here also option for returning to menu

# then repeat for loop for next question

# for testing: see that player scores were updated
print(currentplayer)