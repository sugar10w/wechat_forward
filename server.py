#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, url_for
import hashlib
import time
import xml.etree.ElementTree as ET
import socket
import threading

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
userList=[]

@app.route('/hello')
def hello():
	return 'Hello World!'

@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		token = 'TOKEN'
		query = request.args
		echostr = query.get('echostr', '')
		return make_response(echostr)
	else:
		xml_recv = ET.fromstring(request.data)
		Content = xml_recv.find("Content").text
		
		sendToDM(Content)
		
		msg="";
		if len(userList)==0:
			msg="(暂时没有弹幕客户端开着...)"
		else:
			msg="弹幕已发送~~~"
		
		response = reply_res(xml_recv, msg)
		return response

def reply_res(xml_recv, msg):
	ToUserName = xml_recv.find("ToUserName").text
	FromUserName = xml_recv.find("FromUserName").text
	Content = xml_recv.find("Content").text
	reply = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag></xml>'''
	response = make_response( reply % (
		FromUserName,
		ToUserName,
		str(int(time.time())),
		msg ) )
	response.content_type = 'application/xml'
	return response

def sendToDM(str):
	print str
	for (s,a) in userList:
		try:
			#print "send to " + a[0] + "..."
			s.send(str)
			#print "done."
		except:
			userList.remove((sock,addr))

def tcplink(sock, addr):
	str=sock.recv(1024)
	if str != "asta2015":
		return
		
	userList.append((sock,addr));
	
	print "New connection from %s:%s" % (addr[0],addr[1]) 

	while True:
		try:
			data = sock.recv(1024)
		except:
			userList.remove((sock,addr))
			return 1

def startServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("", 12352))
	s.listen(5)
	print("Waiting for connection...")
	while True:
		sock, addr = s.accept()
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()

t = threading.Thread(target=startServer)
t.start()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 80)
