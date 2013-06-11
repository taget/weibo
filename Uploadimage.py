#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
        call weibo Uploade interface interface , then return a json string.
'''

from weibo import APIClient

import ConfigParser
import sys,time

app_key = '35587412'
app_secret = '1b054a023d36fbacd3e26a5b723baf4d'
r_url = 'https://api.weibo.com/oauth2/default.html'

def main():
	client = APIClient(app_key, app_secret, r_url)
	
	url = client.get_authorize_url()
	print url
	code = raw_input("Input code:")
	print code
	r = client.request_access_token(code)
	client.set_access_token(r.access_token, r.expires_in)
	
	print(client.upload.statuses__upload(status='uploaded at  '\
		+ str(time.time()), pic=open('1.jpg', 'rb')))

if __name__ == '__main__':
	main()
