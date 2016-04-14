import lxml.html
from lxml.cssselect import CSSSelector

import requests
import getpass

# SETUP GITHUB SESSION ---------------------------- #

session = requests.Session()

# LOGIN ------------------------------------- LOGIN #

#getting auth token
loginPage = session.get('https://github.com/login')
loginTree = lxml.html.fromstring(loginPage.text)
findAuth = CSSSelector('input[name="authenticity_token"]')
# print (lxml.html.tostring(tree))
authenticity_token = findAuth(loginTree)[0].get('value')
# print(authenticity_token)

# making post request with login data
# get user info from CL
print("logging into github...")
ghUser = input("Username: ")
ghPw = getpass.getpass()

postData = {'commit':"Sign+in",'utf8':"%E2%9C%93",'authenticity_token':authenticity_token,'login':ghUser,'password':ghPw}

loginPost = session.post("https://github.com/session", postData)
print("Status: ", loginPost.status_code, loginPost.reason)
# print(r.text + "...")