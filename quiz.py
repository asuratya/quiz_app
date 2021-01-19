#####import some libraries
import tkinter as tk
from tkinter import messagebox
from Player import Player
import random,sys
import os
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

        self._players = []
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
                               text="Create new player", command=self._EnterName, width = 30,bg='slate blue',fg='black',activebackground='light grey',height=2 )
        newPButton.place(x=130, y=120)
               
        viewStatsButton = tk.Button(master=self._menuWindow,
                                    text="View stats",command=self._viewStat, width = 30,bg='slate blue',fg='black',activebackground='light grey',height=2)
        # should change command to show stats: still making this function
        viewStatsButton.place(x=130, y=190)


    #this fxn destroys all the widgets except the app_title widget in the frame
    def _destroyFrame(self):
        for widget in self._menuWindow.winfo_children(): #travers through all the widget in the frme
            if str(widget) != '.app_title':
                widget.destroy()
                
    
    def _EnterName(self):  # called by "new player" button: open new entry and button on menuwindow
        self._destroyFrame()
        self._txt_box = tk.Label(
            self._menuWindow, text="Enter your Name: ", font="30",fg='white',bg='black')
        self._txt_box.place(x=30, y=130)
        self._nameTextField = tk.Entry(
            self._menuWindow, text="player name", width=40)
        self._nameTextField.place(x=200, y=133)

        self._nameButton = tk.Button(
            self._menuWindow, text="Confirm", command=self._AddPlayer, width=20, bg='slate blue',fg='black',activebackground='light grey' ) #calls the AddPlayer fxn when buttons is clicked
        self._nameButton.place(x=200, y=220)

    def _AddPlayer(self):  # called by Confirm button, create new player instance + put inside local list of players
        name = self._nameTextField.get()
        if len(name) == 0:
            messagebox.showinfo("Error", "Enter your Name") #make sure the name field is not empty
        else:
            p = Player(name)
            self._players.append(p)
            self._startPlaying() #start the quiz game
    #view the stats of the player in the    
    def _viewStat(self):
        self._statWindow = tk.Toplevel(master = self._menuWindow) # new window
        self._statWindow.geometry('500x300')
        self._statWindow.resizable(0,0) # not resizable: change this?
        self._statWindow.title('Stats')
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
        score = players.getFinalScore()
        name = players.getName()
        msg = 'Score of ' + name + ' is: ' + str(score)
        messagebox.showinfo('Score', msg)

    #this fxn loads the pickled players and passes the objects as a list            
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
    def _startPlaying(self):
        self._destroyFrame()

        txt_box = tk.Label(self._menuWindow,
                           text="Are you ready to get your IQ tested " +
                               self._players[0].getName() + "?",
                           font="30", fg='white', bg='black')
        txt_box.place(x=90, y=130)

        b = tk.Button(master=self._menuWindow, text='Start Quiz', width=20, bg='slate blue',fg='black',activebackground='light grey',
                      command=lambda: self._playingWindow())
        
        b.place(x=170, y=220)
    
    #this fxn displays the final window to the player with the score after completing the quiz
    def _finalWindow(self): 
        #show the points in the message box
        def showPoints():
            ltst_score = self._players[0].getScore()
            self._players[0].updateFinalScore(ltst_score)
            result = "Your final point is " + str(self._players[0].getFinalScore())
            savePlayerInfo()

            messagebox.showinfo("Result", result ) 
           
         
        
  
        #save the info of the current player as a pickle object locally
        def savePlayerInfo():
            player_name = self._players[0].getName()
            prev_dir=os.getcwd()
            filename = player_name+ '.pk1'
            os.chdir('players_data')
            with open(filename, 'wb') as output:
                pickle.dump(self._players[0], output, pickle.HIGHEST_PROTOCOL)
            os.chdir(prev_dir)
            
        self._destroyFrame()
        exit_label = tk.Label(self._menuWindow,
                      text= 'Congratulations you have finished your quiz!!!' , font='10', fg='white', bg='black')
        exit_label.place(x=80, y=110)
        
        btnShowAnswer = tk.Button(master=self._menuWindow, text='View Score', width=20, bg='dark slate blue',fg='black',activebackground='light grey',
                      command= showPoints)
        btnShowAnswer.place(x=180, y=200)

        
        
    #shows the playing window i.e the frame where the questions are loaded
    def _playingWindow(self):        
        self._destroyFrame()
        no_of_ques = 5
        #random index of the question to show
        index = randomQuestions(no_of_ques, (len(quiz_questions) -1))
        for i in range(no_of_ques):
            question, index = getQuestions(i, index)
            self._showQuestions(question, index, i)
            if i == (no_of_ques - 1): #check if the current question is the final question
                self._finalWindow()       
                    
    #show the question and thei options one at a time through the for loop in the playingWindow function       
    def _showQuestions(self, question, index, i):
        q_label = str(i + 1) +'. ' + question
        question_label = tk.Label(self._menuWindow,
                      text= q_label , font='10', fg='white', bg='black')
        question_label.place(x=100, y=80)
        
        answers = getAnswersOnTheList(index, i) #get answer of the current question
        
        #gets the value from the radio button selected and checks
        def checkAnswer():
            if radioVar.get() == '-1' : #checks if radio button is clicked or not
                messagebox.showinfo("Error", 'Choose a option' )
            else:
                selection = radioVar.get()
                correct_ans = getCorrectAnswer(index, i)
                if selection == correct_ans:
                    self._players[0].addScore()
                else:
                    self._players[0].subScore()
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
    ['Question No. 1:', '1', ['1', '2', '3', '4']],
    ['Question No. 2:', '2', ['1', '2', '3', '4']],
    ['Question No. 3:', '3', ['1', '2', '3', '4']],
    ['Question No. 4:', '4', ['1', '2', '3', '4']],
    ['Question No. 5:', '5', ['1', '5', '3', '4']],
    ['Question No. 6:', '6', ['5', '2', '6', '4']],
    ['Question No. 7:', '7', ['4', '8', '3', '7']],
    ['Question No. 8:', '8', ['8', '7', '9', '4']],
    ['Question No. 9:', '9', ['7', '9', '3', '0']]
    ]

#create questions objects and initialize them with the value from the list
for items in quiz_questions:
    questions_obj.append(QuizQuestion(items[0], items[1], items[2]))
 
def getQuestions(i, index): 
    return questions_obj[index[i]].getQuestion(), index

def getAnswersOnTheList(index, i):
    return questions_obj[index[i]].getAnswersList()

def getCorrectAnswer(index, i):
    return questions_obj[index[i]].getAnswer()

def randomQuestions(num, end, start=0):
    que_index = []

    while(len(que_index) < num):
        tmp = random.randint(start, end)
        if tmp not in que_index:
            que_index.append(tmp)
    return que_index

game.run()


'''##############to make the main window#############
root = Tk()
root.title("VUB QUIZ APP")
root.geometry('500x300')
root.resizable(0,0)
root.configure(bg="black")

def getInfo():
    global name,window,Name
    Name = name.get()
    root.deiconify()
    window.destroy()
    
#############create some widget on the window##############
def addwidget():
    global name,window
    window=Toplevel(root)
    window.geometry('500x300')
    window.resizable(0,0)
    window.title('VUB QUIZ APP')
    window.config(bg='black')
    appName = Label(window,text=title,font=('impact',20,'italic'),justify=CENTER,bg='goldenrod2',fg='white')
    appName.pack(side=TOP,fill=BOTH)
    ###take info of the player
    lbl = Label(window, text="Are you ready to get your IQ tested?", font="50",fg='white',bg='black').place(x=100,y=100)
    name = Entry(window,width=30)
    name.place(x=120,y=135)
    name.insert(END,'Name')
    #name_label = Label(window, text="Name",fg='white',bg='black').place(x=120,y=135) 
    Submit_button = Button(window, text="Confirm",command=getInfo).place(x=200,y=200)
    window.mainloop()

#################function to end the game##############
def quit_game():
  quit = showinfo(message="Congratulations you finish the game") 
  if quit == 'ok':
      sys.exit(root.destroy())
      
####################function to disable all the button###############
def disable_allbuttons():
    option1.config(state=DISABLED)
    option2.config(state=DISABLED)
    option3.config(state=DISABLED)
    option4.config(state=DISABLED)
    
###################function to enable all the buttons###################
def enable_allbuttons():
    option1.config(state=NORMAL)
    option2.config(state=NORMAL) 
    option3.config(state=NORMAL)
    option4.config(state=NORMAL)
          
######################## show the final result#########################
def result():
    global score,Name,Roll
    root.withdraw()
    top = Toplevel(root)
    top.geometry('200x100')
    top.resizable(0,0)
    top.title('Quiz Result')
    top.config(bg='blue')
    top.protocol('WM_DELETE_WINDOW',quit_game)
    #store the result in txt file
    filename = Name +'.txt'
    data = '\nPlayer: '+ Name + '\nScore: ' + str(score)
    with open(os.path.join(os.path.expanduser('~'),'results', filename),'a') as file:
    #with open(os.path.join('results', filename),'a') as file: this does not work and I don't know why????
        file.write(data)
    lbl = Label(top,text='Quiz Over...\n Score: '+str(score),font=30,fg='white',bg='blue').place(x=50,y=25)
    exit_button = Button(top,text='Exit',width=10,bg='black',fg='red',command=quit_game).place(x=50,y=70)
    top.mainloop()
    
###############questions and corresponding answers ########
questions = {"What is Robin's age?":"25",
             "What is the first element in the periodic table?":"Hydrogen"}
    
############# separate questions and answers 
que = []
ans= []
for key,value in questions.items():
    que.append(key)
    ans.append(value)

############## corresponding answers with answers including at random ############
options = [
    ['19','22',ans[0],'109'],
    [ans[1],'Lithium','Uranium','adamantium']
    ]

#######################################
currentQ ='' #current question
q_number=None
currentA='' #current answer
score = 0
qn = 1  #for printing No of question 
var = StringVar()

#############function to get to the next question############
def _next():
    global currentQ,currentA,q_number,score,qn
    # when they are still question left
    if len(que)>0:
        currentQ = random.choice(que)
        print(currentQ)
        q = Label(root,text='Que. '+str(qn),font=('arial',10)).place(x=20,y=80)
        qn+=1
        q_number = que.index(currentQ)   
        print(options[q_number])
        currentA = questions[currentQ]
        #first change button name
        submit.config(text='Next')
        #print current question on quelabel
        queLabel.config(text=currentQ,fg='green',height=6)
        #print options for question on labels
        enable_allbuttons()
        option1.config(text=options[q_number][0],bg='sky blue',value=options[q_number][0],bd=1,command=answer)
        option2.config(text=options[q_number][1],bg='sky blue',value=options[q_number][1],bd=1,command=answer)
        option3.config(text=options[q_number][2],bg='sky blue',value=options[q_number][2],bd=1,command=answer)
        option4.config(text=options[q_number][3],bg='sky blue',value=options[q_number][3],bd=1,command=answer)
        # remove question that are asked from the list
        que.remove(currentQ)
        ans.remove(currentA)
        options.remove(options[q_number])
    elif len(que)==0:
        result()
        
def answer():
    global currentQ,currentA,score
    #print selected radiobutton
    a = var.get()
    if currentA == str(a):
        score+=1
        disable_allbuttons()
    else:
        disable_allbuttons()
        
title='VUB QUIZ APP'
appName = Label(root,text=title,font=('impact',20,'italic'),
                justify=CENTER,bg='goldenrod2',fg='white')
appName.pack(side=TOP,fill=BOTH)
#label to show current question    
queLabel = Label(root,text='',justify=LEFT,font=25)
queLabel.pack(side=TOP,fill=BOTH)
#s = Separator(root).place(x=0,y=195)
#options labels
option1=Radiobutton(root,text='',bg='black',font=20,width=20,relief=FLAT,
                    indicator=0,value=1,variable = var,bd=0)
option1.place(x=100,y=150)
option2=Radiobutton(root,text='',bg='black',font=20,width=20,relief=FLAT,
                    indicator=0,value=2,variable = var,bd=0)
option2.place(x=300,y=150)
option3=Radiobutton(root,text='',bg='black',font=20,width=20,relief=FLAT,
                    indicator=0,value=3,variable = var,bd=0)
option3.place(x=100,y=200)
option4=Radiobutton(root,text='',bg='black',font=20,width=20,relief=FLAT,
                    indicator=0,value=4,variable = var,bd=0)
option4.place(x=300,y=200)
#submit button
submit = Button(root,text='Get started',bg='blue',fg='white',width=15,font=('impact',15),command=_next)
submit.pack(side=BOTTOM)

if __name__ =="__main__":
    root.withdraw()
    addwidget()
    root.mainloop()'''
