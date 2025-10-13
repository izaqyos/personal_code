#!/usr/bin/python

"""
Practice IO chapter of Python tutorial.

one question remains, of course: how do you convert values to strings? Luckily, Python has ways to convert any value to a string: pass it to the repr() or str() functions. Reverse quotes (``) are equivalent to repr(), but they are no longer used in modern Python code and will likely not be in future versions of the language.

>>> s = 'Hello, world.'
>>> str(s)
'Hello, world.'
>>> repr(s)
"'Hello, world.'"
>>> str(0.1)
'0.1'
>>> repr(0.1)
'0.10000000000000001'
>>> x = 10 * 3.25
>>> y = 200 * 200
>>> s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
>>> print s
The value of x is 32.5, and y is 40000...
>>> # The repr() of a string adds string quotes and backslashes:
... hello = 'hello, world\n'
>>> hellos = repr(hello)
>>> print hellos
'hello, world\n'
>>> # The argument to repr() may be any Python object:
... repr((x, y, ('spam', 'eggs')))
"(32.5, 40000, ('spam', 'eggs'))"
>>> # reverse quotes are convenient in interactive sessions:
... `x, y, ('spam', 'eggs')`
"(32.5, 40000, ('spam', 'eggs'))"
"""

print "use repr() or str() to convert values of any type to string."
print "str(134.12) is: ",str(134.12)," repr(134.12) is: ", repr(134.12),"\n"

print "use + for string concatanation."
x = 10 * 3.25
y = 200 * 200
s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
print "x = 10 * 3.25 and y = 200 * 200 and s is a concatenated string that contains them:\n",s

print "Formatting can be done in two ways. Either using repr().rjust(n) or using print %nd"
print "Example of writing a cube table with repr().rjust(n)"
for x in range(1, 11):
	print repr(x).rjust(2), repr(x*x).rjust(3),
# Note trailing comma on previous line
	print repr(x*x*x).rjust(4)


print "Example of writing a cube table with print %"
for x in range(1,11):
	print '%2d %3d %4d' % (x, x*x, x*x*x)


print "\nThe method, zfill() pads a numeric string on the left with zeros. It understands about plus and minus signs"

print "\'12\'.zfill(5): ", '12'.zfill(5)
print "\'-3.14\'.zfill(7): ", '-3.14'.zfill(7)
print "\'3.14159265359\'.zfill(5): ", '3.14159265359'.zfill(5)


print "\nIf there is more than one format in the string, you need to pass a tuple as right operand, as in this example"
print "table = {\'Sjoerd\': 4127, \'Jack\': 4098, \'Dcab\': 7678}, print with fields of length 10"

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
	print '%-10s ==> %10d' % (name, phone)

print "\nIf you have a really long format string that you don't want to split up, it would be nice if you could reference the variables to be formatted by name instead of by position. This can be done by using form %(name)format, as shown here:"

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
print 'Jack: %(Jack)d; Sjoerd: %(Sjoerd)d; Dcab: %(Dcab)d' % table

print "This is particularly useful in combination with the new built-in vars() function, which returns a dictionary containing all local variables. "
