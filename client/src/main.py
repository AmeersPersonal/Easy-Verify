from tkinter import *

root = Tk() #Tkinter Setup, this is the main window of the application 
root.title("EasyVerify")
root.geometry("1280x720")

def buttonAction():
    print("Hello")


button = Button(root, text="Hello!", command=buttonAction)
button.pack()
root.mainloop()