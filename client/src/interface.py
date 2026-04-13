import time
import tkinter
from tkinter import ttk
import cv2
from util.resources import resource_path
from PIL import ImageTk, Image
from util.webSocketHandler import connectionStatus, setConnectionStatus;
import tk_async_execute as tae
from util.webSocketHandler import openSocket;

import sv_ttk

root = None

def runWebsocket():
    tae.async_execute(openSocket(), visible=False,pop_up=False, master=root) 

def exitProgram():
    # tae.async_execute(setConnectionStatus(False), visible=False,pop_up=False, master=root) # set connection status to false so the websocket server can close itself gracefully
    root.destroy()



def cameraAction():
    vid = cv2.VideoCapture(0) # init camera
    camWidth, camHeight = 600, 400
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
    #get camera input
    camLabel = ttk.Label(root)
    camLabel.pack()
    def cameraCapture():
        _, frame = vid.read()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)

        photo_image = ImageTk.PhotoImage(image=captured_image)
        camLabel.photo_image = photo_image
        camLabel.configure(image=photo_image)
        camLabel.after(10, cameraCapture) #catch next frame after 10 ms

    cameraCapture()

def generateInterface():
    global root
    root = tkinter.Tk() #Tkinter Setup, this is the main window of the application 
    root.title("EasyVerify")
    root.geometry("1280x720")
    root.iconphoto(False, tkinter.PhotoImage(file=resource_path("assets/icon.png")))

    actionsLabel = ttk.Label(root, text="Welcome to EasyVerify").pack()

    def buttonAction(): 
        actionsLabel.config(text="Button Clicked!")

    button = ttk.Button(root, text="Hello!", command=buttonAction)
    button.pack()
    sv_ttk.set_theme("dark")
    
    tae.start()
    root.after(0, runWebsocket) # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
    root.protocol("WM_DELETE_WINDOW", exitProgram) #cleanup the websocket after closing the application
    #cameraAction()
    settings()
    root.mainloop()
    tae.stop()
    
def generateInterfaceV2():
    global root, main_frame, settings_frame
    root = tkinter.Tk() #Tkinter Setup, this is the main window of the application 
    root.title("EasyVerify")
    root.geometry("1280x720")
    root.iconphoto(False, tkinter.PhotoImage(file=resource_path("assets/icon.png")))
    main_frame = ttk.Frame(root)
    actionsLabel = ttk.Label(main_frame, text="Welcome to EasyVerify").pack()

    def buttonAction(): 
        actionsLabel.config(text="Button Clicked!")

    button = ttk.Button(main_frame, text="Hello!", command=buttonAction)
    button.pack()
    sv_ttk.set_theme("dark")
    
    tae.start()
    root.after(0, runWebsocket) # start the websocket server in the background so we can receive messages from the browser and update the UI accordingly
    root.protocol("WM_DELETE_WINDOW", exitProgram) #cleanup the websocket after closing the application
    #cameraAction()
    settings()
    root.mainloop()
    tae.stop()

def settings():
    settings_button = ttk.Button(root, text="Settings", padding = (20, 10))
    settings_button.pack(side = "bottom", anchor = "nw")