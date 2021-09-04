# save this as main.py
from types import MethodType
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
# , check_password_hash
# from flask import make_response, jsonify
# import json
import jsonpickle

from pathlib import Path
from api import models, product

# import os.path

import os
# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base
from api import database
from api import query
from api import call
import csv
from flask_login import LoginManager

# from flask import Blueprint
# main = Blueprint('main', __name__)

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = os.environ['SECRET']
login_manager = LoginManager() # Create a Login Manager instance
login_manager.login_view = 'index' # define the redirection path when login required and we attempt to access without being logged in
login_manager.init_app(app) # configure it for login

routing = "/api/v1/"

@login_manager.user_loader
def load_user(user_id): #reload user object from the user ID stored in the session
    # since the user_id is just the primary key of our user table, use it in the query for the user
    # return models.User.query.get(int(user_id))
    return models.User("1", "asd@asd", "asd", "asd")

@app.route(routing + "movies")
def get_movies():
    response = {}
    movie_list = base.build_list(database.connect_data())
    response['data'] = []
    # print(movie_list)
    # return response
    # return make_response(jsonify(response))
    # return json.dumps(vars(response))
    return jsonpickle.encode(query.pagination(request, response, movie_list))

@app.route(routing + "search")
def search_movies():
    response = {}
    movie_list = base.build_list(database.connect_data())
    response['data'] = []
    return jsonpickle.encode(query.search(request, response, movie_list))

@app.route(routing + "user")
def check_user():
    return call.sync_cloud()

@app.route(routing + "login", methods=["POST"])
def login_user():
    response = call.login_cloud(request.form.get('username')
    , request.form.get('password'))
    return response

@app.route("/hello")
def hello():
    return "Hello, World!"
  
@app.route("/geeks")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/index", methods=['GET', 'POST']) # define login page path
def index(): # define login page fucntion
    # return "It Works"
    if request.method=='GET': # if the request is a GET we return the login page
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        return render_template('index.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        response = product.login_web(email, password)
        print(response)
        user = models.User(
            response["data"]["userId"],
            response["data"]["email"],
            response["data"]["password"],
            response["data"]["username"]
            )
        # user = models.User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        # if not user:
        if response["data"] == "FAILED":
            flash('Please sign up before!')
            return redirect(url_for('signup'))
        # elif not check_password_hash(user.password, password):
        #     flash('Please check your login details and try again.')
        #     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('profile'))

@app.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = models.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('index'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = models.User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
        # add the new user to the database
        print(new_user)
        # db.session.add(new_user)
        # db.session.commit()
        return redirect(url_for('profile'))
    

@app.route("/profile") # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('index'))

@app.route('/', defaults={'path': ''})
@app.route("/<string:path>")
@app.route('/<path:path>')
def catch_all(path):
    if '.html' in path:
        path = path.split('.')[0]
    # return 'You want path: %s' % path
    current_path = Path(__file__).parent.resolve()
    test_file = Path(str(current_path) + "/templates/" + path + ".html")
    # print("asd " + path, flush=True)
    # print(current_path)
    # print(Path().resolve())
    if test_file.is_file():
    # if os.path.isfile("templates/" + path + ".html"):
        return render_template(path + '.html')
    return redirect(url_for('index')) 