from flask import Flask
from flask import render_template
# It takes a URL and creates a response for a route that simply redirects
# the user to the URL speci ed.
from flask import redirect
# It builds a URL from a function name.
from flask import url_for
from flask import request
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = "KEjD0UYZ/1YeciecjTW/m7qwczhQRVu7Zz9Iu0EaRAPn9uuWEuKz+VzsjXGplWQ2Dz7ICQRiFFTlqnnIuWCNrDDA3TJ5R9XaZg+T"
login_manager = LoginManager(app)


@app.route("/")
def home():
    # return "Under construction"
    return render_template("home.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        # Debug:
        print("Passwords don't match")
        return redirect(url_for("home"))
    if DB.get_user(email):
    	# Debug:
        print("We already have user with this email")
        return redirect(url_for("home"))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    # Debug: We'll print user list:
    print("User list:")
    DB.print_users()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return "You are logged in"


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user:
        print(stored_user['email'])
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()


@app.route("/logout")
# This function simply removes the session cookie from the user's browser.
def logout():
    logout_user()
    return redirect(url_for("home"))


# The decorator indicates to Flask-Login that this is the function we want to use
# to handle users who already have a cookie assigned,
# and it'll pass the user_id variable from the cookie to this function whenever a user visits our site,
# which already has one.
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
