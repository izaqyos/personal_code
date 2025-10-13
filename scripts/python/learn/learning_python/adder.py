#adder.py

def adder(a,b): return a+b

def adder2(*args): 
	print 'adder2'
	sum = args[0]
	for arg in args[1:]:
		sum = sum + arg
	return sum

def adder3(a=1,b=2,c=3): 
	print 'adder3'
	return a+b+c

def adder4(**args): 
	if type(args[args.keys()[0]]) == type(0):               # Integer?
	     sum = 0                               # Init to zero
	elif type(args[args.keys()[0]]) == type('0'):               # String
		sum=''
	else:                                      # else sequence:
	     sum = []                              # Use empty slice of arg1
	print 'adder4'
	for k in args.keys():
		sum = sum + args[k]
	return sum

def dict_cp(dict):
	return dict.copy()

def dict_add(dict1,dict2 ):
	return dict1.update(dict2).copy()

print adder('a','b')
print adder(range(4),['a','b'])
print adder(5.87,6.04)

print adder2('a','b', 'c')
print adder2(range(4))

print adder3(4,5,6)
#print adder3('a')
#print adder3(range(4))

print adder4(a=1, b=100, c=37651)
print adder4(a='1', b='100', c='37651')
print adder4(a=[1,2,3], b=range(10))

print dict_cp({'a':1,'b':2})
print dict_add({'a':1,'b':2}, {'a':2,'c':5})
