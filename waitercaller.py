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
from flask.ext.login import current_user

from user import User
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from forms import RegistrationForm
from forms import LoginForm
from forms import CreateTableForm

import config
import datetime

if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

app = Flask(__name__)
app.secret_key = "KEjD0UYZ/1YeciecjTW/m7qwczhQRVu7Zz9Iu0EaRAPn9uuWEuKz+VzsjXGplWQ2Dz7ICQRiFFTlqnnIuWCNrDDA3TJ5R9XaZg+T"
login_manager = LoginManager(app)


@app.route("/")
def home():
    return render_template("home_1.html", loginForm=LoginForm(), registrationForm=RegistrationForm())


@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("We already have a user with this email")
            return render_template("home_1.html", loginForm=LoginForm(), registrationForm=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        # Debug: We'll print user list:
        # print("User list:")
        # DB.print_users()
        # return redirect(url_for('home'))
        return render_template("home_1.html",
                               loginForm=LoginForm(),
                               registrationForm=form,
                               onloadMessage="Registration successful. Please log in.")
    return render_template("home_1.html", loginForm=LoginForm(), registrationForm=form)


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data,
                                                stored_user['salt'],
                                                stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home_1.html", loginForm=form, registrationForm=RegistrationForm())


@app.route("/logout")
# This function simply removes the session cookie from the user's browser.
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", createTableForm=CreateTableForm(), tables=tables)


@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    form = CreateTableForm(request.form)
    if form.validate():
        # We are using current_user method from FlaskLogin here.
        tableid = DB.add_table(form.tablenumber.data, current_user.get_id())
        # new_url = config.base_url + "newrequest/" + tableid
        # We are using str(tableid) because we are using ObjectId for Mongo.
        # This will ensure that tableid is always a string before we concatenate
        # it to our URL.
        new_url = BH.shorten_url(
            config.base_url + "newrequest/" + str(tableid))
        DB.update_table(tableid, new_url)
        return redirect(url_for('account'))
    return render_template("account.html",
                           createTableForm=form,
                           tables=DB.get_tables(current_user.get_id()))


@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))


@app.route("/newrequest/<tid>")
def new_request(tid):
    if DB.add_request(tid, datetime.datetime.now()):
		return "Your request has been logged and a waiter will be with you shortly"
	return "There is already a request pending for this table. Please be patient."


@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        delta_seconds = (now - req["time"]).seconds
        req['wait_minutes'] = "{}.{}".format(
            (delta_seconds/60), str(delta_seconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)


@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))

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
