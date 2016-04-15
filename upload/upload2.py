# //pip install lxml cssselect
# //pip install Pillow

import lxml.html
from lxml.cssselect import CSSSelector

import requests
import json
import os
import getpass

# LOGIN ------------------------------------- LOGIN #
#input -- a request session
#returns -- a request response (loginPost)

def login(session):
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
	print("Login status: \t\t", loginPost.status_code, loginPost.reason)
	# print(r.text + "...")
	return loginPost

# UPLOAD ------------------------------------------ #
#input -- a request session
	   # -- a photo name
	   # -- a photo path
#returns -- a uploaded photo id	
def upload(session, photoName, photoPath):
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
		'name':(None, photoName),
		'size':(None, os.path.getsize(photoPath)),
		'content_type':(None, "image/png"),
		'authenticity_token':(None, authenticity_token),
		'owner_type':(None, "User"),
		'owner_id':(None, ownerId)
	}

	setupPost = session.post(url, postData)

	print("Upload setup status: \t\t", setupPost.status_code, setupPost.reason)
	# print(setupPost.text + "...")
	json_data = json.loads(setupPost.text)
	GitHub_Remote_Auth = json_data['header']["GitHub-Remote-Auth"]
	# print(GitHub_Remote_Auth)

	# SEND OPTIONS

	# SEND PHOTO

	url = "https://uploads.github.com/storage/avatars"

	headers = {
		'GitHub-Remote-Auth': GitHub_Remote_Auth
	}

	# print (os.path.getsize(photoPath))
	postData = {
		'authenticity_token':(None, authenticity_token),
		'owner_type':(None, "User"),
		'owner_id':(None, ownerId),
		'size':(None, str(os.path.getsize(photoPath))),
		'content_type':(None, "image/png"),
		'file':(photoName, open(photoPath, 'rb'),"image/png",{'Expires':'0'})
	}

	photoPost = session.post(url, files=postData, headers=headers)

	print("Upload send status: \t\t", photoPost.status_code, photoPost.reason)
	# print(photoPost.text + "...")

	json_data = json.loads(photoPost.text)
	photoId = json_data['id']
	# print(photoId)
	return photoId
	# TODO: deal with resizing on gh end

# CROP PHOTO -------------------------------------- $
#input -- a requests session
#	   -- a photoId
#returns -- nada breh for now TODO: figure this out
def crop(session, photoId):
	# get photo auth token
	url = "https://github.com/settings/avatars/" + str(photoId)
	cropPage = session.get(url)
	print("Crop info status: \t\t", cropPage.status_code, cropPage.reason)
	# print(cropPage.text)
	cropTree = lxml.html.fromstring(cropPage.text)
	findAuth = CSSSelector('input[name="authenticity_token"]')

	authenticity_token = findAuth(cropTree)[0].get('value')

	# send crop post
	postData = {
		'utf8':"%E2%9C%93",
		'authenticity_token':authenticity_token,
		'cropped_x':0,
		'cropped_y':10,
		'cropped_width':392,
		'cropped_height':392,
	}
	cropPost = session.post(url,postData)
	print("Crop post status: \t\t", cropPost.status_code, cropPost.reason)
	# print(cropPost.text)

# MAIN ------------------------------------------------------------------MAIN #

# INPUT PHOTO INFO -------------------------------- #

#TODO: auto gen this info
photoName = input("photo name: ")
photoPath = input("photo path: ")

# SETUP REQUEST SESSION --------------------------- #

session = requests.Session()

# start shit up

loginPost = login(session)
photoId = upload(session,photoName,photoPath)
crop(session, photoId)
