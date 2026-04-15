import time
import tkinter
import asyncio
from tkinter import ttk
import cv2
from util.resources import resource_path
from PIL import ImageTk, Image
import tk_async_execute as tae
from util.webSocketHandler import openSocket, stopSocket, finishVerify

import sv_ttk

class verifyUI:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        self.mainUI = mainUI
        self.camLabel = ttk.Label(self.uiFrame)
        self.labelText = ttk.Label(self.uiFrame)
        self.record = True
        self.verificationState = 0 # 1 = first image taken 2: second 3: third
      #  self.img1, img2, img3 = #numpy array for image
       # self.currentImage = #same thing as 
        

        self.labelText.config(text = "Welcome to EasyVerify")
        self.labelText.pack()
        verifyButton = ttk.Button(self.uiFrame, text="Verify Now", command=self.verifyAction)
        verifyButton.pack()

        settingsButton = ttk.Button(self.uiFrame, text="Settings", padding = (20, 10), command=self.mainUI.switchSettings)
        settingsButton.pack(side = "bottom", anchor = "nw")

        self.cameraAction()
        self.uiFrame.after(0, self.runWebsocket) # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
        # self.verifyFrame.after(10,self.cameraAction)
        #

    def runWebsocket(self):
        tae.async_execute(openSocket(), visible=False,pop_up=False, master=self.uiFrame)

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
        if (self.verificationState > 3):
            #verificatio nhandler
            print("test")

        # settings_button = ttk.Button(self.verifyFrame)
        # settings_button.pack()

class settingsUI:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI

        settingsButton = tkinter.Button(self.uiFrame ,text="Go back to Main", command=self.mainUI.switchVerify)
        settingsButton.pack()

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
        self.root.iconphoto(False, tkinter.PhotoImage(file=resource_path("assets\\icon.png")))
        self.root.config(bg ="skyblue")
        sv_ttk.set_theme("dark")

        self.verifyInterface = verifyUI(self) # generate the verification UI
        self.settingsInterface = settingsUI(self)
        self.welcomeInterface = welcome_page(self)
      #  self.signInInterface = sign_in(self)

        #make 3 objects for each ui, then switch between them all
        # start with the verifyui
    def runUI(self):
        #self.switchVerify() # we start with the verification ui,
        self.switchToWelcomePage()
        tae.start()
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

    def switchVerify(self, ):
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
    
    # def switchFromWelcomeToSignIn(self):
    #     self.switchUI(self.welcomeInterface.uiFrame, self.signInInterface.uiFrame)
    #     print("Switching to sign in page")
    

class welcome_page:
     def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI
        labelText = "Welcome to Easy Verify! \n\n Would you like to opt into the database?"
        label = ttk.Label(self.uiFrame, text =labelText, font = ("Helvetica", 24, "bold")) 
        label.pack(pady = 30)
        var = tkinter.IntVar(self.uiFrame, value = 1)
        yes_button = tkinter.Radiobutton(self.uiFrame, text="Yes", variable=var, value="1")
        yes_button.pack()
        no_button = tkinter.Radiobutton(self.uiFrame, text="No", variable=var, value="2") 
        no_button.pack()
        
        
        # no_button = tkinter.Button(self.uiFrame,text="No", command = self.mainUI.switchFromWelcomePage)
        # #let me do my part bro dont do everythign
        # no_button.pack()
        continue_button = tkinter.Button(self.uiFrame,text="Continue", command = self.mainUI.switchFromWelcomePage)
        continue_button.pack()
        
# class sign_in:
#     def __init__(self, mainUI):
#         self.uiFrame = tkinter.Frame(mainUI.root)
#         self.mainUI = mainUI
#         label = ttk.Label(self.uiFrame, text ="Email", font = ("Georgia", 16, "bold"))
#         label.pack(pady = 10)
        
       
#         self.name_var=tkinter.StringVar()
#         self.passw_var=tkinter .StringVar()
#         email_entry = tkinter.Entry(self.uiFrame, textvariable = self.name_var, font=('calibre',10,'normal'))
#         email_entry.pack(pady=10)
#         passLabel = ttk.Label(self.uiFrame, text ="Password", font = ("Georgia", 16, "bold"))
#         passLabel.pack(pady = 10)
#         pass_entry = tkinter.Entry(self.uiFrame, textvariable = self.passw_var, font=('calibre',10,'normal'), show = "*")
#         pass_entry.pack(pady=10)
#         submit_button = tkinter.Button(self.uiFrame, text = "submit", command = self.submit)
#         submit_button.pack()
#     def submit(self):
       
#         self.name = self.name_var.get()
#         self.password=self.passw_var.get()
        
#         print("The name is : " + self.name)
#         print("The password is : " + self.password)
        
#         self.name_var.set("")
#         self.passw_var.set("")

       