from flask import request, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import sys

sys.path.append("./UserTypes")
from UserTypes import *

def databaseInit(app):
    '''
    Initialize the database
    '''

    # Setup the mysql with information from config.json
    data = None
    try:
        with open("config.json", "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        print("Config file cannot be found")
        exit(1)

    # configure db with your details
    app.config['SECRET_KEY'] = data["SECRET_KEY"]
    app.config['MYSQL_HOST'] = data['MYSQL_HOST']
    app.config['MYSQL_USER'] = data['MYSQL_USER']
    app.config['MYSQL_PASSWORD'] = data["MYSQL_PASSWORD"]
    app.config['MYSQL_DB'] = data["MYSQL_DB"]

    return MySQL(app)

def convertUser(account):
    '''
    Convert raw query from the database and into a user object

    **THIS IS A HELPER FUNCTION, DO NOT USE IT BY ITSELF**
    '''
    return Customer(
        id=account["id"],          
        firstName=account["fname"],
        lastName=account["lname"],
        email=account["email"],
        uname=account["username"],
        password=account["password"],
        phoneNumber=account["phone"],
        cardNumber=account["cardnumber"],
        userType=account["type"])

def getUserInDatabaseByLogin(db):
    '''
    Get a user from the database

    **USE THIS METHOD WHEN A USER IS ATTEMPTING TO LOG IN**

    return the user object if the account exist in the database 
    '''
    # fetch form data
    userDetails = request.form
    username = userDetails['username']
    password = userDetails['password']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        flash('Logged in successfully!', category = 'success')
        return convertUser(account)

    else:
        # account does not exist or username/password is incorrect
        flash('Username/password is incorrect.', category = 'error')
        return None

def getUserInDatabaseByID(db, id):
    '''
    Get a user from the database

    **USE THIS METHOD WHEN THE USER ID IS KNOWN**

    return the user object if the account exist in the database 
    '''
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (str(id)))
    account = cursor.fetchone()

    if account:
        return convertUser(account)

    else: 
        return None


def verifyNewUser(db):
    '''
    Check to make sure that the new user creation is successful
    '''
    # fetch form data
    userDetails = request.form
    fname = userDetails['fname']
    lname = userDetails['lname']
    email = userDetails['email']
    username = userDetails['uname']
    password = userDetails['password']
    conpass = userDetails['conpass']
    phone = userDetails['phone']
    card = userDetails['cardnum']

    # checks requirements for registration
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    if account:
        # username must be unique
        flash('Username already exists.', category = 'error')
        return False

    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        # email must be valid
        flash('Email address is invalid.', category = 'error')
    elif not re.search(r"[\d]+", password):
        # password must contain a digit
        flash('Password must contain at least 1 digit.', category = 'error')
    elif not re.search(r"[A-Z]+", password):
        # password must contain an uppercase letter
        flash('Password must contain at least 1 uppercase letter.', category = 'error')
    elif not re.search(r"[a-z]+", password):
        # password must contain a lowercase letter
        flash('Password must contain at least 1 lowercase letter.', category = 'error')
    elif len(password) < 8:
        # password must be at least 8 characters
        flash('Password must contain at least 8 characters.', category = 'error')
    elif password != conpass:
        # checks that password matches confirm password
        flash('Passwords do not match.', category = 'error')
    elif len(phone) != 10:
        # checks that phone number length is valid
        flash('Phone number is invalid. Must be 10 digits.', category = 'error')
    elif len(card) != 16:
        # checks that card number length is valid
        flash('Card number is invalid. Must be 16 digits.', category = 'error')
    else:
        # account pending creation. must be approved by manager to be added to database
        flash('Account pending creation!', category = 'pending')
        # inserts new account into database after approval by manager
        cursor.execute("INSERT INTO accounts(fname, lname, email, username, password, phone, cardnumber) VALUES(%s, %s, %s, %s, %s, %s, %s)", (fname, lname, email, username, password, phone, card))
        db.connection.commit()
        cursor.close()

        return True

def forgotPassword(db):
    '''
    Updates password in database
    '''
    # fetch form data
    userDetails = request.form
    email = userDetails['email']
    username = userDetails['username']
    newpass = userDetails['newpass']
    conpass = userDetails['conpass']

    # checks if user exists in the database
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND username = %s', (email, username,))
    account = cursor.fetchone()

    # if account exists in the database
    if account:
        if not re.search(r"[\d]+", newpass):
        # password must contain a digit
            flash('Password must contain at least 1 digit.', category = 'error')
        elif not re.search(r"[A-Z]+", newpass):
            # password must contain an uppercase letter
            flash('Password must contain at least 1 uppercase letter.', category = 'error')
        elif not re.search(r"[a-z]+", newpass):
            # password must contain a lowercase letter
            flash('Password must contain at least 1 lowercase letter.', category = 'error')
        elif len(newpass) < 8:
            # password must be at least 8 characters
            flash('Password must contain at least 8 characters.', category = 'error')
        elif newpass != conpass:
            # checks that password matches confirm password
            flash('Passwords do not match.', category = 'error')
        else:
            cursor.execute('UPDATE accounts SET password = %s WHERE email = %s AND username = %s', (newpass, email, username,))
            flash('Successfully changed password.', category = 'success')
            db.connection.commit()
            cursor.close()

            return True
    else:
        flash('Email/username does not exist.', category = 'error')