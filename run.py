from groupsafe import app, db, bcrypt
from groupsafe.models import *

# Create dummy data the first time the application is ran
def seeds():
    groups = [
        Group(
            group_name = 'Software Engineering',
            policy = 'Show-up on time, Do your homework, Attend standups',
            group_bio = 'This group is for students in EECE 4520.'
        ),
        Group(
            group_name = 'Group S1',
            policy = 'Attend standups, Do your tickets, Review tickets',
            group_bio = 'This group is for members of group S1.'
        ),
        Group(
            group_name = 'Capstone Group J4',
            policy = 'Create something cool, Meet weekly',
            group_bio = 'This group is for members of the J4 EECE capstone group.'
        ),
        Group(
            group_name = 'Survivor NEU',
            policy = 'Outwit, Outplay, Outlast',
            group_bio = "Northeastern's Survivor Fanclub. True fans only."
        )
    ]

    hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
    user1 = User(username='alex_tapley', password = hashed_password, email = 'root1@gmail.com')
    user2 = User(username='joe_lynch', password=hashed_password, email='root2@gmail.com')
    user3 = User(username='allyson_vakhovskaya', password=hashed_password, email='root3@gmail.com')
    user4 = User(username='augusto_rivas', password=hashed_password, email='root4@gmail.com')
    user5 = User(username='dan_peluso', password=hashed_password, email='root5@gmail.com')
    user6 = User(username='matt_odonnell', password=hashed_password, email='root6@gmail.com')
    user7 = User(username='matt_hoffman', password=hashed_password, email='root7@gmail.com')
    user8 = User(username='prof_kokar', password=hashed_password, email='root8@gmail.com')

    user_groups = [
        UserGroup(
            user_id=8,
            group_id=1,
            is_admin=True,
            status_enum='Healthy'
        ),UserGroup(
            user_id = 1,
            group_id = 1,
            is_admin = False,
            status_enum = 'Healthy'
        ),
        UserGroup(
            user_id = 1,
            group_id = 2,
            is_admin = True,
            status_enum = 'Healthy'
        ),
        UserGroup(
            user_id = 1,
            group_id = 3,
            is_admin = True,
            status_enum = 'Healthy'
        ),
        UserGroup(
            user_id = 2,
            group_id = 1,
            is_admin = False,
            status_enum = 'Healthy'
        ),
        UserGroup(
            user_id=2,
            group_id=2,
            is_admin=False,
            status_enum='Healthy'
        ),
        UserGroup(
            user_id=2,
            group_id=4,
            is_admin=True,
            status_enum='Healthy'
        ),
        UserGroup(
            user_id=3,
            group_id=1,
            is_admin=False,
            status_enum='Untested'
        ),
        UserGroup(
            user_id=3,
            group_id=2,
            is_admin=False,
            status_enum='Untested'
        ),
        UserGroup(
            user_id=4,
            group_id=1,
            is_admin=False,
            status_enum='Negative'
        ),
        UserGroup(
            user_id=4,
            group_id=2,
            is_admin=False,
            status_enum='Negative'
        ),
        UserGroup(
            user_id=5,
            group_id=1,
            is_admin=False,
            status_enum='Recovering'
        ),
        UserGroup(
            user_id=5,
            group_id=2,
            is_admin=False,
            status_enum='Recovering'
        ),
        UserGroup(
            user_id=6,
            group_id=1,
            is_admin=False,
            status_enum='Symptomatic'
        ),
        UserGroup(
            user_id=6,
            group_id=2,
            is_admin=False,
            status_enum='Symptomatic'
        ),
        UserGroup(
            user_id=7,
            group_id=1,
            is_admin=False,
            status_enum='Positive'
        ),
        UserGroup(
            user_id=7,
            group_id=2,
            is_admin=False,
            status_enum='Positive'
        ),
        UserGroup(
            user_id=7,
            group_id=3,
            is_admin=False,
            status_enum='Positive'
        )
    ]

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)
    for group in groups:
        db.session.add(group)
    for user_group in user_groups:
        db.session.add(user_group)
    db.session.commit()


if __name__ == '__main__':
    # Only creates tables if they don't exist
    db.create_all()
    if User.query.filter_by(username='alex_tapley').first() is None:
        print('Running seeds...')
        seeds()
    app.run(debug=True)
