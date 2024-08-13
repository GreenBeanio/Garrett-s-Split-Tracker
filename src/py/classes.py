# My imports

# Package Imports
import datetime


# test class just to store users
class UserObj:
    def __init__(self, username: str, hash_pass: str, salt: str):
        self.username = username
        self.hash_pass = hash_pass
        self.salt = salt


# Test class to store sessions for authentication
class UserAuth:
    def __init__(self, user: str, auth: str, exp: datetime):
        self.user = user
        self.auth = auth
        self.exp = exp
