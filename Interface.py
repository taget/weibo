#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	call weibo interface , then return a json string.
'''

import urllib2
import urllib
import sys
import re
import base64
from urlparse import urlparse 

def geturl(opt):
	theurl = 'http://api.weibo.com/2/statuses/'
	return theurl + opt + '.json?source=35587412'
class WeiboInterface():
	def __init__(self, username, passwd):
		self._username = username
		self._passwd = passwd
	def addopt(self, opt, val):
		print opt % val
	def callweibo(self, opt, data = None):
		theurl = geturl(opt)
		req=urllib2.Request(theurl)
		base64string = base64.encodestring(
					'%s:%s' % (self._username, self._passwd))[:-1] #注意哦，这里最后会自动添加一个\n
		authheader =  "Basic %s" % base64string
		req.add_header("Authorization", authheader)
		try:
			handle = urllib2.urlopen(req, data)
		except IOError, e:
			# here we shouldn't fail if the username/password is right
			print "It looks like the username or password is wrong."
			sys.exit(1)
		thepage = handle.read() 
		return thepage
	
