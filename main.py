from flask import Flask, render_template

app = Flask(__name__)

RANDOM_MSG = "Hello World"

# Create a home route
@app.route("/")
def home():
    return render_template("base.html", message=RANDOM_MSG)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)