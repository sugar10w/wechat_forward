#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, url_for
import hashlib
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)


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
		response = reply_res(xml_recv, "Hello World!")
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

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 80)
