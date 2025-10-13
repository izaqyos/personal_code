#!/usr/bin/python

"""
Python also includes a data type for sets. A set is an unordered collection with no duplicate elements. Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union, intersection, difference, and symmetric difference.

Here is a brief demonstration:
"""

print "demonstration of sets in python.\n"

basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
print "We want to create a set from the list basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']"
fruit = set(basket)               # create a set without duplicates
print "The set is(no duplicates): ", fruit
print "Test membership, is 'orange' in set? ",  'orange' in fruit 
print "Test membership, is 'ananas' in set? ",  'ananas' in fruit , "\n"

print "Is is possible to create a set from string letters."
a = set('abracadabra')
b = set('alacazam')
print "Lets define two sets:  a = set('abracadabra') and b = set('alacazam')\n",a, b, "\n"
print "A-B: ",a-b,"\nA U B: ",a|b,"\nA intersection B: ",a&b,"\nA symmetric difference B: ",a^b, "\n" 
