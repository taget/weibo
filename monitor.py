#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
monitor my command in weibo, then run a shell command on the local host

'''
'''
Need weibo.conf 
[var]
usrname =
passwd = 
'''
import urllib2
import urllib
import sys
import re
import base64
import json
import logging
import time
from urlparse import urlparse 
from Interface import WeiboInterface
from WeiboProcess import WeiboCMD
from message_list import message_list
from message import message
from user import user

from util import *

def writetext(text, key="status"):
	data = urllib.urlencode({key:text})
	return data

class Monitor:
	def __init__(self):
		try:
			import ConfigParser
		except:
			print 'import ConfigParser error'
			sys.exit(1)
		confFile = 'weibo.conf'
		config = ConfigParser.ConfigParser()
		config.read(confFile)
		try:
			self._username = config.get('vars', 'username')
			self._passwd = config.get('vars', 'passwd')
			self._keyword = config.get('conf', 'keyword')
			self._cmd = config.get('conf', 'cmd')
		except:
			print "error happend when read conf"
			sys.exit(1)
		self._interface = WeiboInterface(self._username, self._passwd)
		self._logger = logging.getLogger('Monitor.log')
	def loop(self):
		self._interface.seturl('statuses/mentions')
		self._interface.addopt('count','2')
		ret = self._interface.callweibo()
		msg_list = message_list(ret)
		msg = msg_list.get_message(0)
		usr = msg.msg_user()
		ret_msg = msg.msg_text()
		cmd = ret_msg.find('echo')
	'''	
		if msg.msg_text().find(self._keyword):
			print "find!!"
			rc = -1
			out = ''
			err = ''
			rc, out, err = exec_command(self._cmd)
			if rc == 0:
				ret_msg = 'done ' + self._cmd
				data = writetext(ret_msg)
				try:
					self._interface.seturl('statuses/update')
					ret = self._interface.callweibo(data)
				except:
					print "wrong"
'''

def main():
	mon = Monitor()
	#weibo.testLog()
	while True:
		mon.loop()
		
		time.sleep(5)
		

if __name__ == '__main__':
	main()
