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
        return render_template("home_page.html", user=user, favDishes=user.getFavoriteDishes(None))

    return render_template("home_page.html", user=None, popularDishes=Dish.getPopularDishes(None))

@app.route("/about/")
def aboutPage():
    '''
    Route to the about page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("about.html", user=user)
    
    return render_template("about.html", user=None)
    
@app.route("/menu/")
def menu():
    '''
    Route to the menu page
    '''
    # Get all the dishes from the db
    APPETIZERS = Dish.getAppetizers(None)
    ENTREES = Dish.getEntrees(None)
    DESERTS = Dish.getDeserts(None)

    print(DESERTS)

    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("menu.html", 
            user=user,
            favDishes=user.getFavoriteDishes(None),
            appetizers=APPETIZERS,
            entrees=ENTREES,
            deserts=DESERTS)

    return render_template("menu.html", 
        user=None, 
        appetizers=APPETIZERS,
        entrees=ENTREES,
        deserts=DESERTS)

@app.route("/login/", methods = ['GET', 'POST'])
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

@app.route("/logout/")
def logout():
    '''
    Log out a user from the session
    '''
    session.pop("user", None)
    flash("You have successfully signed out.", category="success")
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
        if verifyNewUser(mysql):
            return redirect('/')

    return render_template('new_user.html')

@app.route("/faqs/")
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

@app.route("/tos/")
def tos():
    '''
    Route to the terms of service page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("tos.html", user=user)

    return render_template("tos.html", user=None)

@app.route("/privacy/")
def privacyPolicy():
    '''
    Route to the privacy policy page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("privacy.html", user=user)

    return render_template("privacy.html", user=None)

@app.route("/customer-support/")
def customerSupport():
    '''
    Route to the customer support page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("customer-support.html", user=user)

    return render_template("customer-support.html", user=None)

@app.route("/careers/")
def careers():
    '''
    Route to the careers page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        return render_template("careers.html", user=user)

    return render_template("careers.html", user=None)

@app.route("/cart/", methods = ['GET', 'POST'])
def cartPage():
    '''
    Route to the cart page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in #
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    else:
        if request.method == 'POST':
            return redirect(url_for("checkoutPage"))
            
    return render_template("cart_page.html", user=user)
    
@app.route("/checkout/", methods = ['GET', 'POST'])
def checkoutPage():
    '''
    Route to the checkout page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    return render_template("checkout_page.html", user=user)

@app.route("/order-placed/", methods = ['GET', 'POST'])
def orderPlacedPage():
    '''
    Route to order confirmation/order failure
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    return render_template("order_placed.html", user=user)

@app.route("/profile/", methods = ['GET', 'POST'])
def profilePage():
    '''
    Route to profile page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))
    if request.method == 'POST':
        if "pass-submit" in request.form:
            if forgotPassword(mysql):
                return redirect('/profile/')
        if "card-submit" in request.form:
            return redirect('/profile/')
        if "wallet-submit" in request.form:
            return redirect('/profile/')
        if "delete-submit" in request.form:
            return redirect('/profile/')
    return render_template("profile_page.html", user=user)

@app.route("/orders/")
def orders():
    '''
    Route to the orders page
    '''
# Get all the orders from the db

    # CURRENTORDERS = Dish.getCurrentOrders(None)
    # PASTORDERS = Dish.getPastOrders(None)
    # POPULARS = Dish.getPopulars(None)

    userExist, user = isUserStillInSession()
    if not userExist:
        return redirect(url_for("loginPage"))
    else:
        return render_template("orders.html")


    # User is not signed in
    #if not userExist:
        #flash("Please Log In", category="error")
        #return redirect(url_for("loginPage"))


    return render_template("orders.html",
        user=None,
        currentOrders=CURRENTORDERS,
        pastOrders=PASTORDERS,
        pupulars=POPULARS)

    #return render_template("orders.html", user=user)

@app.route("/dashboard/")
def dashboard():
    '''
    Route to the dashboard page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In", category="error")
        return redirect(url_for("loginPage"))

    return render_template("dashboard.html", user=user, userType="manager")

@app.route("/dashboard-discussions/")
def dashboardDiscussions():
    '''
    Route to the discussions page

    vary between user types
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In", category="error")
        return redirect(url_for("loginPage"))

    return render_template("dashboard-discussions.html", user=user, userType=user.userType)

@app.route("/dashboard-comments/")
def dashboardComments():
    '''
    Route to the comments page

    vary between user types
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In", category="error")
        return redirect(url_for("loginPage"))

    return render_template("dashboard-comments.html", user=user, userType=user.userType)

@app.route("/add-dish-to-cart/<id>", methods = ['GET', 'POST'])
def addDishToCart(id):
    '''
    Add a dish to the user cart
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if request.method == "POST":
        if not userExist:
            flash("Please Log In", category="error")
            return redirect(url_for("loginPage"))

        else:
            user.addOrder(id)
            return redirect(url_for("cartPage"))
        
# Run the app
if __name__ == "__main__":
    mysql = databaseInit(app) # Setup the database
    app.run(debug=True)