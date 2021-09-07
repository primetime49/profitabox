import requests, json
import urllib.request

from api import models

def login_web(username, password):
    url = "https://product-goridepay.herokuapp.com/login/"
    myobj = {
        "username": username,
        "password": password
    }
    # myobj = "email=" + username + "&password=" + password
    header = {
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    x = requests.post(url, json = myobj, headers = header)
    # print(x)

    return json.loads(x.text)

def get_profile(email):
    url = "https://product-goridepay.herokuapp.com/db?email=" + email
    contents = urllib.request.urlopen(url).read()
    arr = json.loads(contents)
    return models.User(
        arr[0]["userId"],
        arr[0]["email"],
        arr[0]["password"],
        arr[0]["username"]
    )