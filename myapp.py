#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Need weibo.conf 
[var]
usrname =
passwd = 
'''
import urllib2
import sys
import re
import base64
import json
import logging
from urlparse import urlparse 
from Interface import WeiboInterface
from WeiboProcess import WeiboCMD

cmdlist = {
'','w','q','quit','h','help','l','f','m','u'}

class WeiboApi:
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
		except:
			print "error happend when read username and passwd from conf"
			sys.exit(1)
		self._logger = logging.getLogger('Weibosh.log')
		self._process = WeiboCMD(self._username, self._passwd)
	def testLog(self):
		interface = WeiboInterface(self._username, self._passwd)
		interface.seturl('statuses/friends_timeline')
		interface.callweibo()
		print self._username + " 已经成功登录"
	def process(self, line):
		if line not in cmdlist:
			print "您输入了[%s]非法命令，输入[h/help]寻求更多帮助!" %line
			return 0
		self._process.process(line)
	def log(self, logcontent):
		print 'log'

def main():
	weibo = WeiboApi()
	#weibo.testLog()
	print "欢迎使用微博命令行客户端 v 0.0.1，输入[h/help]寻求更多帮助!"
	while True:
		try:
			line = raw_input(weibo._username + ' @ ')
		except:
			print "按 q/quit 退出"
			continue
		weibo.process(line)
		

if __name__ == '__main__':
	main()
