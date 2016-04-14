# //pip install lxml cssselect
# //pip install Pillow

import lxml.html
from lxml.cssselect import CSSSelector

import requests
import json
import os
import getpass

# SETUP REQUEST SESSION --------------------------- #

session = requests.Session()

# LOGIN ------------------------------------- LOGIN #

#getting auth token
loginPage = session.get('https://github.com/login')
loginTree = lxml.html.fromstring(loginPage.text)
findAuth = CSSSelector('input[name="authenticity_token"]')

authenticity_token = findAuth(loginTree)[0].get('value')
# print (lxml.html.tostring(tree))
# print(authenticity_token)

# making post request with login data
# get user info from CL
url = "https://github.com/session"

print("logging into github...")
ghUser = input("Username: ")
ghPw = getpass.getpass()

postData = {
	'commit':"Sign+in",
	'utf8':"%E2%9C%93",
	'authenticity_token':authenticity_token,
	'login':ghUser,
	'password':ghPw
}

loginPost = session.post(url, postData)
print("Login status: ", loginPost.status_code, loginPost.reason)
# print(r.text + "...")

# UPLOAD ------------------------------------------ #

# GET REMOTE AUTH
url = "https://github.com/upload/policies/avatars"

# getting local auth token
settingsPage = session.get('https://github.com/settings/profile')
settingsTree = lxml.html.fromstring(settingsPage.text)
# get auth token
findAuth = CSSSelector('input[name="authenticity_token"]')

authenticity_token = findAuth(settingsTree)[0].get('value')
# get gh user-id (ownerid)
findId = CSSSelector('form[data-alambic-owner-id]')

ownerId = findId(settingsTree)[0].get('data-alambic-owner-id')
# print(ownerId)
# send photo meta to policies
postData = {
	'name':(None, "me.png"),
	'size':(None, os.path.getsize("../images/me.png")),
	'content_type':(None, "image/png"),
	'authenticity_token':(None, authenticity_token),
	'owner_type':(None, "User"),
	'owner_id':(None, ownerId)
}

setupPost = session.post(url, postData)

print("Setup status: ", setupPost.status_code, setupPost.reason)
# print(setupPost.text + "...")
json_data = json.loads(setupPost.text)
GitHub_Remote_Auth = json_data['header']["GitHub-Remote-Auth"]
print(GitHub_Remote_Auth)

# SEND OPTIONS

# SEND PHOTO

url = "https://uploads.github.com/storage/avatars"

headers = {
	'GitHub-Remote-Auth': GitHub_Remote_Auth
}

print (os.path.getsize("/home/adw/Dropbox/PROPIC.jpg"))
postData = {
	'authenticity_token':(None, authenticity_token),
	'owner_type':(None, "User"),
	'owner_id':(None, ownerId),
	'size':(None, os.path.getsize("../images/me.png")),
	'content_type':(None, "image/png"),
	'file':('me.png', open('../images/me.png', 'rb'),'image/png')
}

photoPost = session.post(url, postData, headers=headers)

print("Send status: ", photoPost.status_code, photoPost.reason)
print(photoPost.text + "...")

