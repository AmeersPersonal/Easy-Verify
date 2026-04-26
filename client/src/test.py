import os
import tkinter as tk
from PIL import ImageTk, Image
from util.resources import resource_path

root = tk.Tk()
path = "assets\\loadingCircle\\"
filesList = sorted(
    [files for r,d, files in os.walk(path)][0],
    key= lambda x: int(''.join(filter(str.isdigit,x)))
) #HIDEOUS logic to sort the file names
print(filesList)
iter = 0


loadingLabel = tk.Label(root)


def loadingCircle():
    global iter
    global loadingLabel
    fileStr = resource_path(
        path + str(filesList[iter]).strip("[]'")
    )
    curImage = ImageTk.PhotoImage(Image.open(fileStr))
    loadingLabel.photo_image = curImage
    loadingLabel.configure(image=curImage)
    iter += 1
    if iter >= len(filesList):
        iter = 0

    loadingLabel.after(16, loadingCircle)
    pass
loadingCircle()

# Use it like a normal PhotoImage
loadingLabel.pack()
root.mainloop()
