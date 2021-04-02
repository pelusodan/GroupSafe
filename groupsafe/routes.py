from flask import render_template, url_for, flash, redirect, request, session
from groupsafe import app, db, bcrypt
from groupsafe.forms import RegistrationForm, LoginForm
from groupsafe.models import *
from flask_login import login_user, current_user, logout_user, login_required

#endpoint for the index page
@app.route('/')
def index():
    return render_template('index.html')

#endpoint for the home page
@app.route('/home')
def home():
    return render_template('home.html') 

#endpoint for the login page
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

#endpoint for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#endpoint for logging out the user, goes to the homepage
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))