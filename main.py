from flask import Flask, render_template

app = Flask(__name__)

RANDOM_MSG = "Hello World"

# Create a home route
@app.route("/")
def home():
    return render_template("base.html", message=RANDOM_MSG)

# Create a route to the home page
@app.route("/home/")
def homePage():
    return render_template("home_page.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)