#!/usr/bin/python

print "When looping through dictionaries, the key and corresponding value can be retrieved at the same time using the iteritems() method."

knights = {'gallahad': 'the pure', 'robin': 'the brave'}
print "For example an iteration over the following dictionary.  knights = {'gallahad': 'the pure', 'robin': 'the brave'}"
for k, v in knights.iteritems():
	print k, v


print "\nWhen looping through a sequence, the position index and corresponding value can be retrieved at the same time using the enumerate() function."

print "for example the iteration: for i, v in enumerate(['tic', 'tac', 'toe']): ...     print i, v:"
 
for i, v in enumerate(['tic', 'tac', 'toe']):
	print i, v


print "\nTo loop over two or more sequences at the same time, the entries can be paired with the zip() function."
print "Consider the two seqs. questions = ['name', 'quest', 'favorite color'], answers = ['lancelot', 'the holy grail', 'blue']"
 
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']

print "Iterating as follows:  for q, a in zip(questions, answers): ...     print 'What is your %s?  It is %s.' % (q, a):\n "
for q, a in zip(questions, answers):
	print 'What is your %s?  It is %s.' % (q, a)


"""
To loop over a sequence in reverse, first specify the sequence in a forward direction and then call the reversed() function.
"""

print "\nuse reveresed() to loop over a sequence in reverse."
print "For example reversed(xrange(1,10,2)):" 
for i in reversed(xrange(1,10,2)):
	print i


"""
To loop over a sequence in sorted order, use the sorted() function which returns a new sorted list while leaving the source unaltered.
"""

print "\nuse sorted() to iterate over sorted sequence"
print " for example sort loop over basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']:"

basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
for f in sorted(set(basket)):
	print f

