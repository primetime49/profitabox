# save this as main.py
from flask import Flask, render_template, redirect, url_for

from pathlib import Path
# import os.path

app = Flask(__name__, static_url_path='', static_folder='static')

routing = "/api/v1/"

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