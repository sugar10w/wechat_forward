#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import socket
import threading

import sys
reload(sys)
sys.setdefaultencoding('utf8')


clientList=[]
userNameList=[]
userNameStatus=[]


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

def startServer_Client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 12352))
    s.listen(5)
    print("Waiting for connection...")
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

def startServer_Web():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 45102))
    s.listen(5)
    print("Waiting for connection...")
    while True:
        sock, addr = s.accept()
        try:
            str = sock.recv(1024);
            print str
            sendToDM(str);
        except:
            print '[warning] web error occurred in startServer_Web'
        

t = threading.Thread(target=startServer_Client)
t.start()

startServer_Web()
