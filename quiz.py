from tkinter import *

window = Tk()

window.title("VUB QUIZ APP")

window.geometry('500x450')
window.configure(bg="black")

lbl = Label(window, text="Are you ready to get your IQ tested?")
lbl.grid(column=1, row=0)

btn = Button(window, text="Get Started")
btn.grid(column=1, row=5)

window.mainloop()