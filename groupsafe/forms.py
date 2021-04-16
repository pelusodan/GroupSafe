from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from groupsafe.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CreateGroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired(), Length(max=30)])
    policy = StringField('Policies (comma separated)', validators=[DataRequired(), Length(min=1)])
    group_bio = StringField('Group Bio', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Length(min=3, max=100)])
    user_bio = StringField('Bio', validators=[Length(max=256)])
    submit = SubmitField('Update')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Previous Password', validators=[DataRequired(), Length(min=3)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')

class UpdateGroupInfoForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired(), Length(max=30)])
    policy = StringField('Policies (comma separated)', validators=[DataRequired(), Length(min=1)])
    group_bio = StringField('Group Bio', validators=[Length(max=256)])
    submit = SubmitField('Update')
