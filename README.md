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

Run the app and access it on localhost:5000 in your browser:
```
python3 run.py
```

Note: If this is your first time running the app (or if you delete the database), the code will automatically create the database, its tables, and add dummy data to it for convenience. The dummy data consists of 4 groups and a user with username user1 and password user104. It will also add this user as a member to the first two groups. So, if you want to check out our app with some added data, feel free to log in with user1!