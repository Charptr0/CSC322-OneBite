from flask import Flask, render_template

app = Flask(__name__)

# Create a home page
@app.route("/")
def home():
    return render_template("home_page.html")

# Create a route to the home page
@app.route("/home/")
def homePage():
    return render_template("home_page.html")
    
# Menu page start
@app.route("/menu/")
def menu():
    return render_template("menu.html")


@app.route("/login/")
def loginPage():
    return render_template('login_page.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)