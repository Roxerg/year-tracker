from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from goaldb import get_password_hash, get_user_by_id, get_user_by_name


def getUser(id):
    user = User(id)

    if (user.id == None or
        user.username == None or
        user.password_hash == None):
        return None

    return user



class User(UserMixin):


    def __init__(self, id=None, username=None):
        if (id != None):
            res = get_user_by_id(int(id))
        elif (username != None):
            res = get_user_by_name(username)
        else:
            res = [(None, None, None)]

        res = res[0]

        self.id = res[0]
        self.username = res[1]
        self.password_hash = res[2]


    def get_id(self):
        return self.id
    
    def is_anonymous(self):
        return False 

    def is_active(self):
        return (self.id != None or self.username != None or self.password_hash != None)

    def is_authenticated(self):
        return (self.id != None or self.username != None or self.password_hash != None)
   
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
