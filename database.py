from flask import request, flash, session
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

    # configure db with your details
    app.config['SECRET_KEY'] = data["SECRET_KEY"]
    app.config['MYSQL_HOST'] = data['MYSQL_HOST']
    app.config['MYSQL_USER'] = data['MYSQL_USER']
    app.config['MYSQL_PASSWORD'] = data["MYSQL_PASSWORD"]
    app.config['MYSQL_DB'] = data["MYSQL_DB"]

    return MySQL(app)

def isUserInDatabase(db):
    '''
    Check wether a user is in the database
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
        # create session data, which can be accessed in other routes
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']

        # redirect to registered customer home page
        flash('Logged in successfully!', category = 'success')
        return True

    else:
        # account does not exist or username/password is incorrect
        flash('Username/password is incorrect.', category = 'error')
        return False

def verifyNewUser(db, userInSession : list):
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

        userInSession.append(Customer(
            firstName=fname,
            lastName=lname,
            email=email,
            uname=username,
            password=password,
            phoneNumber=phone,
            cardNumber=card))
        return True
