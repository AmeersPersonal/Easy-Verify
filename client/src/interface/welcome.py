import tkinter
from tkinter import ttk

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
