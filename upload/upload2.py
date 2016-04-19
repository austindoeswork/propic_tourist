# //pip install lxml cssselect
# //pip install Pillow

import lxml.html
from lxml.cssselect import CSSSelector

from PIL import Image

import requests
import json
import os
import getpass

# LOGIN ------------------------------------- LOGIN #
#input -- a request session
#	   -- a github username and password 
#returns -- a request response (loginPost)

def login(session, ghUser, ghPw):
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

	postData = {
		'commit':"Sign+in",
		'utf8':"%E2%9C%93",
		'authenticity_token':authenticity_token,
		'login':ghUser,
		'password':ghPw
	}

	loginPost = session.post(url, postData)
	
	return loginPost

# UPLOAD ------------------------------------------ #
#input -- a request session
#	   -- a photo name
# 	   -- a photo path
#	   -- a photo type
#returns -- a post response with photo metadata	(photoPost)
def upload(session, photoName, photoPath, photoType):
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
		'content_type':(None, photoType),
		'authenticity_token':(None, authenticity_token),
		'owner_type':(None, "User"),
		'owner_id':(None, ownerId)
	}

	setupPost = session.post(url, postData)

	print("upload setup status: ", setupPost.status_code, setupPost.reason)
	# print(setupPost.text + "...")

	jsonData = json.loads(setupPost.text)
	GitHub_Remote_Auth = jsonData['header']["GitHub-Remote-Auth"]
	
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
		'content_type':(None, photoType),
		'file':(photoName, open(photoPath, 'rb'),photoType,{'Expires':'0'})
	}

	photoPost = session.post(url, files=postData, headers=headers)

	# print("Upload send status: \t\t", photoPost.status_code, photoPost.reason)
	# print(photoPost.text + "...")

	return photoPost 

# CROP PHOTO -------------------------------------- $
#input -- a requests session
#	   -- a photoId
#returns -- cropPost
def crop(session, photoId, photoWidth, photoHeight):
	# get photo auth token
	url = "https://github.com/settings/avatars/" + str(photoId)
	cropPage = session.get(url)
	print("crop setup status: ", cropPage.status_code, cropPage.reason)
	# print(cropPage.text)
	cropTree = lxml.html.fromstring(cropPage.text)
	findAuth = CSSSelector('input[name="authenticity_token"]')

	authenticity_token = findAuth(cropTree)[0].get('value')

	# send crop post
	postData = {
		'utf8':"%E2%9C%93",
		'authenticity_token':authenticity_token,
		'cropped_x':0,
		'cropped_y':0,
		'cropped_width':photoWidth, #DEFUALT TO FULL SIZE
		'cropped_height':photoHeight,
	}

	cropPost = session.post(url,postData)
	return cropPost
	# print("Crop post status: \t\t", cropPost.status_code, cropPost.reason)
	# print(cropPost.text)


# HELPERS ------------------------------------------------------------------- #

# PRINT RESPONSE STATUS --------------------------- #
def print_status(name,res):
	print(name, " status: ", res.status_code, res.reason)


# INPUT PHOTO INFO -------------------------------- #
def handle_pic(photoName, photoPath):
	photoSize = os.path.getsize(photoPath)

	im = Image.open(photoPath)
	photoWidth, photoHeight = im.size
	format = im.format
	photoType = "image/" + format.lower()

	return photoSize,photoWidth,photoHeight,photoType

def handle_photoPost(photoPost):
	jsonData = json.loads(photoPost.text)
	photoId = jsonData['id']
	ghDefaultDimensions = jsonData['cropped_dimensions']
	photoWidth = jsonData['width']
	photoHeight = jsonData['height']
	return photoId, ghDefaultDimensions, photoWidth, photoHeight


# MAIN ------------------------------------------------------------------MAIN #

def main():

	# SETUP REQUEST SESSION --------------------------- #

	session = requests.Session()

	# start shit up

	photoName = input("photo name: ")
	photoPath = input("photo path: ")

	photoSize,photoWidth,photoHeight,photoType = handle_pic(photoName, photoPath)

	print("logging into github...")
	ghUser = input("Username: ")
	ghPw = getpass.getpass()

	#TODO: add proper logging of this crap
	
	loginPost = login(session, ghUser, ghPw) # LOGIN 
	print_status("LOGIN", loginPost)

	photoPost = upload(session,photoName,photoPath, photoType) # UPLOAD PHOTO
	print_status("UPLOAD", photoPost)

	photoId,_,_,_ = handle_photoPost(photoPost) # get photoId to crop
	
	cropPost = crop(session, photoId, photoWidth, photoHeight) # CROP PHOTO
	print_status("CROP", cropPost)

	print ("be patient dude it might take like 20 seconds...")


if __name__ == "__main__":
    main()