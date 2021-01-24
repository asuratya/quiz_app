#####import some libraries
import tkinter as tk
from tkinter import messagebox
from Player import Player
import random
import os
from os import path
from QuizQuestion import QuizQuestion
import pickle
#from tkinter.ttk import Separator,Progressbar
#from tkinter.messagebox import showinfo

class QuizGame():
# mainly a class to host all user interface objects + some data (questions, players)
    def __init__(self):

        # setting up the root of the user interface = menuWindow
        self._MenuWindow()
        # initialize these as None or compiler will complain the class doesn't have these as attributes
        self._nameTextField = None  # need ref to this to get content & to destroy
        self._nameButton = None  # need ref to this to destroy
        self._pWindow = None  # need ref to this to destroy
        self._mainWindow = None  # need ref to this to add new Qframe
        self._Qframe = None  # put widgets of mainwindow inside a frame together for easy destroy

        # fill with players in record.. maybe link to .txt file to keep player info even when closing game:
        # creating game loads player file into _players and saving game overwrites player file with new info

    def run(self):  # starting window of user interface is launched
        self._menuWindow.mainloop()

    def _MenuWindow(self):
        self._menuWindow = tk.Tk()
        self._menuWindow.title("VUB QUIZ APP")
        self._menuWindow.geometry('500x300') #600x400
        self._menuWindow.resizable(0, 0)  # not resizable: change?
        self._menuWindow.configure(bg="black")

        # start screen: 4 buttons: new player, select player, view stats, save game
        # title at top of every window
        title = tk.Label(self._menuWindow, text='VUB QUIZ APP', font=(
            'impact', 20, 'italic'), justify=tk.CENTER, bg='dark slate blue', fg='white', name='app_title', height=2)
        title.pack(side=tk.TOP, fill=tk.BOTH)

        # make these buttons prettier?:
        newPButton = tk.Button(master=self._menuWindow,
                               text="Create new player", command=self._EnterName, width = 30,bg='slate blue',fg='black',activebackground='light grey',height=2)
        newPButton.place(x=130, y=120)
        
        selectPButton = tk.Button(master=self._menuWindow,
                                text="Select a player", command = self._SelectPWindow, width = 30,bg='slate blue',fg='black',activebackground='light grey',height=2)
        selectPButton.place(x = 130, y = 180)
               
        viewStatsButton = tk.Button(master=self._menuWindow,
                                text="View stats",command=self._viewStat, width = 30,bg='slate blue',fg='black',activebackground='light grey',height=2)
        
        viewStatsButton.place(x=130, y=240)


    #this fxn destroys all the widgets except the app_title widget in the frame
    def _destroyFrame(self):
        for widget in self._menuWindow.winfo_children(): #travers through all the widget in the frme
            if str(widget) != '.app_title':
                widget.destroy()
               
    
    def _EnterName(self):  # called by "new player" button: open new entry and button on menuwindow
        self._nameWindow = tk.Toplevel(master = self._menuWindow) # new window
        self._nameWindow.geometry('500x300')
        self._nameWindow.resizable(0,0) # not resizable: change this?
        self._nameWindow.title('SELECT A PLAYER')
        self._nameWindow.config(bg ='black')
        title = tk.Label(self._nameWindow,text='VUB QUIZ APP', font=(
            'impact', 20, 'italic'), justify=tk.CENTER, bg='dark slate blue', fg='white', name='app_title', height=2)
        title.pack(side = tk.TOP, fill = tk.BOTH)
        self._txt_box = tk.Label(
            self._nameWindow, text="Enter your Name: ", font="30",fg='white',bg='black')
        self._txt_box.place(x=30, y=130)
        self._nameTextField = tk.Entry(
            self._nameWindow, text="player name", width=40)
        self._nameTextField.place(x=200, y=133)

        self._nameButton = tk.Button(
            self._nameWindow, text="Confirm", command=self._AddPlayer, width=20, bg='slate blue',fg='black',activebackground='light grey' ) #calls the AddPlayer fxn when buttons is clicked
        self._nameButton.place(x=200, y=220)

    #function to add player and save the player object locally after creating
    def _AddPlayer(self):  # called by Confirm button, create new player instance + put inside local list of players
        name = self._nameTextField.get()
        self._checkPlayerExist(name)
        if len(name) == 0:
            messagebox.showinfo("Error", "Enter your Name") #make sure the name field is not empty
        else:
            playerObj = Player(name)
            self._savePlayerInfo(playerObj) # save the player object locally
            #self._startPlaying() #start the quiz game
            self._nameWindow.destroy() #destroy the current add player window
                    
    #function that shows the list of players and choose the player to start the quiz        
    def _SelectPWindow(self):
        self._pWindow = tk.Toplevel(master = self._menuWindow) # new window
        self._pWindow.geometry('500x300')
        self._pWindow.resizable(0,0) # not resizable: change this?
        self._pWindow.title('SELECT A PLAYER')
        self._pWindow.config(bg ='black')
        title = tk.Label(self._pWindow,text='VUB QUIZ APP', font=(
            'impact', 20, 'italic'), justify=tk.CENTER, bg='dark slate blue', fg='white', name='app_title', height=2)
        title.pack(side = tk.TOP, fill = tk.BOTH)
        
        players_list = self._loadPlayers() #load players from the pickled object
        for players in players_list: #traverse through the list of players object and create button for each
            tk.Button(self._pWindow,
                      text=players.getName(),
                      width = 40,
                      bg='black',
                      fg='slate blue',
                      activebackground='light grey',
                      command=lambda players=players: self._startPlaying(players)).pack(padx=5, pady=5) 
            
            
    #view the stats of the player in the    
    def _viewStat(self):
        self._statWindow = tk.Toplevel(master = self._menuWindow) # new window
        self._statWindow.geometry('500x300')
        self._statWindow.resizable(0,0) # not resizable: change this?
        self._statWindow.title('View Players Stats')
        self._statWindow.config(bg ='black')
        title = tk.Label(self._statWindow,text='VUB QUIZ APP', font=(
            'impact', 20, 'italic'), justify=tk.CENTER, bg='dark slate blue', fg='white', name='app_title', height=2)
        title.pack(side = tk.TOP, fill = tk.BOTH)
        #load the picked list of players saved locally
        players_list = self._loadPlayers()
        for players in players_list: #traverse through the list of players object and create button for each
            tk.Button(self._statWindow,
                      text=players.getName(),
                      width = 60,
                      bg='black',
                      fg='slate blue',
                      activebackground='light grey',
                      command=lambda players=players: self._viewScore(players)).pack(padx=5, pady=5)
            
    #show the score of the players in a message box when the button is clicked from the list of players    
    def _viewScore(self, players):
        self._scoreWindow = tk.Toplevel(master = self._statWindow) # new window
        self._scoreWindow.geometry('500x300')
        self._scoreWindow.resizable(0,0) # not resizable: change this?
        self._scoreWindow.title('Individual Player Stats')
        self._scoreWindow.config(bg ='black')
        title = tk.Label(self._scoreWindow,text='VUB QUIZ APP', font=(
            'impact', 20, 'italic'), justify=tk.CENTER, bg='dark slate blue', fg='white', name='app_title', height=2)
        title.pack(side = tk.TOP, fill = tk.BOTH)
        score = players.getFinalScore()
        name = players.getName()
        
        self._txt_box = tk.Label(
            self._scoreWindow, text="Score for " + name + " are as follows:", font= 14 ,fg='white',bg='black')
        self._txt_box.place(x=30, y=80)
        
        x_cord = 30 
        y_cord = 120
        
        for key, value in score.items():
            scrText = key.title() + " : " + str(value)
            tk.Label(self._scoreWindow, text= scrText).place(x = x_cord , y = y_cord)
            #x_cord += 50
            y_cord += 40
        
    #this fxn loads the pickled players and passes the players objects as a list            
    def _loadPlayers(self):
        prev_cwd = os.getcwd()
        os.chdir('players_data')
        cwd = os.getcwd()
        players = []
        for files in os.listdir(cwd):
            with open(files, 'rb') as openfile:
                players.append(pickle.load(openfile))
        os.chdir(prev_cwd)
        return players

    #this fxn shows the starting window for the quiz game
    def _startPlaying(self, players):
        self._destroyFrame()
        players.clearScore()
        currentP = players
        txt_box = tk.Label(self._menuWindow,
                           text="Choose the category " +
                               currentP.getName(),
                           font="24", fg='white', bg='black')
        txt_box.place(x=50, y=80)
        
        #gets the chosen questions category and passes the index of the chosen questions and the category
        def choseCategory():
            categoryQuestions = []
            questionsIndex = []
            if categoryVar.get() == '-1' : #checks if radio button is clicked or not
                messagebox.showinfo("Error", 'Choose a category!' )
            else:
                selectedCategory = categoryVar.get() 
                
                for questions in quiz_questions:
                    if selectedCategory in questions:
                        categoryQuestions.append(questions)
                        questionsIndex.append(quiz_questions.index(questions))
                self._playingWindow(questionsIndex, selectedCategory, currentP)
           
        categoryVar = tk.StringVar()
        categoryVar.set(-1)
        
        R1 = tk.Radiobutton(self._menuWindow, text= 'History',variable= categoryVar, indicatoron=0, value = 'history', width = 20, height=1, fg='black',bg='slate blue', activebackground='light grey')
        R1.place(x=50, y=130) 
      
        R2 = tk.Radiobutton(self._menuWindow, text= 'Computer Science', variable= categoryVar,indicatoron=0, value = 'computer science', width = 20,fg='black',height=1,bg='slate blue', activebackground='light grey')
        R2.place(x=300, y=130)
        
        R3 = tk.Radiobutton(self._menuWindow, text= 'Economics', variable= categoryVar,indicatoron=0, value = 'economics', width = 20,fg='black',height=1,bg='slate blue', activebackground='light grey')
        R3.place(x=50, y=170)
        
        R4 = tk.Radiobutton(self._menuWindow, text= 'Politics', variable= categoryVar,indicatoron=0, value = 'politics', width = 20,fg='black',height=1,bg='slate blue', activebackground='light grey')
        R4.place(x=300, y=170)

        b = tk.Button(master=self._menuWindow, text='Start Quiz', width=20, bg='slate blue',fg='black',activebackground='light grey',
                      command= choseCategory)
        
        b.place(x=175, y=240)
    
    
    #save the info of the current player as a pickle object locally
    def _savePlayerInfo(self, player):
        player_name = player.getName()
        prev_dir=os.getcwd()
        filename = player_name + '.pk1'
        os.chdir('players_data')
        with open(filename, 'wb') as output:
            pickle.dump(player, output, pickle.HIGHEST_PROTOCOL)
        os.chdir(prev_dir)
    
    #check if the player exists or not and throw error if exists
    def _checkPlayerExist(self, player_name):
        prev_dir=os.getcwd()
        os.chdir('players_data')
        filename = player_name+ '.pk1'
        if path.exists(filename):
            messagebox.showinfo("Error", 'User Already Exists!' )
        os.chdir(prev_dir)
            
        
            
    #this fxn displays the final window to the player with the score after completing the quiz
    def _finalWindow(self, selectedCategory, currentP): 
        ltst_score = currentP.getScore()
        currentP.updateFinalScore(selectedCategory, ltst_score)
        self._savePlayerInfo(currentP) 
        #show the points in the message box
        def showPoints():
            result = "Your final score for " + selectedCategory + " is " + str(ltst_score)
            messagebox.showinfo("Result", result)
  
        self._destroyFrame()
        exit_label = tk.Label(self._menuWindow,
                      text= 'Congratulations you have finished your quiz!!!' , font='10', fg='white', bg='black')
        exit_label.place(x=80, y=110)
               
        btnShowAnswer = tk.Button(master=self._menuWindow, text='View Score', width=20, bg='dark slate blue',fg='black',activebackground='light grey',
                      command= showPoints)
        btnShowAnswer.place(x=180, y=200)

        
        
    #shows the playing window i.e the frame where the questions are loaded
    def _playingWindow(self, questionsIndex, selectedCategory, currentP):        
        self._destroyFrame()
        no_of_ques = 5
        #random index of the question to show
        #index = randomQuestions(no_of_ques, (len(categoryQuestions) -1))
        index = random.sample(questionsIndex, no_of_ques)
        for i in range(no_of_ques):
            question, index = getQuestions(i, index)
            self._showQuestions(question, index, i, currentP)
            self._destroyFrame()            
            if i == (no_of_ques - 1): #check if the current question is the final question
                self._finalWindow(selectedCategory, currentP)       
                    
    #show the question and thei options one at a time through the for loop in the playingWindow function       
    def _showQuestions(self, question, index, i, currentP):
        q_label = str(i + 1) +'. ' + question
        question_label = tk.Label(self._menuWindow,
                      text= q_label , font='10', fg='white', bg='black')
        question_label.place(x=20, y=80)
        
        answers = getAnswersOnTheList(index, i) #get answer of the current question
        
        #gets the value from the radio button selected and checks
        def checkAnswer():
            if radioVar.get() == '-1' : #checks if radio button is clicked or not
                messagebox.showinfo("Error", 'Choose a option' )
            else:
                selection = radioVar.get()
                correct_ans = getCorrectAnswer(index, i)
                if selection == correct_ans:
                    currentP.addScore()
                else:
                    currentP.subScore()
                var2.set(1)                
           
        radioVar = tk.StringVar()
        radioVar.set(-1)
        
        #initialized a variable for python to wait until it's value is changed
        var2 = tk.IntVar()
        
        
        R1 = tk.Radiobutton(self._menuWindow, text= answers[0],variable= radioVar, indicatoron=0, value = answers[0], width = 20, height=2, fg='black',bg='slate blue', activebackground='light grey')
        R1.place(x=50, y=110) 
      
        R2 = tk.Radiobutton(self._menuWindow, text= answers[1], variable= radioVar,indicatoron=0, value = answers[1], width = 20,fg='black',height=2,bg='slate blue', activebackground='light grey')
        R2.place(x=300, y=110)
        
        R3 = tk.Radiobutton(self._menuWindow, text= answers[2], variable= radioVar,indicatoron=0, value = answers[2], width = 20,fg='black',height=2,bg='slate blue', activebackground='light grey')
        R3.place(x=50, y=200)
        
        R4 = tk.Radiobutton(self._menuWindow, text= answers[3], variable= radioVar,indicatoron=0, value = answers[3], width = 20,fg='black',height=2,bg='slate blue', activebackground='light grey')
        R4.place(x=300, y=200)
        
        
        next_button =  tk.Button(self._menuWindow, text = 'Next Question', command =checkAnswer,fg='black',bg='dark slate blue',activebackground='light grey')
        next_button.place(x=210, y = 260)
        
        next_button.wait_variable(var2)
        
        



# *******************************************************************
questions_obj = []

game = QuizGame()

quiz_questions = [
    ['Question No. 1:When did the WW1 start?', '1', ['28 july 1914', '28 june 1914', '28 july 1916', '28 june 1916'],'history'],
    ['Question No. 2:Who invented the first Vaccine', '2', ['Louis pasteur', 'Edward jener', 'Alexander Fleming', 'james Phipps'],'history'],
    ['Question No. 3:Which vaccine was the first invented?', '3', ['Covid-19', 'turbercolisis', 'Small pox', 'meningitis'],'history'],
    ['Question No. 4:When did the WW2 end?', '4', ['1949', '1955', '1947', '1945'],'history'],
    ['Question No. 5:I joined the EU most recently?', '5', ['Swahili', 'Croatia', 'Bulgaria', 'Slovenia'],'history'],
    ['Question No. 6:Which country is not a former European colony?', '6', ['Namibia', 'Congo', 'Ethiopia', 'Kenya'],'history'],
    ['Question No. 7:Who was Ivory Coast first president?', '7', ['Julius Nyerere', 'Alix Mazrui', 'Kwame Nkrumah', 'felix Houphouet Boigny'],'history'],
    ['Question No. 8: Which country was known as Dahomey', '8', ['Benin', 'Senegal', 'Botswana', 'Dahomie'],'history'],
    ['Question No. 9: When did prince Philippe became king of Belgium', '9', ['2011', '2013', '2014', '2012'],'history'],
    ['Question No. 10:Who was the first president of the US?', '2', ['Donald Trump', 'George Washington', 'Barack Obama', 'John Adams'],'history'],
    ['Question No. 11:', '2', ['1', '2', '3', '4'],'politics'],
    ['Question No. 12:', '3', ['1', '2', '3', '4'],'politics'],
    ['Question No. 13:', '4', ['1', '2', '3', '4'],'politics'],
    ['Question No. 14:', '5', ['1', '5', '3', '4'],'politics'],
    ['Question No. 15:', '6', ['5', '2', '6', '4'],'politics'],
    ['Question No. 16:', '7', ['4', '8', '3', '7'],'politics'],
    ['Question No. 17:', '8', ['8', '7', '9', '4'],'politics'],
    ['Question No. 18:', '9', ['7', '9', '3', '0'],'politics'],
    ['Question No. 19:', '1', ['1', '2', '3', '4'],'politics'],
    ['Question No. 20:', '2', ['1', '2', '3', '4'],'politics'],
    ['Question No. 21: Which general term refer to harmful software?', '3', ['virus', 'trojan horse', 'malware', 'spyware'],'computer science'],
    ['Question No. 22: Who is the primary creator of java Language?', '4', ['Brian Kernighan', 'Domain squatters', 'Bryan Kerningham', 'james Gosling'],'computer science'],
    ['Question No. 23:What was the name of the first calculator', '5', ['abacus', 'Pascaline', 'calculus1', 'lening'],'computer science'],
    ['Question No. 24:What is the date and time of the Unix epoch', '6', ['00:00, December 31,1970', '00:00,january 1,1980', '00:00,january 1,1970', '00:00, December 31,1980'],'computer science'],
    ['Question No. 25: 1 Gigabyte equals:', '7', ['1000Mb', '1220Mb', '1200Mb', '1024Mb'],'computer science'],
    ['Question No. 26: A web address is usually known as:', '8', ['URL', 'WWW', 'URI', 'UWL'],'computer science'],
    ['Question No. 27:Who invented the first microchip?', '9', ['Jack Dorsey', 'Jack Kilby', 'Greg Chesson', 'Ronald Rider'],'computer science'],
    ['Question No. 28: Which among the folowing connects two networks?', '1', ['gateway', 'highway', 'http', 'bus'],'computer science'],
    ['Question No. 29:The technology is used to record cryptocurrency transactions is?', '2', ['digital wallet', 'Blockchain', 'token', 'mining'],'computer science'],
    ['Question No. 30:What is the binary representation of 45/8?', '3', ['110.101', '100.11', '100.101', '10.011'],'computer science'],
    ['Question No. 31:', '4', ['1', '2', '3', '4'],'economics'],
    ['Question No. 32:', '5', ['1', '5', '3', '4'],'economics'],
    ['Question No. 33:', '6', ['5', '2', '6', '4'],'economics'],
    ['Question No. 34:', '7', ['4', '8', '3', '7'],'economics'],
    ['Question No. 35:', '8', ['8', '7', '9', '4'],'economics'],
    ['Question No. 36:', '9', ['7', '9', '3', '0'],'economics'],
    ['Question No. 37:', '6', ['5', '2', '6', '4'],'economics'],
    ['Question No. 38:', '7', ['4', '8', '3', '7'],'economics'],
    ['Question No. 39:', '8', ['8', '7', '9', '4'],'economics'],
    ['Question No. 40:', '9', ['7', '9', '3', '0'],'economics']
    ]

#create questions objects and initialize them with the value from the list
for items in quiz_questions:
    questions_obj.append(QuizQuestion(items[0], items[1], items[2], items[3]))
 
def getQuestions(i, index): 
    return questions_obj[index[i]].getQuestion(), index

def getAnswersOnTheList(index, i):
    return questions_obj[index[i]].getAnswersList()

def getCorrectAnswer(index, i):
    return questions_obj[index[i]].getAnswer()

game.run()

