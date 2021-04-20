from flask import render_template, url_for, flash, redirect, request, session
from groupsafe import app, db, bcrypt
from groupsafe.forms import *
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
        group.number_of_users = len(group.users)
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Endpoint for creating a group
@app.route("/create_group", methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        if Group.query.filter_by(group_name=form.group_name.data).first() is None:
            group = Group(
                group_name=form.group_name.data,
                policy=form.policy.data,
                group_bio=form.group_bio.data)
            # need to add to database to get id
            db.session.add(group)
            db.session.commit()
            updatedGroup = get_group_from_name(group.group_name)
            user_group = UserGroup(
                user_id=current_user.id,
                group_id=updatedGroup.id,
                is_admin=True,
                status_enum=StatusEnum.Untested
            )
            db.session.add(user_group)
            db.session.commit()
            flash('Group: ' + form.group_name.data + ' added')
            return redirect(url_for('home'))
        else:
            flash('Group: ' + form.group_name.data + ' already exists!', category="error")

    return render_template('create_group.html', form=form)


# helper for querying group table by name
def get_group_from_name(group_name) -> Group:
    return Group.query.filter(Group.group_name == group_name).first()


# Endpoint for getting all user profile information for a specific user
@app.route("/user_profile/<username>", methods=['GET'])
@login_required
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return render_template("user_profile.html", user_data=user)
    else:
        return render_template("error.html")


# Endpoint for updating user account information
@app.route("/update_account/<username>", methods=['GET', 'POST'])
@login_required
def update_account(username):
    user = User.query.filter_by(username=username).first()
    form = UpdateProfileForm(obj=user)
    if form.validate_on_submit():
        db_username_check = User.query.filter_by(username=form.username.data).first()
        db_email_check = User.query.filter_by(email=form.email.data).first()
        if db_username_check is None or db_username_check.username == user.username:
            if db_email_check is None or db_email_check.username == user.username:
                user.username = form.username.data
                user.user_bio = form.user_bio.data
                user.email = form.email.data
                db.session.commit()
                return redirect(url_for('get_user_profile', username=user.username))
            else:
                flash('Email taken!', category="error")
        else:
            flash('Username taken!', category="error")

    if user is not None:
        return render_template("update_profile.html", user_data=user, form=form)
    else:
        return render_template("error.html")


@app.route("/change_password/<username>", methods=['GET', 'POST'])
@login_required
def change_password(username):
    user = User.query.filter_by(username=username).first()
    form = ChangePasswordForm(obj=user)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data) and current_user.username == username:
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('get_user_profile', username=user.username))
        else:
            flash('Incorrect Previous Password!', category="error")
    if user is not None:
        return render_template("change_password.html", user_data=user, form=form)
    else:
        return render_template("error.html")


# Endpoint for deleting a user's account
@app.route("/user_profile/delete")
@login_required
def remove_account():
    user = User.query.filter_by(username=current_user.username).first()
    groups = UserGroup.query.filter_by(user_id=user.id, is_admin=True)
    for group in groups:
        g = Group.query.filter_by(id=group.group_id).first()
        db.session.delete(g)
        db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))


# Endpoint for an individual group
@app.route("/group/<id>")
@login_required
def group(id):
    group = Group.query.filter_by(id=id).first()
    group_users = []
    is_admin = False
    is_member = False
    for user in group.users:
        group_users.append(user)
        if user.user.id == current_user.id:
            is_member = True
            if user.is_admin:
                is_admin = True
    if group is not None:
        return render_template(
            "group.html", 
            group_data=group, 
            group_users=group_users, 
            is_admin=is_admin, 
            is_member=is_member
        )
    else:
        return render_template("error.html")


# Endpoint for joining a group
@app.route("/join-group/<id>")
@login_required
def join_group(id):
    user_group = UserGroup(
        user_id=current_user.id,
        group_id=id,
        is_admin=False,
        status_enum=StatusEnum.Untested
    )
    db.session.add(user_group)
    db.session.commit()
    return redirect(url_for('home'))


# Endpoint for updating group information
@app.route("/update_group/<id>", methods=['GET', 'POST'])
@login_required
def update_group(id):
    group = Group.query.filter_by(id=id).first()
    form = UpdateGroupInfoForm(obj=group)
    if form.validate_on_submit():
        db_group_name_check = Group.query.filter_by(group_name=form.group_name.data).first()
        if db_group_name_check is None or db_group_name_check.group_name == group.group_name:
            group.group_name = form.group_name.data
            group.policy = form.policy.data
            group.group_bio = form.group_bio.data
            db.session.commit()
            return redirect(url_for('group', id=id))
        else:
            flash('Group name taken!', category="error")
    if group is not None:
        return render_template("update_group.html", form=form)
    else:
        return render_template("error.html")


# Endpoint for leaving a group
@app.route("/leave_group/<id>")
@login_required
def leave_group(id):
    user = UserGroup.query.filter_by(user_id=current_user.id, group_id=id)
    if user.first().is_admin:
        Group.query.filter_by(id=id).delete()
    user.delete()
    db.session.commit()
    return redirect(url_for('home'))


# Endpoint for updating the current user's status
@app.route("/update_status/<group_id>/<status>")
@login_required
def update_status(group_id, status):
    user= UserGroup.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    user.status_enum = status
    db.session.commit()
    return redirect(url_for('group', id=group_id))

