
# import tkinter
# from tkinter import ttk

# root = tkinter.Tk()

# style = ttk.Style()
# style.map("C.TButton",
#     foreground=[('pressed', 'red'), ('active', 'blue')],
#     background=[('pressed', '!disabled', 'black'), ('active', 'white')]
#     )

# colored_btn = ttk.Button(text="Test", style="C.TButton").pack()

# root.mainloop()

# from tkinter import ttk
# import tkinter

# root = tkinter.Tk()

# style = ttk.Style()
# style.layout("TMenubutton", [
#    ("Menubutton.background", None),
#    ("Menubutton.button", {"children":
#        [("Menubutton.focus", {"children":
#            [("Menubutton.padding", {"children":
#                [("Menubutton.label", {"side": "left", "expand": 1})]
#            })]
#        })]
#    }),
# ])

# mbtn = ttk.Menubutton(text='Text')
# mbtn.pack()
# root.mainloop()

import tkinter
from tkinter import ttk



import sv_ttk

root = tkinter.Tk()

button = ttk.Button(root, text="Click me!")
button.pack()

# This is where the magic happens


root.mainloop()