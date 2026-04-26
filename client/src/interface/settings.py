import tkinter
from tkinter import ttk
import sv_ttk

class settingsUI:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI

        settingsButton = ttk.Button(
            self.uiFrame, text="Go back to Main", command=self.mainUI.switchVerify
        )
        settingsButton.pack()
        self.change_theme()


    def change_theme(self):
        frame = self.uiFrame

        toggle_theme = ttk.Button(frame, text = "Toggle theme", command = sv_ttk.toggle_theme)
        toggle_theme.pack()

