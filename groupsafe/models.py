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
    user_bio = db.Column(db.String(256))
    locked = db.Column(db.Boolean, default=False)
    incorrect_login_counter = db.Column(db.Integer)
    groups = relationship("UserGroup", back_populates="user")

    def __repr__(self):
        return f"('{self.id}', '{self.username}', '{self.email}')"

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20), unique=True, nullable=False)
    policy = db.Column(db.String(256), nullable=False)
    group_bio = db.Column(db.String(256), nullable=False)
    users = relationship("UserGroup", back_populates="group")

    def __repr__(self):
        return f"Group('{self.id}', '{self.group_name}', '{self.policy}', '{self.group_bio}')"

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
    status_enum = db.Column(db.Enum(StatusEnum), nullable=False)
    group = relationship("Group", back_populates="users")
    user = relationship("User", back_populates="groups")

    def __repr__(self):
        return f"('{self.user_id}', '{self.group_id}', '{self.is_admin}', '{self.status_enum}')"

