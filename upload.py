#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
        call weibo Uploade interface interface weibo1 , then return a json string.
'''

from weibo1 import OAuthToken
from weibo1 import APIClient

import ConfigParser
import sys,time
import urllib

app_key = u'35587412'
app_secret = u'1b054a023d36fbacd3e26a5b723baf4d'
r_url = 'https://api.weibo.com/oauth2/default.html'

uname = '月亮jimmy'
passw = 'jimmy1985'

def main():
	client = APIClient(app_key=app_key, app_secret=app_secret)

	reqToken = client.get_request_token()	
	auth_url =  client.get_authorize_url(reqToken)
	post_data = urllib.urlencode({  
            "action": "submit",
            "forcelogin": "",  
            "from": "",  
            "oauth_callback" : "http://api.weibo.com/oauth2/default.html",
            "oauth_token" : reqToken.oauth_token,
            "passwd" : passw,
            "regCallback": "",  
            "ssoDoor": "",  
            "userId" : uname,  
            "vdCheckflag" : 1,  
            "vsnval":""  
        })  
  

if __name__ == '__main__':
	main()
