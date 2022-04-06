from flask import Flask, render_template, request, redirect, session, url_for
from database import *
from dish import Dish

app = Flask(__name__)
mysql = None

# store each user id that correspond with a user object
usersInSession = {}

def isUserStillInSession():
    '''
    Verify if the user exist in session

    if the user exist, return the user object
    '''
    if "user" in session: # If the user has previous logged in
        user = usersInSession.get(session["user"]) # check the program's memory for the user
        
        if not user: # cannot find user from the program (most likely the website restart and the user had not close their browsers)
            user = getUserInDatabaseByID(mysql, session["user"])
            
            if not user:
                return (False, None)       

        return (True, user)
    
    return (False, None)

@app.route("/")
def homePage():
    '''
    Route to the home page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("home_page.html", user=user)

    return render_template("home_page.html", user=None)

@app.route("/about")
def aboutPage():
    '''
    Route to the about page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("about.html", user=user)
    
    return render_template("about.html", user=None)
    
@app.route("/menu")
def menu():
    '''
    Route to the menu page
    '''
    APPETIZERS = Dish.getAppetizers(None)

    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("menu.html", user=user, appetizers=APPETIZERS)

    return render_template("menu.html", user=None, appetizers=APPETIZERS)

@app.route("/login", methods = ['GET', 'POST'])
def loginPage():
    '''
    Route to the user login page
    '''
    if request.method == 'POST':
        user = getUserInDatabaseByLogin(mysql)
        if user != None: # Success
            session["user"] = user.id
            usersInSession[user.id] = user
            return redirect(url_for("homePage"))

        else:
            return render_template('login_page.html')

    return render_template("login_page.html")

@app.route("/logout")
def logout():
    '''
    Log out a user from the session
    '''
    session.pop("user", None)
    flash("You have successfully signed out", category="success")
    return redirect(url_for("loginPage"))

@app.route("/forgotpass/", methods = ['GET', 'POST'])
def forgotpassPage():
    '''
    Route to the forgot password page
    '''
    if request.method == 'POST':
        if forgotPassword(mysql):
            return redirect('/')
    return render_template('forgot_pass.html')

@app.route("/newuser/", methods = ['GET', 'POST'])
def newuserPage():
    '''
    Route to the new user page
    '''
    if request.method == 'POST':
        if verifyNewUser(mysql, usersInSession):
            return redirect('/')

    return render_template('new_user.html')

@app.route("/faqs")
def faqs():
    '''
    Route to the FAQs page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("faqs.html", user=user)

    return render_template("faqs.html", user=None)

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
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("tos.html", user=user)

    return render_template("tos.html", user=None)

@app.route("/privacy")
def privacyPolicy():
    '''
    Route to the privacy policy page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("privacy.html", user=user)

    return render_template("privacy.html", user=None)

@app.route("/customer-support")
def customerSupport():
    '''
    Route to the customer support page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("customer-support.html", user=user)

    return render_template("customer-support.html", user=None)

@app.route("/careers")
def careers():
    '''
    Route to the careers page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("careers.html", user=user)

    return render_template("careers.html", user=None)

# Run the app
if __name__ == "__main__":
    mysql = databaseInit(app) # Setup the database
    app.run(debug=True)