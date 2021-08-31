# save this as main.py
from flask import Flask, render_template, redirect, url_for, request
# from flask import make_response, jsonify
# import json
import jsonpickle

from pathlib import Path

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