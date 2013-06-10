#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
process command line 
'''
import urllib2
import urllib
import sys
import re
import base64
import logging
from urlparse import urlparse 
from Interface import WeiboInterface
from Json import JsonProcessor
from friends import friends

reload(sys)
sys.setdefaultencoding('utf8')

def Weibohelp():
	print "	h : 帮助"
	print "	f : 获取当前登录用户及其所关注用户的最新微博"
	print "	l : 获得关注列表"
	print "	w : 写一条新微博"
	print "	m : 查看@我的微博"
	print "	u : 查看用户信息"
	print "	q : 退出微博客户端"

class WeiboCMD:
	def  __init__(self, username, passwd):
		self._interface = WeiboInterface(username,passwd)
		self._jsonprocessor = JsonProcessor()
	def gettextfromjson(self, text, content='text'):
		return self._jsonprocessor.Parse_get_text_from_json(text, content)
	def gettextfromlist(self, text, content='text'):
		return self._jsonprocessor.Parse_get_text_from_list(text, content)
	def writetext(self, text, key="status"):
		data = urllib.urlencode({key:text})
		return data
	def process(self, line):
		if line == 'q' or line == 'quit':
			print "感谢使用!"
			sys.exit(1)
		if line == 'h' or line == 'help':
			Weibohelp()
		if line == 'f':
			f = friends(self._interface, 'statuses/friends_timeline')
			f.run()
		if line == 's':
			print "s!"
		if line == 'm':
			f = friends(self._interface, 'statuses/mentions')
			f.run()
		if line == 'w':
			try:
				line = raw_input("请输入要发表的内容（不超过140字,ctrl + d 取消发表）")
			except:
				print "取消发表"
				return
			#data = self.dumpjson(line)
			data = self.writetext(line)
			print data
			try:
				self._interface.seturl('statuses/update')
				ret = self._interface.callweibo(data)
			except:
				print "发表失败"
			print "发表成功 ： " + self.gettextfromjson(ret, 'created_at')
			#print ret
			
	def  print_format(*line):
		""" Function doc """
		print line

