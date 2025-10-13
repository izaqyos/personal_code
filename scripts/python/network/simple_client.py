#! /usr/bin/python

# This is a simple TCP client, example taken from http://www.devshed.com/c/a/Python/Sockets-in-Python-Into-the-World-of-Python-Network-Programming/2/
from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while 1:
	data = raw_input('> ')
	if not data: 
		break 
	tcpCliSock.send(data)
	data = tcpCliSock.recv(1024)
	if not data: 
		break 
	print data

tcpCliSock.close()
