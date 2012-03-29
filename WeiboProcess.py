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
import WeiboUtil
from urlparse import urlparse 
from Interface import WeiboInterface
from Json import JsonProcessor

def Weibohelp():
	print "	h : 帮助"
	print "	f : 获取当前登录用户及其所关注用户的最新微博"
	print "	l : 获得关注列表"
	print "	w : 写一条新微博"
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
			'''
			查看当前关注用户的最新20条
			'''
			print '查看当前关注用户的最新20条...'
			try:
				texts = self._jsonprocessor.Parse_json_2_list(self._interface.callweibo('friends_timeline'))
			except:
				print "拉取失败，请重试"
				return
			i = 1 
			print '[序号]--[作者]--[内容]----------------------------------------------------'
			for text in texts:
				retweete = self.gettextfromlist(text, 'retweeted_status')
				if retweete == False:
					sys.stdout.write("【原创】")
					print "[%d] : [%s] %s" %(i, self.gettextfromlist(text, 'user').get('name'),
					self.gettextfromlist(text, 'text'))
				else:
					print "[%d] : [%s] %s" %(i, self.gettextfromlist(text, 'user').get('name'),
					self.gettextfromlist(text, 'text'))
					print "--->>>转发原文内容为<<<---"
					print retweete['text'] 
				i = i + 1
		if line == 's':
			print "s!"
		if line == 'l':
			print "l!"
		if line == 'w':
			try:
				line = raw_input("请输入要发表的内容（不超过140字,ctrl + d 取消发表）")
			except:
				print "取消发表"
				return
			#data = self.dumpjson(line)
			data = self.writetext(line)
			try:
				ret = self._interface.callweibo('update',data)
			except:
				print "发表失败"
			print "发表成功 ： " + self.gettextfromjson(ret, 'created_at')
			#print ret
			
	def  print_format(*line):
		""" Function doc """
		print line

