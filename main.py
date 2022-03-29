from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home/")
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

@app.route("/login/")
def loginPage():
    '''
    Route to the user login page
    '''
    return render_template('login_page.html')

@app.route("/forgotpass/")
def forgotpassPage():
    return render_template('forgot_pass.html')


@app.route("/newuser/")
def newuserPage():
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

# Run the app
if __name__ == "__main__":
    app.run(debug=True)