

class Client():
    def __init__(self, userObject):
        self.first_name = userObject["first_name"]
        self.last_name = userObject["last_name"]
        self.oauth_token = userObject["oauth_token"]
        self.callback_url = userObject["callback_url"]
        self.client_id = userObject["client_id"]


    #todo fiest gotta properly set up
    def printAttrib(self):
        print(self.first_name)
