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
clientList=[]
userNameList=[]
userNameStatus=[]
MAXSTATUS=10

def ModifyUserStatus(UserName,Content):
	if UserName in userNameList:
		i = userNameList.index(UserName)
		if userNameStatus[i]<=MAXSTATUS:
			userNameStatus[i]+=1
	else:
		userNameList.append(UserName)
		userNameStatus.append(1)

def GetUserStatus(UserName):
	if UserName in userNameList:
		i=0
		i = userNameList.index(UserName)
		return userNameStatus[i]
	else:
		ModifyUserStatus(UserName," ")
		return 0
		
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
		FromUserName = xml_recv.find("FromUserName").text
		
		msg="";
		if len(clientList)==0:
			msg="(暂时没有弹幕客户端开着...)"
		else:
			cnt=0
			if Content=="撒花":
				ModifyUserStatus(FromUserName,Content)
				cnt=GetUserStatus(FromUserName)
				print "cnt="+str(cnt)
				if cnt<=MAXSTATUS:
					sendToDM(Content)
					msg="撒花成功！！您还有"+str(MAXSTATUS-cnt)+"次撒花机会~~~"
					print msg
				else:
					msg="啊哦，您的撒花机会已经用光啦~~~"
			else:
				sendToDM(Content)
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
	for (s,a) in clientList:
		try:
			#print "send to " + a[0] + "..."
			s.send(str)
			#print "done."
		except:
			clientList.remove((sock,addr))

def tcplink(sock, addr):
	str=sock.recv(1024)
	if str != "asta2015":
		return
		
	clientList.append((sock,addr));
	
	print "New connection from %s:%s" % (addr[0],addr[1]) 

	while True:
		try:
			data = sock.recv(1024)
		except:
			clientList.remove((sock,addr))
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
