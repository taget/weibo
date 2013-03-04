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
import unicodedata
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
		except:
			print "error happend when read conf"
			sys.exit(1)

		self._interface = WeiboInterface(self._username, self._passwd)
		self._logger = logging.getLogger()

		hdlr = logging.FileHandler('Monitor.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		self._logger.addHandler(hdlr)
		self._logger.setLevel(logging.NOTSET)

		self._lastmsg = ''
		self._sleep_time = 10
		self._run = False

	def info(self, msg):
		self._logger.info(msg)

	def error(self, msg):
		self._logger.error(msg)

	def run_command(self, cmd):
		print "ready to run shell command: " + cmd
		self.info("ready to run shell command: " + cmd)
		rc = -1
		out = ''
		err = ''
		rc, out, err = exec_command(cmd)
		if rc == 0:
			return "".join(out.split());
		else:
			return 0

	def parse_keyword(self, msg):
		return msg[7:11] # find exec

	def parse_cmd(self, msg): # find shell command
		return msg[12:]

	def run(self):
		while True:
			self.loop()
			time.sleep(self._sleep_time)

	def loop(self):
		self._interface.seturl('statuses/mentions')
		self._interface.addopt('count','2')
		ret = self._interface.callweibo()
		msg_list = message_list(ret)
		msg = msg_list.get_message(0)
		usr = msg.msg_user()
		ret_msg = msg.msg_text()
		
		if self._lastmsg != ret_msg:
			self._lastmsg = ret_msg
			self._run = True
		else:
			print "zz..."
			self._run = False
		
		key_word = self.parse_keyword(ret_msg)
		
		if self._run == True and key_word == self._keyword:
			cmd = self.parse_cmd(ret_msg)
			res = self.run_command(cmd)

			if res != 0:
				ret = 'done result is:'+ res
				data = writetext(ret)
				print data
				try:
					self._interface.seturl('statuses/update')
					self._interface.callweibo(data)
					print 'run successful , write back to weibo'
					self.info("run successful , write back to weibo")
				except:
					print "wrong"
					self.error("return msg to weibo error")
			else:
				# run failed
				self._lastmsg = ''

def main():
	mon = Monitor()
	mon.run()

		

if __name__ == '__main__':
	main()
