from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# configure db with your details
app.config['SECRET_KEY'] = 'ndjasndkjsan'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '8814'
app.config['MYSQL_DB'] = 'team_m_restaurant'

mysql = MySQL(app)

@app.route("/")
def homePage():
    '''
    Route to the home page
    '''
    return render_template("home_page.html")

@app.route("/about")
def aboutPage():
    return render_template("about.html")
    
@app.route("/menu/")
def menu():
    '''
    Route to the menu page
    '''
    return render_template("menu.html")

@app.route("/login/", methods = ['GET', 'POST'])
def loginPage():
    '''
    Route to the user login page
    '''
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        # checks if user exists in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            return render_template('home_page.html')
        else:
            # account does not exist or username/password is incorrect
            flash('Username/password is incorrect.', category = 'error')
    return render_template('login_page.html')

@app.route("/forgotpass/")
def forgotpassPage():
    return render_template('forgot_pass.html')


@app.route("/newuser/", methods = ['GET', 'POST'])
def newuserPage():
    if request.method == 'POST':
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
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            # username must be unique
            flash('Username already exists.', category = 'error')
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
            mysql.connection.commit()
            cursor.close()
            return redirect('/')

    return render_template('new_user.html')

@app.route("/faqs")
def faqs():
    '''
    Route to the FAQs page
    '''
    return render_template("faqs.html")

@app.errorhandler(404)
def pageNotFound(e):
    '''
    Route to this page is the page DNE
    '''
    return render_template("404.html")

@app.route("/tos")
def tos():
    '''
    Route to the terms of service page
    '''
    return render_template("tos.html")

@app.route("/privacy")
def privacyPolicy():
    '''
    Route to the privacy policy page
    '''
    return render_template("privacy.html")

@app.route("/customer-support")
def customerSupport():
    '''
    Route to the customer support page
    '''
    return render_template("customer-support.html")

@app.route("/careers")
def careers():
    '''
    Route to the careers page
    '''
    return render_template("careers.html")

@app.route("/delivery")
def delivery():
    '''
    Route to the delivery page
    '''
    return render_template("delivery.html")

@app.route("/cart-page")
def delivery():
    '''
    Route to the delivery page
    '''
    return render_template("cart-page.html")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)