from groupsafe import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Enum
import enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    userBio = db.Column(db.String(256), nullable=False)
    locked = db.Column(db.Boolean, nullable=False)
    loginCounter = db.Column(db.Integer)
    incorrectLoginCounter = db.Column(db.Integer)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(20), unique=True, nullable=False)
    adminUsername = db.Column(db.String(20), unique=True, nullable=False)
    policy = db.Column(db.String(256), nullable=False)
    groupBio = db.Column(db.String(256), nullable=False)


class StatusEnum(enum.Enum):
    Positive = 'Positive'
    Negative = 'Negative'
    Untested = 'Untested'
    Healthy = 'Healthy'
    Symptomatic = 'Symptomatic'
    Recovering = 'Recovering'


class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    statusEnum = db.Column(db.Enum(StatusEnum), nullable=False)

