#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testbottle.py
#  
#  Copyright 2013 lenovo <lenovo@N-QIAOLIYONG>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from bottle import route, get, post, request, run, static_file, error,template
import os
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

def run_command(cmd):
	rc = -1
	out = ''
	err = ''
	rc, out, err = exec_command(cmd)
	
	if rc == 0:
		return "".join(out.split());
	else:
		return 0

def check_login(name, password):
	if name == 'taget' and password == '123':
		return True
	else:
		return False

def call_weibo(name, passwd):
		interface = WeiboInterface(name, passwd)
		interface.seturl('statuses/friends_timeline')
		return interface.callweibo()
		
def get_save_path_for_category(category):
	return '/home/qiaoliyong/sda/code/weibo/'

@get('/login') # or @route('/login')
def login_form():
    return '''<p>欢迎使用微博客户端</p>
              <form method="POST" action="/login">
                用户名：<input name="name"     type="text" />
                密码：<input name="password" type="password" />
                <input type="submit" />
              </form>'''

@post('/login') # or @route('/login', method='POST')
def login_submit():
    name     = request.forms.get('name')
    password = request.forms.get('password')
    try:
        ret = call_weibo(name, password)
        msg_list = message_list(ret)
        msg = msg_list.get_message(0)
        usr = msg.msg_user()
        ret_msg = msg.msg_text()
        auth_usr = usr.get_user_name()
    except:
        return "error"    
    if len(ret) > 0:
        return template('<form><input type="submit" value="Refresh"/></form><b>{{user}} : {{msg}}</b>!', user= auth_usr, msg=ret_msg)
    else:	
        return '登录失败'

@get('/upload')
def do_login():
	return '''<form action="/upload" method="post" enctype="multipart/form-data">
  Category:      <input type="text" name="category" />
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
  </form>'''

      
@route('/upload', method='POST')
def do_login():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    print ext
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = get_save_path_for_category(category)
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/home/qiaoliyong/')

@get('/rhevhbuild')
def rhevhbuild():
	return '''<p>RHEVH Blue Build:</p>
              <form method="POST" action="/rhevhbuild">
              <p>RAV_LINK_ADDRESS:<input name="RAV_LINK_ADDRESS" type="text" /></p>
              <p>RAV_PACKAGE_NAME:<input name="RAV_PACKAGE_NAME" type="text" /></p>
              <p>EMULEX_LINK_ADDRESS:<input name="EMULEX_LINK_ADDRESS" type="text" /></p>
              <p>EMULEX_PACKAGE_NAME:<input name="MULEX_PACKAGE_NAME" type="text" /></p>
              <p>PA_SELINUX_POLICY_ADDRESS:<input name="PA_SELINUX_POLICY_ADDRESS" type="text" /></p>
              <p>PA_SELINUX_POLICY_NAME:<input name="PA_SELINUX_POLICY_NAME" type="text" /></p>
                <input type="submit" />
              </form>'''
@post('/rhevhbuild')
def do_build():
	rav_addr = request.forms.get('RAV_LINK_ADDRESS')
	rav_name = request.forms.get('RAV_PACKAGE_NAME')
	emu_addr = request.forms.get('EMULEX_LINK_ADDRESS')
	emu_name = request.forms.get('EMULEX_PACKAGE_NAME')
	pa_addr = request.forms.get('PA_SELINUX_POLICY_ADDRESS')
	pa_name = request.forms.get('PA_SELINUX_POLICY_NAME')
	
	
#$cmd = "RAV_LINK_ADDRESS=$RAV_LINK_ADDRESS RAV_PACKAGE_NAME=$RAV_PACKAGE_NAME EMULEX_LINK_ADDRESS=$EMULEX_LINK_ADDRESS EMULEX_PACKAGE_NAME=$EMULEX_PACKAGE_NAME SELINUX_LINK_ADDRESS=$SELINUX_POLICY_ADDRESS SELINUX_PACKAGE_NAME=$SELINUX_POLICY_NAME /home/git/bingbu/rhevh/pa-download-uncompress.sh";
#$cmd = "/home/git/bingbu/rhevh/a.sh $RAV_LINK_ADDRESS $RAV_PACKAGE_NAME $EMULEX_LINK_ADDRESS $EMULEX_PACKAGE_NAME $SELINUX_POLICY_ADDRESS SELINUX_POLICY_NAME ";
	cmdline = "RAV_LINK_ADDRESS=%s RAV_PACKAGE_NAME=%s EMULEX_LINK_ADDRESS=%s \
	 EMULEX_PACKAGE_NAME=%s SELINUX_LINK_ADDRESS=%s SELINUX_PACKAGE_NAME=%s \
	 /home/qiaoliyong/sda/test/sh/a.sh" \
	 % (rav_addr, rav_name, emu_addr, emu_name, pa_addr, pa_name)
   #cmd = "RAV_LINK_ADDRESS=$RAV_LINK_ADDRESS RAV_PACKAGE_NAME=$RAV_PACKAGE_NAME EMULEX_LINK_ADDRESS=$EMULEX_LINK_ADDRESS EMULEX_PACKAGE_NAME=$EMULEX_PACKAGE_NAME SELINUX_LINK_ADDRESS=$SELINUX_POLICY_ADDRESS SELINUX_PACKAGE_NAME=$SELINUX_POLICY_NAME /home/git/bingbu/rhevh/pa-download-uncompress.sh"
	return run_command(cmdline)
#$out = shell_exec($cmd);
	
	return template('<form><input type="submit" value="Refresh"/></form><b>{{addr}} : {{pkg_name}}</b>!', addr= cmdline, pkg_name=rav_name)
        
@error(404)
def error404(error):
    return 'Nothing here, sorry'    
    
def main():
	run(host='localhost', port=8080, debug=True)
	return 0

if __name__ == '__main__':
	main()



