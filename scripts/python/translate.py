#!/usr/bin/python

from sys import *

if len(argv) != 2:
	print "usage: translate  <string> "
else:
	str = argv[1]
	new_str = ""
	print "Translating string ",str

#my long way :)
	for c in str:
		if ord('a') <= ord(c) and ord(c) <= ord ('z'):
			#print "char is ",c, "ord is ",ord(c), "normalized ord ", ((ord(c))-ord('a')), "trans ord is ",(((ord(c)+2)-ord('a'))%26 +ord('a')),"Tran char ",chr(((ord(c)+2)-ord('a'))%25 +ord('a'))
			new_str += chr(((ord(c)+2)-ord('a'))%26 +ord('a') )
			#new_str += chr((ord(c)+2))
		else:
			new_str += c
	print new_str

#Solution
# i hope you didnt translate it by hand. thats what computers are for. doing it in by hand is inefficient and that's why this text is so long. using string.maketrans() is recommended. now apply on the url

