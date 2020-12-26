import tkinter as tk  # Tkinter library for GUI
import random
import time
from Player import *
from QuizQuestion import *

class QuizGame(): # mainly a class to host all user interface objects + some data (questions, players)
	def __init__(self):

		# setting up the root of the user interface = menuWindow
		self._MenuWindow()

		# initialize these as None or compiler will complain the class doesn't have these as attributes
		self._nameTextField = None # need ref to this to get content & to destroy
		self._nameButton = None # need ref to this to destroy
		self._pWindow = None # need ref to this to destroy
		self._mainWindow = None # need ref to this to add new Qframe
		self._Qframe = None # put widgets of mainwindow inside a frame together for easy destroy

		self._currentQ = None # current question being displayed/evaluated
		self._currentP = None # current active player
		self._currentcatindex = None # current category of questions
		
		# better would be: .txt files per topic with questions + function to add to game
		self._topics = [] # fill with names of question topics
		self._questions = [] # a nestedlist: contains lists with questions per topic

		self._players = [] 
		# fill with players in record.. maybe link to .txt file to keep player info even when closing game:
		# creating game loads player file into _players and saving game overwrites player file with new info

	def run(self): # starting window of user interface is launched
		self._menuWindow.mainloop()

	def _MenuWindow(self):
		self._menuWindow = tk.Tk()
		self._menuWindow.title("VUB QUIZ APP")
		self._menuWindow.geometry('500x300')
		self._menuWindow.resizable(0,0) # not resizable: change?
		self._menuWindow.configure(bg = "black")

		# start screen: 4 buttons: new player, select player, view stats, save game
		# title at top of every window
		title = tk.Label(self._menuWindow, text = 'VUB QUIZ APP', font = ('impact', 20, 'italic'), justify = tk.CENTER, bg = 'goldenrod2', fg = 'white')
		title.pack(side = tk.TOP, fill = tk.BOTH)
		
		# text box
		txt_box = tk.Label(self._menuWindow, text = "Are you ready to get your IQ tested?", font = "50", fg = 'white', bg = 'black')
		txt_box.place(x = 100, y = 100)

		# make these buttons prettier?:
		newPButton = tk.Button(master=self._menuWindow, text="Create new player", command = self._EnterName)
		newPButton.place(x = 50, y = 140)

		selectPButton = tk.Button(master=self._menuWindow, text="Select a player", command = self._SelectPWindow)
		selectPButton.place(x = 50, y = 180)

		viewStatsButton = tk.Button(master=self._menuWindow, text="View stats - under construction", command = None)
		# should change command to show stats: still making this function
		viewStatsButton.place(x = 50, y = 220)


		saveButton = tk.Button(master=self._menuWindow, text="Save - under construction", command = None)
		# should change command to write player info to .txt: still making this function
		saveButton.place(x = 50, y = 260)


	def _EnterName(self): # called by "new player" button: open new entry and button on menuwindow

		self._nameTextField = tk.Entry(master = self._menuWindow, text = "player name", width = 30)
		self._nameTextField.place(x = 190, y = 140)

		self._nameButton = tk.Button(master = self._menuWindow, text = "Confirm", command = self._AddPlayer)
		self._nameButton.place(x = 400, y = 140)

	def _AddPlayer(self): # called by Confirm button, create new player instance + put inside local list of players
		name = self._nameTextField.get()
		# should actually check if player already exists...!
		p = Player(name)
		self._players.append(p)
		self._nameButton.destroy()
		self._nameTextField.destroy()

	def _SelectPWindow(self):
		self._pWindow = tk.Toplevel(master = self._menuWindow) # new window
		self._pWindow.geometry('500x300')
		self._pWindow.resizable(0,0) # not resizable: change this?
		self._pWindow.title('SELECT A PLAYER')
		self._pWindow.config(bg ='black')
		title = tk.Label(self._pWindow, text = 'VUB QUIZ APP', font = ('impact', 20, 'italic'), justify = tk.CENTER, bg = 'goldenrod2', fg = 'white')
		title.pack(side = tk.TOP, fill = tk.BOTH)

		# display all players as buttons
		# dict to bind button and index: know which button was called = player index
		buttondict = {}
		index = 0
		for player in self._players:
			# command is a lambda function to pass input arg
			b = tk.Button(master = self._pWindow, text = player.GetName(), command = lambda: self._playingWindow(buttondict[b]))
			buttondict[b] = index 
			b.pack(side = tk.TOP, fill = tk.X) # make buttons stretched over window width
			index = index + 1
		
	def _playingWindow(self, index):
		self._pWindow.destroy()
		self._currentP = self._players[index]

		self._mainWindow = tk.Toplevel(master = self._menuWindow) # new window for the main game part
		self._mainWindow.geometry('500x300')
		self._mainWindow.resizable(0,0) # not resizable: change this?
		self._mainWindow.title('QUIZ')
		self._mainWindow.config(bg ='black')

		
		title = tk.Label(self._mainWindow, text = 'VUB QUIZ APP', font = ('impact', 20, 'italic'), justify = tk.CENTER, bg = 'goldenrod2', fg = 'white')
		title.pack(side = tk.TOP, fill = tk.BOTH)

		self._UpdateQuestion(-1) # display the question
		
	def _UpdateQuestion(self, prevAIndex):
		# step 1: update player stats based on prev Q (if there was one)
		
		if (self._currentQ != None): # we had a prev Q
			txt = ''
			if (self._currentQ.IsCorrectA(prevAIndex)): # player answered correctly
				self._currentP.AddScore(self._currentcatindex, 100)
				txt = 'You were correct and earned 100 points.'

			else: # player was wrong
				self._currentP.AddScore(self._currentcatindex, -50) 
				txt = 'You were wrong, the correct answer was ' + self._currentQ.getCorrectA() + '. You lost 50 points.'

			# show message box saying (in)correct for a few seconds
			resultbox = tk.Label(master = self._Qframe, text = txt, fg='green')
			resultbox.pack() # this doesn't show up???

			time.sleep(3) # making Python sleep to display this is not a great solution... replace?
			self._Qframe.destroy()

		self._Qframe = tk.Frame(self._mainWindow, bg = 'black') # encloses the other widgets so we can easily destroy them for the next Q
		self._Qframe.pack(expand = True, fill = tk.BOTH) # frame just fills rest of whole window

		# step 2: generating next Q:
		# fetch a category based on self._currentP current stats (separate function?)
		self._currentcatindex = 0 # for now for testing: take cat 0
		self._currentQ = self._GetQuesion(self._currentcatindex) # quiz question to ask

		# generate mainwindow questionbox
		# make prettier
		self._Qbox = tk.Label(master = self._Qframe, text = self._currentQ.getQ(), fg='green')
		self._Qbox.pack()

		# displaying possible answers: use same dictionary trick as with select player to know which button is clicked
		buttondict = {}
		index = 0
		for item in self._currentQ.getA():
			b = tk.Button(master = self._Qframe, text = item, command = lambda: self._UpdateQuestion(buttondict[b]))
			# actually command should check if right, update player stats and fetch new playingWindow: still to be made
			b.pack()
			buttondict[b] = index
			index = index + 1

	def _GetQuesion(self, topicindex): # getting a random question for a topic
		index = random.randint(0,len( self._questions[topicindex] ) - 1)
		return (self._questions[topicindex])[index]

	# these functions should become private to use with reading the .txt files but still to be implemented

	def AddQuestion(self, topic_index, question):
		if ((topic_index < len(self._questions)) and (topic_index >= 0) ): # make sure topic_index is valid
			self._questions[topic_index].append(question)

	def AddTopic(self, topicname):
		self._topics.append(topicname)
		self._questions.append([])
    
     
# testing: these are just some dumb examples to test for now
#*******************************************************************
game = QuizGame()

game.AddTopic("History")
H_index = 0
q1 = QuizQuestion("When did Belgium become independent?", ["1800", "1812", "1830"], 2)
game.AddQuestion(H_index, q1)

game.AddTopic("Science")
Sc_index = 1
q2 = QuizQuestion("What is the first element in the periodic table?", ["Lithium", "Hydrogen", "Uranium"], 1)
game.AddQuestion(Sc_index, q2)

game.AddTopic("Sport")
Sp_index = 2
q3 = QuizQuestion("Who won the world championship soccer in 2018?", ["France", "Kroatia", "Germany"], 0)
game.AddQuestion(Sp_index, q3)

q4 = QuizQuestion('q2?',['a','b','c'],0)
game.AddQuestion(H_index, q4)

p1 = Player("P1")
p2 = Player("P2")

p1.AddScoresCategory() #history
p1.AddScoresCategory() #science
p1.AddScoresCategory() # sports

p2.AddScoresCategory() #history
p2.AddScoresCategory() #science
p2.AddScoresCategory() # sports

game._players = [p1, p2]

game.run()