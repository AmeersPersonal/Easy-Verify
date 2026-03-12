import tkinter
from tkinter import ttk
import cv2
from PIL import ImageTk, Image
import sv_ttk

root = None

def generateInterface():
    global root
    root = tkinter.Tk() #Tkinter Setup, this is the main window of the application 
    root.title("EasyVerify")
    root.geometry("1280x720")
    
    
    actionsLabel = ttk.Label(root, text="Welcome to EasyVerify")
    actionsLabel.pack()
    
    def buttonAction(): 
        print("Hello")

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


    button = ttk.Button(root, text="Hello!", command=buttonAction)
    button.pack()

    sv_ttk.set_theme("dark")
    root.mainloop()
    