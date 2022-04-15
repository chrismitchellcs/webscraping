from . import db
from flask_login import UserMixin

class City(db.Model, UserMixin):
    url = db.Column(db.String(100), primary_key=True)
