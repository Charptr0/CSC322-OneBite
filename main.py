from re import A
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

@app.route("/",  methods = ['GET', 'POST'])
def homePage():
    '''
    Route to the home page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("home_page.html", user=user, favDishes=user.getFavoriteDishes(None))
        else:
            return redirect(url_for("dashboard"))

    return render_template("home_page.html", user=None, popularDishes=Dish.getPopularDishes(None))

@app.route("/about/")
def aboutPage():
    '''
    Route to the about page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("about.html", user=user)
        else:
            return redirect(url_for("homePage"))
    
    return render_template("about.html", user=None)
    
@app.route("/menu/")
def menu():
    '''
    Route to the menu page
    '''
    # Get all the dishes from the db
    APPETIZERS = Dish.getAppetizers(mysql)
    ENTREES = Dish.getEntrees(mysql)
    DESERTS = Dish.getDeserts(mysql)
    DRINKS = Dish.getDrinks(mysql)
    SPECIALS = Dish.getSpecials(mysql)
    
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("menu.html", 
                user=user,
                appetizers=APPETIZERS,
                entrees=ENTREES,
                deserts=DESERTS,
                drinks=DRINKS,
                specials=SPECIALS)
        else:
            return redirect(url_for("homePage"))

    return render_template("menu.html", 
        user=None, 
        appetizers=APPETIZERS,
        entrees=ENTREES,
        deserts=DESERTS,
        drinks=DRINKS)

@app.route("/login/", methods = ['GET', 'POST'])
def loginPage():
    '''
    Route to the user login page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("You are already logged in.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        user = getUserInDatabaseByLogin(mysql)
        if user != None: # Success
            session["user"] = user.id
            session["orders"] = []

            usersInSession[user.id] = user
            # if user is a customer
            if user.userType == 'customer':
                if user.address == None and user.wallet == 0:
                    flash("Set delivery address and add funds to your account in your profile page before making your first order.")
                elif user.wallet == 0:
                    flash("Add funds to your account in your profile page before making your first order.")
                elif user.address == None:
                    flash("Set delivery address in your profile page before making your first order.")
                if user.warnings > 0:
                    flash("You have {0} warning(s), please check our dashboard".format(user.warnings), category = "error")
                return redirect(url_for("homePage"))
            # if user is an employee
            else:
                return redirect(url_for("dashboard"))

        else:
            return render_template('login_page.html')

    return render_template("login_page.html")

@app.route("/logout/")
def logout():
    '''
    Log out a user from the session
    '''
    session.pop("user", None)
    session.pop("orders", None)
    flash("You have successfully signed out.", category="success")
    return redirect(url_for("loginPage"))

@app.route("/forgot-password/", methods = ['GET', 'POST'])
def forgotpassPage():
    '''
    Route to the forgot password page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("Please logout first.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if forgotPassword(mysql):
            return redirect('/')

    return render_template('forgot_pass.html')

@app.route("/newuser/", methods = ['GET', 'POST'])
def newuserPage():
    '''
    Route to the new user page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            flash("Please logout first.", category = "error")
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if verifyNewUser(mysql):
            return redirect('/login/')

    return render_template('new_user.html')

@app.route("/faqs/")
def faqs():
    '''
    Route to the FAQs page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("faqs.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("faqs.html", user=None)

@app.errorhandler(404)
def pageNotFound(e):
    '''
    Route to this page is the page DNE
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("404.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("404.html", user=None)

@app.route("/tos/")
def tos():
    '''
    Route to the terms of service page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("tos.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("tos.html", user=None)

@app.route("/privacy/")
def privacyPolicy():
    '''
    Route to the privacy policy page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("privacy.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("privacy.html", user=None)

@app.route("/customer-support/")
def customerSupport():
    '''
    Route to the customer support page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("customer-support.html", user=user)
        else:
            return redirect(url_for("homePage"))

    return render_template("customer-support.html", user=None)

@app.route("/careers/")
def careers():
    '''
    Route to the careers page
    '''
    userExist, user = isUserStillInSession()
    if userExist:
        if user.userType == 'customer':
            return render_template("careers.html", user=user)
        else:
            return redirect(url_for("homePage"))

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
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    orders = session.get("orders")

    if orders == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    # Get all the dishes
    dishes = []
    for id in orders:
        dishes.append(Dish.getDishFromID(mysql, id))

    # Calculate the subtotal, tax, and total
    subtotal = 0
    for dish in dishes: subtotal += dish.price
    tax = subtotal * 0.085
    total = subtotal + tax

    if user.isVIP == 1:
        discount = subtotal * 0.05
        total -= discount

        if request.method == 'POST':
            if total == 0: 
                return redirect(url_for("cartPage"))

            return redirect(url_for("checkoutPage", user=user, order=dishes, subtotal=subtotal, tax=round(tax, 2), total=round(total, 2), discount=round(discount, 2)))

        return render_template("cart_page.html", user=user, order=dishes, subtotal=subtotal, tax=round(tax, 2), total=round(total, 2), discount=round(discount, 2))
    
    else:
        if request.method == 'POST':
            if total == 0: 
                return redirect(url_for("cartPage"))

            return redirect(url_for("checkoutPage", user=user, order=dishes, subtotal=subtotal, tax=round(tax, 2), total=round(total, 2), discount=0.0))

        return render_template("cart_page.html", user=user, order=dishes, subtotal=subtotal, tax=round(tax, 2), total=round(total, 2), discount=0.0)

@app.route("/remove-dish-from-cart/<id>", methods = ['GET', 'POST'])
def removeDishFromCart(id):
    '''
    Remove a dish from the cart
    '''
    userExist, user = isUserStillInSession()

    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        orders = session.get("orders")

        if orders == None:
            flash("Session timed out, please try again", category="error")
            return redirect(url_for("loginPage"))

        orders.remove(id)
        session["orders"] = orders
        
        return redirect(url_for("cartPage"))

    
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
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        return redirect(url_for("orderPlacedPage", total=request.args.get("total")))

    orders = session.get("orders")

    if orders == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    # Get all the dishes
    dishes = []
    for id in orders:
        dishes.append(Dish.getDishFromID(mysql, id))
    
    return render_template("checkout_page.html", user=user, order=dishes, 
        subtotal=request.args.get("subtotal"), tax=request.args.get("tax"), total=request.args.get("total"), discount=request.args.get("discount"))

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
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    total = float(request.args.get("total"))

    if user.wallet < total:
        user.warnings += 1 # Give the user an warning
        return render_template("order_placed.html", user=user, success=False)
    else:
        user.wallet -= total # Subtract the amount from the wallet
        session["orders"] = []

        return render_template("order_placed.html", user=user, success=True)


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
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))

    if request.method == 'POST':
        if "pass-submit" in request.form:
            if forgotPassword(mysql):
                return redirect('/profile/')
        if "address-submit" in request.form:
            if changeAddress(mysql, user):
                return redirect('/profile/')
        if "card-submit" in request.form:
            if changeCard(mysql, user):
                return redirect('/profile/')
        if "wallet-submit" in request.form:
            if chargeFunds(mysql, user):
                return redirect('/profile/')
        if "delete-submit" in request.form:
            if deleteAcc(mysql, user):
                flash('Successful! Your deposit will be cleared and the account will be deleted.', category = 'success')
                return redirect('/logout/')
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
    elif userExist and user.userType != 'customer':
        return redirect(url_for("homePage"))
    else:
        return render_template("orders.html")


    # User is not signed in
    #if not userExist:
        #flash("Please Log In", category="error")
        #return redirect(url_for("loginPage"))

    return render_template("orders.html", user=user)

@app.route("/dashboard/",  methods = ['GET', 'POST'])
def dashboard():
    '''
    Route to the dashboard page
    '''
    userExist, user = isUserStillInSession()

    # User is not signed in
    if not userExist:
        flash("Please Log In", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        if "disputesubmit" in request.form:
            retrieveDispute(mysql)
        if "complaintsubmit" in request.form:
            retrieveComplaint(mysql)
        if "editsubmit" in request.form:
            print("test\n\n")
            edititem(mysql)
        if "removeitem" in request.form:
            removeitem(mysql)
        if "addsubmit" in request.form:
            additem(mysql)
            
    if user.userType == "manager":
        rows=loadDisputes(mysql)
        # print(rows)
        CHEFS, DELIVERYS, CUSTOMERS = retrieveUsers(mysql)
        return render_template("dashboard.html", user=user, userType=user.userType, rows=rows,chefs=CHEFS, deliverys=DELIVERYS, customers=CUSTOMERS)
    if user.userType == "delivery":
        rows=loadPastDeliveries(mysql)
        print(rows)
        return render_template("dashboard.html", user=user, userType=user.userType, rows=rows)
    if user.userType == "chef":
        entree=loadEntrees(mysql)
        appetizers=loadAppt(mysql)
        desserts=loadDesserts(mysql)
        drinks=loadDrinks(mysql)
        # print(entree)
        # print(appetizers)
        # print(desserts)
        return render_template("dashboard.html", user=user, userType=user.userType,entree=entree, appetizers=appetizers,desserts=desserts,drinks=drinks)
    return render_template("dashboard.html", user=user, userType=user.userType)

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

@app.route("/forum/")
def forum():
    '''
    Route to the forum home page
    '''
    return render_template("forum_home.html")

@app.route("/forum_chef/")
def forumChef():
    '''
    Route to the forum chef page
    '''
    return render_template("forum_chef.html")

@app.route("/forum_staff/")
def forumStaff():
    '''
    Route to the forum staff page
    '''
    return render_template("forum_staff.html")

@app.route("/forum_appetizer/")
def forumAppetizer():
    '''
    Route to the forum appetizer page
    '''
    return render_template("forum_appetizer.html")

@app.route("/forum_entree/")
def forumEntree():
    '''
    Route to the forum entree page
    '''
    return render_template("forum_entree.html")

@app.route("/forum_drinks/")
def forumDrinks():
    '''
    Route to the forum drinks page
    '''
    return render_template("forum_drinks.html")

@app.route("/forum_post/")
def forumPost():
    '''
    Route to the forum post page
    '''
    return render_template("forum_post.html")

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
        elif userExist and user.userType != 'customer':
            return redirect(url_for("homePage"))

        else:
            # Get orders
            orders = session.get("orders")

            # the list cannot be found, most likely their session timed out
            if orders == None:
                flash("Session timed out, please try again", category="error")
                return redirect(url_for("loginPage"))

            # append the new dish
            orders.append(id)
            session["orders"] = orders

            return redirect(url_for("cartPage"))
        
# Run the app
if __name__ == "__main__":
    mysql = databaseInit(app) # Setup the database
    app.run(debug=True)