import tkinter
from tkinter import ttk
from tkinter import messagebox
import darkdetect
import cv2
import numpy as np
import sv_ttk
import tk_async_execute as tae
from PIL import Image, ImageTk

from util.resources import resource_path
from util.webSocketHandler import openSocket, stopSocket


from interface.verifyAndConfirm import verifyUI, confirmScreen
from interface.welcome import welcome_page
from interface.settings import settingsUI
from interface.loadingScreen import loadingScreen
from interface.doneScreen import doneScreen


class mainUI:

    # this class basically runs the main interface for the program,
    # all of the ui functionallity for each section of the program is contained within frames
    # we switch between the UIs with the switchUI function

    def exitProgram(self):
        stopSocket()
        self.root.destroy()

    def __init__(self):
        self.root = tkinter.Tk()
        # set up interface and icon
        self.root.title("EasyVerify")
        self.root.geometry("1280x720")
        self.root.iconphoto(
            False, tkinter.PhotoImage(file=resource_path("assets\\icon.png"))
        )
        self.root.config(bg="skyblue")
        sv_ttk.set_theme(darkdetect.theme())

        self.verifyInterface = verifyUI(self)  # generate the verification UI
        self.settingsInterface = settingsUI(self)
        self.welcomeInterface = welcome_page(self)
        self.confirmInterface = confirmScreen(self)
        self.loadingScreen = loadingScreen(self)
        self.doneInterface = doneScreen(self)

    #  self.signInInterface = sign_in(self)

    # make 3 objects for each ui, then switch between them all
    # start with the verifyui
    def runUI(self):
        # self.switchUI(self.settingsInterface.uiFrame, self.loadingScreen.uiFrame)
        # self.loadingScreen.loadingCircle()
        self.switchToWelcomePage()
        tae.start()
        self.root.protocol(
            "WM_DELETE_WINDOW", self.exitProgram
        )  # cleanup the websocket after closing the application
        self.root.mainloop()
        tae.stop()



    def switchUI(self, fromFrame, toFrame):
        # if the old frame is visible, we hide it
        if fromFrame.winfo_viewable():
            fromFrame.pack_forget()
        else:
            print("from frame already hidden")

        # if the new frame is not visible, we switch to the new one
        if not toFrame.winfo_viewable():
            toFrame.pack(fill="both", expand=True)
            toFrame.tkraise()
        else:
            print("to frame already visible")



    def switchVerify(self):
        self.switchUI(self.settingsInterface.uiFrame, self.verifyInterface.uiFrame)
        print("switching to verification UI")

    def switchSettings(self):
        self.switchUI(self.verifyInterface.uiFrame, self.settingsInterface.uiFrame)
        print("switching to settings UI")

    def switchToWelcomePage(self):
        self.switchUI(self.verifyInterface.uiFrame, self.welcomeInterface.uiFrame)
        print("switching to welcome UI")

    def switchFromWelcomePage(self):
        self.switchUI(self.welcomeInterface.uiFrame, self.verifyInterface.uiFrame)
        print("switching from welcome page")

    def switchVerifyToConfirm(self):
        self.switchUI(self.verifyInterface.uiFrame, self.confirmInterface.uiFrame)
        print("switching from welcome page")

    # def switchFromWelcomeToSignIn(self):
    #     self.switchUI(self.welcomeInterface.uiFrame, self.signInInterface.uiFrame)
    #     print("Switching to sign in page")
    def switchToLoadingUI(self):
        self.switchUI(self.confirmInterface.uiFrame, self.loadingScreen.uiFrame)
        print("switching to loading interface")
    def switchToCompleteUi(self):
        self.switchUI(self.verifyInterface.uiFrame, self.doneInterface.uiFrame)
        self.switchUI(self.loadingScreen.uiFrame, self.doneInterface.uiFrame)
