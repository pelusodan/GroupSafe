from groupsafe import app, db, bcrypt
from groupsafe.models import *
import click

@click.command()
def seeds():
    groups = [
        Group(
            group_name = 'Group 1',
            policy = 'Policy 1, policy 2, policy 3',
            group_bio = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
        ),
        Group(
            group_name = 'Group 2',
            policy = 'Policy 4, policy 5, policy 6',
            group_bio = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
        ),
        Group(
            group_name = 'Group 3',
            policy = 'Policy 7, policy 8, policy 9',
            group_bio = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
        ),
        Group(
            group_name = 'Group 4',
            policy = 'Policy 10, policy 11, policy 12',
            group_bio = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
        )
    ]

    hashed_password = bcrypt.generate_password_hash('user104').decode('utf-8')
    user = User(username = 'user1', password = hashed_password, email = 'root@gmail.com')

    user_groups = [
        UserGroup(
            user_id = 1,
            group_id = 1,
            is_admin = True,
            status_enum = 'Healthy'
        ),
        UserGroup(
            user_id = 1,
            group_id = 2,
            is_admin = True,
            status_enum = 'Recovering'
        )
    ]

    db.session.add(user)
    for group in groups:
        db.session.add(group)
    for user_group in user_groups:
        db.session.add(user_group)
    db.session.commit()
    
if __name__ == '__main__':
    seeds()