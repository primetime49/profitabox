# save this as main.py
from types import MethodType
from flask import Flask, render_template, redirect, url_for, request
# from flask import make_response, jsonify
# import json
import jsonpickle

from pathlib import Path

# import os.path

# import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base
from api import database
from api import query
from api import call

app = Flask(__name__, static_url_path='', static_folder='static')

routing = "/api/v1/"

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

@app.route("/index")
def index():  
    return render_template('index.html')

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