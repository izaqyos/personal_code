#!/usr/local/bin/python
rem=[]

num=input('plz enter number ')
print('calculating binary of: ',num)

while num>0:
	#num,remider = (num/2, num%2)
	num,remider = divmod(num,2)
	print('num/2 ',num,' num%2', remider)
	rem.append(remider)

print 'binary: '
#rem.reverse()
rem=rem[::-1]
print rem
#for i in rem.reverse():
	#print i


