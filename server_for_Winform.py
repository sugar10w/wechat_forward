#-*- coding: UTF-8 -*-

import socket
import threading

import sys
reload(sys)
sys.setdefaultencoding('utf8')

userList=[]

def sendToAll(str):
	for (s,a) in userList:
		try:
			s.send("现在如此")
		except:
			userList.remove((sock,addr))
	print str

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

while True:
	s = raw_input()
	sendToAll(s)