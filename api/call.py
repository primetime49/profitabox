import urllib.request
import requests

def sync_cloud():
    url = "https://account-goridepay.herokuapp.com/api/v1/202001/employees"
    contents = urllib.request.urlopen(url).read()
    return contents

def login_cloud(username, password):
    url = "https://csui-bot-1.herokuapp.com/api/v1/login/"
    # myobj = {
    #     "email": username,
    #     "password": password
    # }
    myobj = "email=" + username + "&password=" + password
    # print(myobj)
    #use the 'headers' parameter to set the HTTP headers:
    h = {"Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*"}
    x = requests.post(url, data = myobj, headers = h)
    # x = requests.post(url, data = myobj)
    print(x)

    return x.text