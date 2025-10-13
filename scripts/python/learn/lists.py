#!/usr/bin/python

""" 
Demonstrates lists in python
"""

"""
append(  	x)
    Add an item to the end of the list; equivalent to a[len(a):] = [x]. 

extend( 	L)
    Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L. 

insert( 	i, x)
    Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x). 

remove( 	x)
    Remove the first item from the list whose value is x. It is an error if there is no such item. 

pop( 	[i])
    Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. The item is also removed from the list. (The square brackets around the i in the method signature denote that the parameter is optional, not that you should type square brackets at that position. You will see this notation frequently in the Python Library Reference.) 

index( 	x)
    Return the index in the list of the first item whose value is x. It is an error if there is no such item. 

count( 	x)
    Return the number of times x appears in the list. 

sort( 	)
    Sort the items of the list, in place. 

reverse( 	)
    Reverse the elements of the list, in place. 

"""

mylist = [66.25, 333, 333, 1, 1234.5]

print "list is:", mylist

print "333 apears", mylist.count(333)," times", "66.25 apears ",mylist.count(66.25)," times", "x apears", mylist.count('x')," times", "\n"

print "insert -1 in position 2 than append 333"
mylist.insert(2, -1)
mylist.append(333)
print "the list: ", mylist
print "index 0f 333 ", mylist.index(333)

print "removing 333"
mylist.remove(333)
print "updated list: ", mylist, "\n"

print "reverse the list"
mylist.reverse()
print "updated list: ", mylist, "\n"

print "Sort list"
mylist.sort()
print "updated list: ", mylist, "\n"

"""
There are three built-in functions that are very useful when used with lists: filter(), map(), and reduce().

"filter(function, sequence)" returns a sequence consisting of those items from the sequence for which function(item) is true. If sequence is a string or tuple, the result will be of the same type; otherwise, it is always a list. For example, to compute some primes:
"""

def f(x): return x % 2 != 0 and x % 3 != 0

print "filter list (2,25) according to not divide by 2 and 3 ", filter(f, range(2, 25)), "\n"

"""
"map(function, sequence)" calls function(item) for each of the sequence's items and returns a list of the return values. For example, to compute some cubes:
"""

def cube(x): return x*x*x

print "map list (1, 11) to it's cubic values ", map(cube, range(1, 11))

"""
More than one sequence may be passed; the function must then have as many arguments as there are sequences and is called with the corresponding item from each sequence (or None if some sequence is shorter than another). For example:
"""
seq = range(8)
def add(x, y): return x+y

print "The function can have more then one parameter. for example, add has two parameters so map call is as follows: map(add, seq, seq)"
print "result is: ", map(add, seq, seq), "\n"

"""
"reduce(function, sequence)" returns a single value constructed by calling the binary function function on the first two items of the sequence, then on the result and the next item, and so on. For example, to compute the sum of the numbers 1 through 10:
"""
print "reduce example. use reduce to calculate the sum of a list"
def add(x,y): return x+y

print "calling: reduce(add, range(1, 11)). result: ",  reduce(add, range(1, 11))

"""
If there's only one item in the sequence, its value is returned; if the sequence is empty, an exception is raised.

A third argument can be passed to indicate the starting value. In this case the starting value is returned for an empty sequence, and the function is first applied to the starting value and the first sequence item, then to the result and the next item, and so on. For example,
"""

print "using reduce to define a sum method for lists."
def sum(seq):
	def add(x,y): return x+y
	return reduce(add, seq, 0)

print "calling the defined method - sum(range(1, 11)). result: ",  sum(range(1, 11))
print "calling the defined method for empty list - sum([]). result: ",  sum([])
print "this is just an example. there's a built in sum method. sum(seq). result: ", sum(range(1,11)), "\n"

"""List comprehensions provide a concise way to create lists without resorting to use of map(), filter() and/or lambda. The resulting list definition tends often to be clearer than lists built using those constructs. Each list comprehension consists of an expression followed by a for clause, then zero or more for or if clauses. The result will be a list resulting from evaluating the expression in the context of the for and if clauses which follow it. If the expression would evaluate to a tuple, it must be parenthesized.
"""
print "use for to create lists. (list comprehension)","\n"

print"for example use strip on list, freshfruit = ['  banana', '  loganberry ', 'passion fruit  ']"
freshfruit = ['  banana', '  loganberry ', 'passion fruit  ']
stripped = [fruit.strip() for fruit in freshfruit]
print "the stripped list: ", stripped, "\n"

print "multiply by 3 all elements of list: [2, 4, 6]"
vec = [2, 4, 6]
print "result: ", [3*x for x in vec]
print "multiply by 3 only elements larger than 3: ", [3*x for x in vec if x > 3]
print "multiply by 3 only elements smaller than 2: ", [3*x for x in vec if x < 2]
print "create a list of pairs [elem, elem**2]: ", [[x,x**2] for x in vec]
print "create a list of tupples (x, x**2): ", [(x, x**2) for x in vec],"\n"

print "its also possible to work on more than one list."
print "example. two lists: [2, 4, 6] and [4, 3, -9]"
vec1 = [2, 4, 6]
vec2 = [4, 3, -9]
print "create a list of all elements multiplied by all elements of the two lists: ", [x*y for x in vec1 for y in vec2]
print "create a list of all elements summed with all elements of the two lists: ", [x+y for x in vec1 for y in vec2]
print "vector multiplication: ", [vec1[i]*vec2[i] for i in range(len(vec1))], "\n"

"""
List comprehensions are much more flexible than map() and can be applied to complex expressions and nested functions:
"""

print "this example rounds a number to a different resolution from 1 to 6" 
print "number is 355/113.0. different reolutions of round: ", [str(round(355/113.0, i)) for i in range(1,6)] , "\n"

"""
There is a way to remove an item from a list given its index instead of its value: the del statement. Unlike the pop()) method which returns a value, the del keyword is a statement and can also be used to remove slices from a list (which we did earlier by assignment of an empty list to the slice). For example:
"""
print "use del to delete list slices and elements. uses indexes instead of values"
print "example array [-1, 1, 66.25, 333, 333, 1234.5]"
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
print "Delete element at index 0.", a, "\n"
del a[2:4]
print "Delete slice at index 2,4.", a, "\n"
print "del also be used to delete entire variables:"
del a
