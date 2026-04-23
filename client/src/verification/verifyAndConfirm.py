import tkinter
from tkinter import ttk, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

from util.resources import resource_path
from util.webSocketHandler import openSocket, stopSocket
from util.verificationHandler import startVerification

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
        print("eh")
        # tae.async_execute(
        #     openSocket(), visible=False, pop_up=False, master=self.mainUI.root
        # )

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
            messagebox.showerror("No Camera Found", "Camera not Found. Please close any apps using the camera, or check if it's disabled by the device."
                                   " Refresh the website to reverify.") 
            self.mainUI.root.destroy()
           
       

    def cameraInit(self):
        camWidth, camHeight = 600, 400
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
        # get camera input
        self.camLabel.pack()
        # catch next frame after 10 ms


        self.cameraCapture()


    def verifyAction(self):
        #startVerification(self.img1, self.img2, self.img3, self)
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
