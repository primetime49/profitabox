import requests, json

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