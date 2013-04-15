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

import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:
	def hello(self, widget, data=None):
		print "Hello World"
	def delete_event(self, widget, event, data=None):
		print "delete event occurred"
		return False
	def destroy(self, widget, data=None):
		gtk.main_quit()
	
	def login(self, widget, data=None):
		if data == None:
			print "error!"
			self.destory()
		else:
			print data
	
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(100)
		
		# a new button for logon test
		
		self.button = gtk.Button("log on")
		self.button.connect("clicked", self.login, "123");
		self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
		
   		self.window.add(self.button)
		self.button.show()
		self.window.show()
	def main(self):
		gtk.main()
if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()
