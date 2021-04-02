After cloning the repo and moving into its directory, I recommend using a Python virtual environment:
```
virtualenv venv
source venv/bin/activate
```
Now you can install all the packages and dependencies in requirements.txt:
```
pip3 install -r requirements.txt
```
You can also use `pip` instead of `pip3`, depending on your setup. If you ever install more packages, make sure to add them to the requirements.txt file by doing:
```
pip3 freeze > requirements.txt
```
Now, you only need to create the database (locally) before running the application. Run:
```
python3
>>> from groupsafe import db
>>> from groupsafe.models import *
>>> db.create_all()
>>> exit()
```
This will create the database and all its tables, which are written as classes in the models.py file. 

Run the app and access it on localhost:5000 in your browser:
```
python3 run.py
```