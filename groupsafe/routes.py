from flask import render_template, url_for, flash, redirect, request, session
from groupsafe import app, db, bcrypt
from groupsafe.forms import RegistrationForm, LoginForm, CreateGroupForm
from groupsafe.models import *
from flask_login import login_user, current_user, logout_user, login_required


# Endpoint for the index page
@app.route('/')
def index():
    return render_template('index.html')


# Endpoint for the home page
@app.route('/home')
@login_required
def home():
    user_group_ids = set()
    for user_group in current_user.groups:
        user_group_ids.add(user_group.group_id)

    groups = Group.query.all()
    # groups that a user is part of
    user_groups = []
    # groups that a user is not part of
    other_groups = []

    for group in groups:
        if group.id in user_group_ids:
            user_groups.append(group)
        else:
            other_groups.append(group)
    return render_template('home.html', user_groups=user_groups, other_groups=other_groups)


# Endpoint for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Username or password is incorrect.', 'danger')
    return render_template('login.html', form=form)


# Endpoint for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Endpoint for logging out the user, goes to the homepage
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Endpoint for creating a group
@app.route("/create_group", methods=['GET', 'POST'])
def createGroup():
    form = CreateGroupForm()
    if form.validate_on_submit():
        #TODO: add group to database based on models
        return redirect(url_for('home'))
    return render_template('create_group.html', form=form)


# Endpoint for getting all user profile information for a specific user
@app.route("/user_profile/<username>", methods=['GET'])
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return render_template("user_profile.html", user_data=user)
    else:
        return render_template("error.html")


# Endpoint for deleting a user's account
@app.route("/user_profile/delete/<username>", methods=['GET'])
def remove_account(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))
