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
        if user.userType == 'customer':
            return render_template("home_page.html", user=user, favDishes=user.getFavoriteDishes(None))
        else:
            return render_template("dashboard.html", user=user, userType=user.userType)

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
            session["cart"] = { "dish" : [], "quantity" : [] }

            usersInSession[user.id] = user
            # if user is a customer
            if user.userType == 'customer':
                if user.address == None and user.wallet == 0:
                    flash("IMPORTANT: Set delivery address and add funds to your account in your profile page before making your first order.", category = "warning")
                elif user.wallet == 0:
                    flash("IMPORTANT: Add funds to your account in your profile page before making your first order.", category = "warning")
                elif user.address == None:
                    flash("IMPORTANT: Set delivery address in your profile page before making your first delivery order.", category = "warning")
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
    session.pop("cart", None)
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
    
    cart = session.get("cart")

    if cart == None:
        flash("Session timed out, please try again", category="error")
        return redirect(url_for("loginPage"))

    items = getCartItems(mysql, cart)
    cartInfo = getCartInfo(items, user.isVIP)

    if request.method == 'POST':
        if "cart-submit" in request.form:
            if cartInfo["subtotal"] == 0:
                flash("Error: Your cart is empty.", category = "error")
            else:
                return redirect(url_for("checkoutPage"))
        else:
            dish_id = request.form["dish-id"]
            index = cart["dish"].index(dish_id)
            if "minus" in request.form:
                cart = updateQuantity(cart, index, "minus")
                session["cart"] = cart
                if cart["quantity"][index] == 0:
                    removeDishFromCart(dish_id)
                return redirect(url_for("cartPage"))
            if "plus" in request.form:
                cart = updateQuantity(cart, index, "plus")
                session["cart"] = cart
                return redirect(url_for("cartPage"))

    return render_template("cart_page.html", user=user, cart=items, cartInfo=cartInfo)


@app.route("/add-dish-to-cart/<id>", methods = ['POST'])
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
            # Get cart
            cart = session.get("cart")

            # the list cannot be found, most likely their session timed out
            if cart == None:
                flash("Session timed out, please try again", category="error")
                return redirect(url_for("loginPage"))

            if id in cart["dish"]:
                # if item already exists, increase quantity
                index = 0
                for item in cart["dish"]:
                    if item == id:
                        cart["quantity"][index] += 1
                    index += 1
            else:
                # append the new dish
                cart["dish"].append(id)
                cart["quantity"].append(1)
            session["cart"] = cart
    return redirect(url_for("cartPage"))

@app.route("/remove-dish-from-cart/<id>", methods = ['POST'])
def removeDishFromCart(id):
    '''
    Remove a dish from the cart
    '''
    userExist, user = isUserStillInSession()

    if not userExist:
        flash("Please Log In.", category="error")
        return redirect(url_for("loginPage"))

    if request.method == 'POST':
        cart = session.get("cart")

        if cart == None:
            flash("Session timed out, please try again", category="error")
            return redirect(url_for("loginPage"))

        index = cart["dish"].index(id)
        del cart["dish"][index]
        del cart["quantity"][index]
        session["cart"] = cart
        
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

    return render_template("dashboard.html", user=user, userType=user.userType)

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
        
# Run the app
if __name__ == "__main__":
    mysql = databaseInit(app) # Setup the database
    app.run(debug=True)