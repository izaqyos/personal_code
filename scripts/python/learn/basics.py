#!/usr/bin/python

delim = "\n*********************************************************\n"

print delim, "control structures"
print "if else"
x = int(raw_input("Please enter an integer: "))
if x < 0:
	x = 0
	print 'Negative changed to zero'
elif x == 0:
	print 'Zero'
elif x == 1:
	print 'Single'
else:
	print 'More'

print delim, "for, (print length of some strings)"
a = ['cat', 'window', 'defenestrate']
print "strings: ", a
for x in a:
	print x, len(x)

print delim, "compute permutation, while loop"

# in interactive shell:
#>>> x = 256 
#>>> c = 1
#>>> while ( x > 1) :
#...     c = x*c
#...     x = x-1
#... 
#>>> print c
# and to compute log_10
#  math.log(c,10)
x = 5
c = 1
while (x > 1):
	c  = c*x
	x = x-1

print c

print delim, "the range() function"
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
	print i, a[i]


#The pass statement does nothing. It can be used when a statement is required syntactically but the program requires no action. For example:
#
#>>> while True:
#...       pass # Busy-wait for keyboard interrupt
#...


print delim, "Function definition. Fibonacci 2000"

def fib(n):    # write Fibonacci series up to n
	"""Print a Fibonacci series up to n."""
	a, b = 0, 1
	while b < n:
		print b,
		a, b = b, a+b

def fib2(n): #return the list of Fibonnacy numbers up to n.
	"""return the list of Fibonnacy numbers up to n."""
	a,b = 0,1
	res = []
	while b<n:
		res.append(b)
		a,b = b, a+b
	return res

# Now call the function we just defined:
fib(2000)
print "\nfib # up to 100", fib2(100)
