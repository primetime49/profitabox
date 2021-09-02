# save this as main.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
# from flask import make_response, jsonify
# import json
import jsonpickle

from pathlib import Path
from api import models

# import os.path

# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base
import csv

app = Flask(__name__, static_url_path='', static_folder='static')

routing = "/api/v1/"

@app.route(routing + "movies")
def get_movies():
    response = {}
    current_path = Path(__file__).parent.resolve()
    with open(str(current_path) + "/../movies_raw_v2.csv", 'r'
    , encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    movie_list = base.build_list(your_list)
    response['data'] = []
    # print(movie_list)
    # return response
    # return make_response(jsonify(response))
    # return json.dumps(vars(response))
    page = request.args.get('page')
    page_size =  request.args.get('pageSize')
    if page is None or page == "":
        page = 0
    else:
        page = int(page)
    if page_size is None or page_size == "":
        page_size = 25
    else:
        page_size = int(page_size)    
    for i in range(0, page+1):
        for j in range(i*page_size, i*page_size+page_size):
            response['data'].append(movie_list[j])
    return jsonpickle.encode(response)

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
        return render_template('index.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

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
            return redirect(url_for('auth.signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = models.User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
        # add the new user to the database
        print(new_user)
        # db.session.add(new_user)
        # db.session.commit()
        return redirect(url_for('auth.login'))
    

@app.route("/profile") # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('main.index'))

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