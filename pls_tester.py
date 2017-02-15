#!/usr/bin/python

import hashlib
import time
import base64
import re
import urllib2
import sys
import os
from datetime import datetime  
from datetime import timedelta 
import time
import getopt
import requests
from oauth2client.service_account import ServiceAccountCredentials
import msvcrt
import json




COMMANDS = ['to do']
#PROD settings
PLS_PROD_ROOT = 'https://admin-dot-mq-media-cms-prod.appspot.com/'
PLS_KEYFILE_PROD = 'pls_media_cms_keyfile_prod.json'
#DEV settings
PLS_DEV_ROOT = 'https://admin-dot-mq-media-cms-dev.appspot.com/'
PLS_KEYFILE_DEV = 'pls_media_cms_keyfile_dev.json'


PLS_PATH = 'api/mtv1/'

def make_url(path, query_params = None):
	url = ROOT_URL + path	
	if query_params != None and query_params != '':
		url = url  + '?' + query_params
	return url



def ExecuteAccCheck(command, salt, installation_id, transport_token):
	executeCommand(command, salt, installation_id, transport_token, 'post')
	
def ExecuteGetChart(command, salt, installation_id, transport_token):
	executeCommand(command, salt, installation_id, transport_token, 'get', 'WIDTHXHEIGHT', '480x800')

def ExecuteContext(command, salt, installation_id, transport_token):
	executeCommand(command, salt, installation_id, transport_token, 'get')
	

def main(argv):

	
	

	if 1 == 0: #use PROD
		print 'are you sure you want to run commands on PLS PROD? Press Y to continue'
		c = msvcrt.getch()
		if c == 'y' or c == 'Y':
			root = PLS_PROD_ROOT
			keyfile = PLS_KEYFILE_PROD
		else:
			sys.exit(2)
	else:
		#DEV
		root = PLS_DEV_ROOT
		keyfile = PLS_KEYFILE_DEV


	token = generateOAuthToken(keyfile)




	#GET playlist feeds
	#executeCommand(token, 'get', root, PLS_PATH, 'playlistFeeds')
	
	if 1 == 0:
		#GET PlaylistFeedTasteProfiles	
		executeCommand(token, 'get', root, PLS_PATH, 'tasteProfiler/playlistFeedTasteProfiles')

	if 1 == 1:
		#POST PlaylistFeedTasteProfiles
		with open('post_playlistFeedTasteProfiles.json') as json_data:
			js = json.load(json_data)
		executeCommand(token, 'put', root, PLS_PATH, 'tasteProfiler/playlistFeedTasteProfiles', payload = json.dumps(js,indent = 2, sort_keys=True, separators=(',', ': ')).encode('utf8'))

	return



	


def print_options_manual():
	print 'pls_tester.py'
	print '      E.g. pls_tester.py'
	print '      Supported commands are ' + str(COMMANDS)

def generateOAuthToken(key_file):

	#salt value is written in my MQ Useful Info

	scopes = ['https://www.googleapis.com/auth/userinfo.email']

	print 'generating oauth token'
	credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scopes)
	#http = credentials.authorize(httplib2.Http())
	print credentials.get_access_token().access_token
	return credentials.get_access_token().access_token


def executeCommand(oauth_token, method, root, path, command, customParamKey = None, payload = None):

	if oauth_token == None or oauth_token == '':
	    print 'missing oauth_token'
	    print_options_manual()
	    sys.exit(2)


	url = root + path + command

	headers = {"Authorization" : 'Bearer ' + oauth_token, 'Content-Type' : 'application/json'}
	#urlparams = {'USER_NAME':installation_id,'USER_TOKEN':secureToken, 'TIMESTAMP':timestamp}
	urlparams = {}
	if customParamKey != None:
		urlparams[customParamKey] = customParamVal
	if method == 'post':
 		if payload == None:
 			r = requests.post(url, headers = headers, params = urlparams)
 		else:
 			r = requests.post(url, headers = headers, params = urlparams, data = payload)
 	elif method == 'put':
 		if payload == None:
 			r = requests.put(url, headers = headers, params = urlparams)
 		else:
 			r = requests.put(url, headers = headers, params = urlparams, data = payload)
 	else:
 		r = requests.get(url, headers = headers, params = urlparams)
 	print r.url
 	print r.status_code
 	try:
		js = r.json()
		print js.dumps(js,indent = 2, sort_keys=True, separators=(',', ': ')).encode('utf8')
 	except Exception, error:
 		print r.text.encode('utf8')

if __name__ == "__main__":
   main(sys.argv[1:])