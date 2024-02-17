from flask_login import UserMixin
import datetime

class User(UserMixin):
    id = 0
    email = ''
    name = ''
    password = ''
    date_of_birth = datetime.date(2001, 1, 1)
