#!/usr/bin/python

delim = "\n*********************************************************\n"

def ask_user(prompt,  retries=3,  complaint = 'Please choose Yes or No'):


	while True:
        	ok = raw_input(prompt)
        	if ok in ('y', 'ye', 'yes'): return True
        	if ok in ('n', 'no', 'nop', 'nope'): return False
        	retries = retries -1
        	if retries < 0 : raise IOError, 'refusing user'
        	print complaint

print delim, "default values for arguments example"
ask_user("Elegir una respuesta, yes o no por favor\n")

#Important warning: The default value is evaluated only once.
#This makes a difference when the default is a mutable object such as a list, dictionary, or instances of most classes.
#For example, the following function accumulates the arguments passed to it on subsequent calls:

def f(a, L=[]):
    L.append(a)
    return L

print f(1)
print f(2)
print f(3)

#Functions can also be called using keyword arguments of the form "keyword = value".
#For instance, the following function:

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print "-- This parrot wouldn't", action,
    print "if you put", voltage, "volts through it."
    print "-- Lovely plumage, the", type
    print "-- It's", state, "!"

parrot(1000)
parrot(action = 'VOOOOOM', voltage = 1000000)
parrot('a thousand', state = 'pushing up the daisies')
parrot('a million', 'bereft of life', 'jump')

#When a final formal parameter of the form **name is present, it receives a dictionary containing all keyword arguments except for those corresponding to a formal parameter. This may be combined with a formal parameter of the form *name (described in the next subsection) which receives a tuple containing the positional arguments beyond the formal parameter list. (*name must occur before **name.) For example, if we define a function like this:

def cheeseshop(kind, *arguments, **keywords):
    print "-- Do you have any", kind, '?'
    print "-- I'm sorry, we're all out of", kind
    for arg in arguments: print arg
    print '-'*40
    keys = keywords.keys()
    keys.sort()
    for kw in keys: print kw, ':', keywords[kw]

#It could be called like this:

print delim,"demonstration of using *name and **name to process the list of arguments and keyword arguments\n"
cheeseshop('Limburger', "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           client='John Cleese',
           shopkeeper='Michael Palin',
           sketch='Cheese Shop Sketch')

