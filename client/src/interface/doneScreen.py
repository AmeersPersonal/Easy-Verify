import tkinter
from tkinter import ttk
import sv_ttk

class doneScreen:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI
        self.doneLabel = tkinter.Label(self.uiFrame, text="Done Verifying")
        self.statusLabel = tkinter.Label(self.uiFrame)
        self.doneLabel.pack()

    def setStatus(self, statusText):
        self.statusLabel.configure(text=statusText)
        self.statusLabel.pack()
