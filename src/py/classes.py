# My imports

# Package Imports
import datetime


# test class just to store users
class UserObj:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


# Test class to store sessions for authentication
class UserAuth:
    def __init__(self, user: str, auth: str, exp: datetime):
        self.user = user
        self.auth = auth
        self.exp = exp
