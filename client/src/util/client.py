class Client:
    def __init__(self, userObject):
        self.first_name = userObject["firstName"]
        self.last_name = userObject["lastName"]
        self.oauth_token = userObject["oAuthToken"]
        self.callback_url = userObject["callBackURL"]
        self.client_id = userObject["clientID"]

    # todo fiest gotta properly set up
    def printAttrib(self):
        print(self.first_name)
