#! /usr/bin/python

# This is a simple TCP server, example taken from http://www.devshed.com/c/a/Python/Sockets-in-Python-Into-the-World-of-Python-Network-Programming/2/

from socket import *

#Then the constants that defines the host, port, buffer size and the address tuple to be used with bind().

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

#Then we create the server side socket and bind it to the host and the port. Then comes the max queue size to 2:

serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(2)

#Now, to make it listen for incoming requests continuously, place the accept() method in a while loop. This is not the most preferred mode. The preferred way will be discussed in the next section:
#Next, receive the data from the client and echo it back. This has to continue until the client doesnt send the null data or ctrl+c. To achieve this, use a while loop again and then close the connection when done.

while 1:
	print 'waiting for connection'
	clientsock, addr = serversock.accept()
	print 'connected from:', addr

	while 1:
		data = clientsock.recv(BUFSIZ)
		print "received: ", list(data)
		if not data: break
		clientsock.send(data)

	clientsock.close()
serversock.close()







