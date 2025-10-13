#!/usr/bin/python

"""
Demonstrates the concept of tuples in python
"""
"""
We saw that lists and strings have many common properties, such as indexing and slicing operations. They are two examples of sequence data types. Since Python is an evolving language, other sequence data types may be added. There is also another standard sequence data type: the tuple.

A tuple consists of a number of values separated by commas, for instance:
"""
t = 12345, 54321, 'hello!'
print "Tuples consists of a number of values separated by commas, for instance: ",t
print "And access first element (t[0]): ",t[0]
u = t, (1, 2, 3, 4, 5)
print "Tuples may be nested, for example u = t, (1, 2, 3, 4, 5): ", u

"""
As you see, on output tuples are always enclosed in parentheses, so that nested tuples are interpreted correctly; they may be input with or without surrounding parentheses, although often parentheses are necessary anyway (if the tuple is part of a larger expression).

Tuples have many uses. For example: (x, y) coordinate pairs, employee records from a database, etc. Tuples, like strings, are immutable: it is not possible to assign to the individual items of a tuple (you can simulate much of the same effect with slicing and concatenation, though). It is also possible to create tuples which contain mutable objects, such as lists.

A special problem is the construction of tuples containing 0 or 1 items: the syntax has some extra quirks to accommodate these. Empty tuples are constructed by an empty pair of parentheses; a tuple with one item is constructed by following a value with a comma (it is not sufficient to enclose a single value in parentheses). Ugly, but effective. For example:
"""
print "syntax for empty tuple,  empty = (). For one element tuple,  singleton = 'hello',"
empty = ()
singleton = 'hello',    # <-- note trailing comma
print "length of empty, ",len(empty)," length of singelton, ",len(singleton), "\n"

"""
The statement t = 12345, 54321, 'hello!' is an example of tuple packing: the values 12345, 54321 and 'hello!' are packed together in a tuple. The reverse operation is also possible:
"""

x, y, z = t
print "creating a tuple is also refered to as packing. The reverse operation is also possible. For example x, y, z = t. x,y,z values are: ",x,y,z,"\n"

"""
This is called, appropriately enough, sequence unpacking. Sequence unpacking requires the list of variables on the left to have the same number of elements as the length of the sequence. Note that multiple assignment is really just a combination of tuple packing and sequence unpacking!

There is a small bit of asymmetry here: packing multiple values always creates a tuple, and unpacking works for any sequence. 
"""

