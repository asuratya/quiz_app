#####import some libraries
from tkinter import *
import random,sys
from tkinter.ttk import Separator,Progressbar
from tkinter.messagebox import showinfo
import os

##############to make the main window#############
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
    root.mainloop()
