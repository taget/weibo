#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
        call weibo Uploade interface interface , then return a json string.
'''

from weibo import APIClient

import ConfigParser
import sys,time
import webbrowser

app_key = '35587412'
app_secret = '1b054a023d36fbacd3e26a5b723baf4d'
r_url = 'https://api.weibo.com/oauth2/default.html'

def main():
	client = APIClient(app_key, app_secret, r_url)
	
	url = client.get_authorize_url()
	print url
	webbrowser.open_new(url)
	code = raw_input()
	r = client.request_access_token(code)
	access_token = r.access_token  # access token，e.g., abc123xyz456
	expires_in = r.expires_in      # token expires in
	client.set_access_token(access_token, expires_in)
	print(client.statuses__public_timeline())

if __name__ == '__main__':
	main()
