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

root = tkinter.Tk()
camLabel = ttk.Label(root)
labelText = ttk.Label(root)
record = True


def runWebsocket():
    tae.async_execute(openSocket(), visible=False,pop_up=False, master=root)

def exitProgram():
    stopSocket()
    root.destroy()


def cameraAction():
    vid = cv2.VideoCapture(0) # init camera

    if not vid.isOpened():
        print("Webcam error")
        return


    camWidth, camHeight = 600, 400
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
    #get camera input
    # camLabel = ttk.Label(root).pack()
    camLabel.pack()

    def cameraCapture():
        _, frame = vid.read()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)

        photo_image = ImageTk.PhotoImage(image=captured_image)
        camLabel.photo_image = photo_image
        camLabel.configure(image=photo_image)
        if record:
            camLabel.after(1, cameraCapture)
        else:
           print("stopped camera") #catch next frame after 10 ms

    cameraCapture()


def buttonAction():
    #actionsLabel.config(text="Button Clicked!")
    global record
    record = False
    finishVerify()

def generateInterface():
    root.title("EasyVerify")
    root.geometry("1280x720")
    root.iconphoto(False, tkinter.PhotoImage(file=resource_path("assets\\icon.png")))


    labelText.config(text = "Welcome to EasyVerify")
    labelText.pack()
    button = ttk.Button(root, text="Verify Now", command=buttonAction)
    button.pack()
    sv_ttk.set_theme("dark")

    tae.start()
    cameraAction()
    settings()
    root.after(0, runWebsocket) # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
    # root.after(10,cameraAction)
    root.protocol("WM_DELETE_WINDOW", exitProgram) #cleanup the websocket after closing the application
    root.mainloop()
    tae.stop()

def settings():
    settings_button = ttk.Button(root, text="Settings", padding = (20, 10))
    settings_button.pack(side = "bottom", anchor = "nw")
    settings_button.pack()
