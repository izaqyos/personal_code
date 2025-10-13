#!/usr/bin/python

"""
Another useful data type built into Python is the dictionary. Dictionaries are sometimes found in other languages as ``associative memories'' or ``associative arrays''. Unlike sequences, which are indexed by a range of numbers, dictionaries are indexed by keys, which can be any immutable type; strings and numbers can always be keys. Tuples can be used as keys if they contain only strings, numbers, or tuples; if a tuple contains any mutable object either directly or indirectly, it cannot be used as a key. You can't use lists as keys, since lists can be modified in place using methods like append() and extend() or modified with slice and indexed assignments.

It is best to think of a dictionary as an unordered set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.

The main operations on a dictionary are storing a value with some key and extracting the value given the key. It is also possible to delete a key:value pair with del. If you store using a key that is already in use, the old value associated with that key is forgotten. It is an error to extract a value using a non-existent key.

The keys() method of a dictionary object returns a list of all the keys used in the dictionary, in arbitrary order (if you want it sorted, just apply the sort() method to the list of keys). To check whether a single key is in the dictionary, either use the dictionary's has_key() method or the in keyword.

Here is a small example using a dictionary:
"""

print "This is a brief demonstration of using dictionaries in Python\n"
tel = {'jack': 4098, 'sape': 4139}
print "Phone book dictionary. init as tel = {'jack': 4098, 'sape': 4139} : ",tel
tel['guido'] = 4127
print " add a key:value pair, tel['guido'] = 4127 : ", tel

print "Acess via dict[key] (as in tel['jack']). see: ", tel['jack']
del tel['sape']
print "Delete entry via del dict[key]. as in del tel['sape']. dictionary: ",tel 
tel['irv'] = 4127
print "Added 'irv':4127. get keys via dict.keys() method: ", tel.keys()

print "determine whether a key:value exists via has_key(). example, tel.has_key('guido'): ", tel.has_key('guido')
True
print "determine whether a key:value exists via key in dict. example, 'guido' in tel: ", 'guido' in tel

"""
The dict() constructor builds dictionaries directly from lists of key-value pairs stored as tuples. When the pairs form a pattern, list comprehensions can compactly specify the key-value list.
"""

print "It is possible to use list comprehensions to initialize a dictionary via the dict() CTOR."
quad = dict([(x, x**2) for x in (2, 4, 6)])     # use a list comprehension

print "Consider the dictionary created by the following list comprehension:  quad = dict([(x, x**2) for x in (2, 4, 6)]) ", quad

"""
Later in the tutorial, we will learn about Generator Expressions which are even better suited for the task of supplying key-values pairs to the dict() constructor.

When the keys are simple strings, it is sometimes easier to specify pairs using keyword arguments:
"""

tel1 = dict(sape=4139, guido=4127, jack=4098)
print "When the keys are simple strings, it is sometimes easier to specify pairs using keyword arguments such as, dict(sape=4139, guido=4127, jack=4098): ", tel1
