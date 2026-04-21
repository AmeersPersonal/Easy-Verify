import time
import tkinter
import asyncio
#from tkinter import ttk
import cv2
from util.resources import resource_path
from PIL import ImageTk, Image
import tk_async_execute as tae
from util.webSocketHandler import openSocket, stopSocket, finishVerify
import customtkinter as ctk
import sv_ttk

class verifyUI:
    def __init__(self, mainUI):
        self.uiFrame = ctk.CTkFrame(mainUI.root)
        self.mainUI = mainUI
        self.camLabel = tkinter.Label(self.uiFrame)
        self.labelText = ctk.CTkLabel(self.uiFrame)
        self.record = True

        self.labelText.configure(text = "Welcome to EasyVerify")
        self.labelText.pack()
        verifyButton = ctk.CTkButton(self.uiFrame, text="Verify Now", command=self.verifyAction)
        verifyButton.pack()

        settingsButton = ctk.CTkButton(self.uiFrame, text="Settings", width=100, command=self.mainUI.switchSettings)
        settingsButton.pack(side = "bottom", anchor = "nw")

        self.cameraAction()
        self.uiFrame.after(0, self.runWebsocket) # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
        # self.verifyFrame.after(10,self.cameraAction)
        #

    def runWebsocket(self):
        try:
            tae.async_execute(openSocket(), visible=False,pop_up=False)
        except Exception as e:
            print(e)

    def cameraAction(self):
        vid = cv2.VideoCapture(0) # init camera

        if not vid.isOpened():
            print("Webcam error")
            return

        camWidth, camHeight = 600, 400
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
        #get camera input
        # camLabel = ttk.Label(root).pack()
        self.camLabel.pack()

        def cameraCapture():
            _, frame = vid.read()

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)

            photo_image = ImageTk.PhotoImage(image=captured_image)
            self.camLabel.photo_image = photo_image
            self.camLabel.configure(image=photo_image)
            if self.record:
                self.camLabel.after(1, cameraCapture)
            else:
                print("stopped camera") #catch next frame after 10 ms
        cameraCapture()

    def verifyAction(self):
        #actionsLabel.config(text="Button Clicked!")
        self.record = False
        finishVerify()

        # settings_button = ttk.Button(self.verifyFrame)
        # settings_button.pack()

class settingsUI:
    def __init__(self, mainUI):
        self.uiFrame = ctk.CTkFrame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI

        settingsButton = ctk.CTkButton(self.uiFrame ,text="Go back to Main", command=self.mainUI.switchVerify)
        settingsButton.pack()

class mainUI:

    # this class basically runs the main interface for the program,
    # all of the ui functionallity for each section of the program is contained within frames
    # we switch between the UIs with the switchUI function

    def exitProgram(self):
        stopSocket()
        self.root.destroy()

    def __init__(self):
        self.root = ctk.CTk()
        # set up interface and icon
        self.root.title("EasyVerify")
        self.root.geometry("1280x720")
        self.root.iconphoto(False, tkinter.PhotoImage(file=resource_path("assets\\icon.png")))
        #self.root.config(bg ="skyblue")
      #  sv_ttk.set_theme("dark")

        self.verifyInterface = verifyUI(self) # generate the verification UI
        self.settingsInterface = settingsUI(self)
        self.welcomeInterface = welcome_page(self)

        #make 3 objects for each ui, then switch between them all
        # start with the verifyui
    def runUI(self):
        #self.switchVerify() # we start with the verification ui,
        tae.start()
        self.switchToWelcomePage()
       
        self.root.protocol("WM_DELETE_WINDOW", self.exitProgram) #cleanup the websocket after closing the application
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
            toFrame.pack(fill='both', expand=True)
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
        

class welcome_page:
     def __init__(self, mainUI):
        self.uiFrame = ctk.CTkFrame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI
       # text_area = ctk.CTK.Text(self.uiFrame)
       # text_area.pack()
      #  text_area.insert(ctk.CTk.END, "Welcome to Easy Verify! \n Would you like to sign in? (Optional)")
        continue_button = ctk.CTkButton(self.uiFrame ,text="Continue", command = self.mainUI.switchFromWelcomePage)
        continue_button.pack()