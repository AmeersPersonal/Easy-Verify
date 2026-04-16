import tkinter
from tkinter import ttk

import darkdetect
import cv2
import numpy as np
import sv_ttk
import tk_async_execute as tae
from PIL import Image, ImageTk

from util.resources import resource_path
from util.webSocketHandler import openSocket, stopSocket
from util.verificationHandler import startVerification


"""
The verification process has 3 states:
    1: Take a picture of the front
    2: Take a picture from the left
    3: Take a picture from the right
"""


class verifyUI:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        self.mainUI = mainUI
        self.camLabel = ttk.Label(self.uiFrame)
        self.labelText = ttk.Label(self.uiFrame)
        self.record = True

        self.verificationState = 0  # 1 = first image taken 2: second 3: third
        self.img1, self.img2, self.img3 = (
            np.array([]),
            np.array([]),
            np.array([]),
        )  # numpy array for images
        self.currentImage = np.array([])  # same thing as ^

        self.labelText.config(text="Take a picture looking forward")
        self.labelText.pack()

        verifyButton = ttk.Button(
            self.uiFrame, text="Verify Now", command=self.verifyAction
        )
        verifyButton.pack()

        settingsButton = ttk.Button(
            self.uiFrame,
            text="Settings",
            padding=(20, 10),
            command=self.mainUI.switchSettings,
        )
        settingsButton.pack(side="bottom", anchor="nw")

        self.vid = cv2.VideoCapture(0)  # init camera

        if not self.vid.isOpened():
            print("Webcam error")
            return

        self.cameraInit()
        self.uiFrame.after(
            0, self.runWebsocket
        )  # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
        # self.verifyFrame.after(10,self.cameraAction)
        #
        self.go_back_to_welcome()
    
    
    def go_back_to_welcome(self):
        print("GO back on")
      
        goBack = tkinter.Button(self.uiFrame, text= "Back", font=("Helvetica", 16, "bold"), foreground="dark blue", background="light blue", command = self.mainUI.switchToWelcomePage)
        goBack.pack(side="top", anchor="nw")
    def runWebsocket(self):
        tae.async_execute(
            openSocket(), visible=False, pop_up=False, master=self.uiFrame
        )

    def cameraCapture(self):
        try:
            
            ret, frame = self.vid.read() #we care about the boolean value
            
            if not ret or frame is None:
                raise Exception()
            self.currentImage = frame
            imageDisplay = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(imageDisplay)

            photo_image = ImageTk.PhotoImage(image=captured_image)
            self.camLabel.photo_image = photo_image
            self.camLabel.configure(image=photo_image)
            if self.record:
                self.camLabel.after(1, self.cameraCapture)
            else:
                print("stopped camera")
            
        except Exception as e:
            print("Camera not Found. Please close any apps using the camera, or check if it's disabled by the device")
       
            
        
        

       

    def cameraInit(self):
        camWidth, camHeight = 600, 400
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
        # get camera input
        self.camLabel.pack()
        # catch next frame after 10 ms
      
   
        self.cameraCapture()


    def verifyAction(self):
        self.record = False
        if self.verificationState >= 3:
            print("error state")
            print(f"test + {self.verificationState}")

        else:
            self.mainUI.confirmInterface.updateImage(self.currentImage)
            self.mainUI.switchVerifyToConfirm()

    def confirmImage(self):
        # confirm image, but don't pass to next screen
        match (self.verificationState):
            case 0:
                self.img1 = self.currentImage.copy()
                print("img1")
                self.labelText.config(
                    text="Take a picture looking slightly to the Right"
                )
            case 1:
                self.img2 = self.currentImage.copy()
                print("img2")
                self.labelText.config(
                    text="Take a picture looking slightly to the Left"
                )
            case 2:
                self.img3 = self.currentImage.copy()
                print("img3")
                startVerification(self.img1, self.img2, self.img3, self)
                # TODO: do the verification here
            case _:
                print("Invalid State")
                exit(1)

        self.verificationState = self.verificationState + 1
        self.record = True
        self.cameraCapture()

    def failedVerify(self):
        self.verificationState = 0
        self.labelText.config(text="Verification failed, Try again")
        self.record = True
        self.cameraCapture()
        # settings_button = ttk.Button(self.verifyFrame)
        # settings_button.pack()


class confirmScreen:
    def __init__(self, mainUI):
        self.verifyUI = mainUI.verifyInterface
        self.uiFrame = tkinter.Frame(mainUI.root)
        self.mainUI = mainUI

        self.camLabel = ttk.Label(self.uiFrame)

        self.camLabel.pack()
        self.labelText = ttk.Label(self.uiFrame, text="Does this image look correct?")
        self.labelText.pack()
        self.confirmButton = ttk.Button(
            self.uiFrame, text="Confirm", command=self.confirm
        )
        self.confirmButton.pack()
        self.backButton = ttk.Button(self.uiFrame, text="Back", command=self.back)
        self.backButton.pack()

    def updateImage(self, image):
        imageDisplay = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(imageDisplay)

        photo_image = ImageTk.PhotoImage(image=captured_image)
        self.camLabel.photo_image = photo_image  # updates the visual image display
        self.camLabel.configure(image=photo_image)

    def confirm(self):
        self.mainUI.verifyInterface.confirmImage()
        print("wow")
        self.mainUI.switchUI(self.uiFrame, self.mainUI.verifyInterface.uiFrame)

    def back(self):
        self.mainUI.verifyInterface.record = True
        self.mainUI.verifyInterface.cameraCapture()
        print("notWow")
        self.mainUI.switchUI(self.uiFrame, self.mainUI.verifyInterface.uiFrame)


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
   
    #  self.signInInterface = sign_in(self)

    # make 3 objects for each ui, then switch between them all
    # start with the verifyui
    def runUI(self):
        # self.switchVerify() # we start with the verification ui,
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


class welcome_page:
    def __init__(self, mainUI):
        self.uiFrame = tkinter.Frame(mainUI.root)
        # self.uiFrame.pack(fill='both', expand=True)
        self.mainUI = mainUI
        labelText = (
            "Welcome to Easy Verify! \n\n Would you like to opt into the database?"
        )
        label = ttk.Label(self.uiFrame, text=labelText, font=("Helvetica", 24, "bold"))
        label.pack(pady=30)
        self.var = tkinter.IntVar(value=1)
    
        self.Welcome_Buttons()
        my_style = ttk.Style()
        my_style.configure('continue.TButton', font = ("Helvetica", 18, "bold"))
        continue_button = ttk.Button(
            self.uiFrame, text="Continue", style = 'continue.TButton', command=  self.user_choice
        )
        continue_button.pack(fill = tkinter.X, ipady = 3)

    def Welcome_Buttons(self):

        self.selected_choice = tkinter.StringVar(self.uiFrame, "1")

        values = {
        "Yes": "1",
        "No": "2",
        }
        self.current_value = "1"
        for text, value in values.items():
            tkinter.Radiobutton(
                self.uiFrame, text=text,font=("Helvetica", 24, "bold"), variable=self.selected_choice, value=value, indicator=0, foreground="dark blue", background="light blue",
                command = lambda x = value: self.on_click(x) ).pack(fill= tkinter.X, ipady=5, )
            

    def on_click(self, value):
        self.current_value = value
    
        
    def user_choice(self):
        if self.current_value == "1":
            print("User chose Yes")
        elif self.current_value == "2":
            print("User chose No")
        
        self.mainUI.switchFromWelcomePage()

        
    

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
