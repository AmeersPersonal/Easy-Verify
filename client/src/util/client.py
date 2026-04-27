class Client:
    def __init__(self, userObject):
        self.callback_url = userObject["callback_url"]
        self.email = userObject["email"]
        self.userID = userObject["userID"]

    # todo fiest gotta properly set up
    def printAttrib(self):
        pass
