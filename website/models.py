from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    notes = db.relationship("Note")