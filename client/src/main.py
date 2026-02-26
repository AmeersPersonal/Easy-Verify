from tkinter import *
import cv2
from PIL import Image, ImageTk # python image library

vid = cv2.VideoCapture(0) # init camera
camWidth, camHeight = 600, 400
vid.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)


root = Tk() #Tkinter Setup, this is the main window of the application 
root.title("EasyVerify")
root.geometry("1280x720")

def buttonAction(): 
    print("Hello")

#get camera input
camLabel = Label(root)
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


button = Button(root, text="Hello!", command=buttonAction)
button.pack()



root.mainloop()