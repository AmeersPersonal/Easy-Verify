import tkinter
from tkinter import ttk
import sv_ttk
import os
from util.resources import resource_path
from PIL import Image, ImageTk

class loadingScreen:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI

        self.path = "assets\\loadingCircle\\"
        self.filesList = sorted(
            [files for r,d, files in os.walk(self.path)][0],
            key= lambda x: int(''.join(filter(str.isdigit,x)))
        ) #HIDEOUS logic to sort the file names
        print(self.filesList)
        self.iter = 0
        self.loadingImage = tkinter.Label(self.uiFrame)
        self.loadingImage.pack()

        self.record = True

    def loadingCircle(self):
        self.mainUI.root.update_idletasks()
        self.fileStr = resource_path(
            self.path + str(self.filesList[self.iter]).strip("[]'")
        )
        self.curImage = ImageTk.PhotoImage(Image.open(self.fileStr))
        self.loadingImage.photo_image = self.curImage
        self.loadingImage.configure(image=self.curImage)
        self.iter += 1
        if self.iter >= len(self.filesList):
            self.iter = 0
        if self.record:
            self.uiFrame.after(1, lambda: self.loadingCircle())
