#!/usr/bin/python

print "File manipulation in python.\n"

print "Reading and Writing Files:"
print " open() returns a file object, and is most commonly used with two arguments: \"open(filename, mode)\"."
print "Open a file named 'dummy'."
f=open('dummy', 'w')
print f

print "\nTo read a file's contents, call f.read(size), which reads some quantity of data and returns it as a string. size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it's your problem if the file is twice as large as your machine's memory. Otherwise, at most size bytes are read and returned. If the end of the file has been reached, f.read() will return an empty string ("")."

print "Content of dummy: ", f.read()
print "A second call to read returns an empty string ", f.read()


print "\nf.readline() reads a single line from the file; a newline character (\n) is left at the end of the string, and is only omitted on the last line of the file if the file doesn't end in a newline. This makes the return value unambiguous; if f.readline() returns an empty string, the end of the file has been reached, while a blank line is represented by '\n', a string containing only a single newline."

print 'This is the first line of the file: ', f.readline()
print 'This is the second line of the file: ', f.readline()

print "\nf.readlines() returns a list containing all the lines of data in the file. If given an optional parameter sizehint, it reads that many bytes from the file and enough more to complete a line, and returns the lines from that. This is often used to allow efficient reading of a large file by lines, but without having to load the entire file in memory. Only complete lines will be returned."

print "All file lines \n", f.readlines()

print "\nAn alternate approach to reading lines is to loop over the file object. This is memory efficient, fast, and leads to simpler code is to iterate over the file lines.\n"

for line in f:
	print line,
        
print "\nThe alternative approach is simpler but does not provide as fine-grained control. Since the two approaches manage line buffering differently, they should not be mixed"

print "\nf.write(string) writes the contents of string to the file, returning None."

f.write('This is a test\n')

print "\nTo write something other than a string, it needs to be converted to a string first:"

value = ('the answer', 42)
s = str(value)
f.write(s)

print "\nf.tell() returns an integer giving the file object's current position in the file, measured in bytes from the beginning of the file."

print "\nTo change the file object's position, use \"f.seek(offset, from_what)\". The position is computed from adding offset to a reference point; the reference point is selected by the from_what argument. A from_what value of 0 measures from the beginning of the file, 1 uses the current file position, and 2 uses the end of the file as the reference point. from_what can be omitted and defaults to 0, using the beginning of the file as the reference point."

f = open('dummy', 'r+')
f.write('0123456789abcdef')
f.seek(5)     # Go to the 6th byte in the file
f.read(1)        
f.seek(-3, 2) # Go to the 3rd byte before the end
f.read(1)


print "File objects have some additional methods, such as isatty() and truncate() which are less frequently used; consult the Library Reference for a complete guide to file objects."

print "\nPickle is an important module for object to string serialization."
print "Strings can easily be written to and read from a file. Numbers take a bit more effort, since the read() method only returns strings, which will have to be passed to a function like int(), which takes a string like '123' and returns its numeric value 123. However, when you want to save more complex data types like lists, dictionaries, or class instances, things get a lot more complicated."

print "Rather than have users be constantly writing and debugging code to save complicated data types, Python provides a standard module called pickle. This is an amazing module that can take almost any Python object (even some forms of Python code!), and convert it to a string representation; this process is called pickling. Reconstructing the object from the string representation is called unpickling. Between pickling and unpickling, the string representing the object may have been stored in a file or data, or sent over a network connection to some distant machine."

print "If you have an object x, and a file object f that's been opened for writing, the simplest way to pickle the object takes only one line of code:\n"
print "pickle.dump(x, f)"
print "To unpickle the object again, if f is a file object which has been opened for reading:\n"
print "x = pickle.load(f)"


print "\nWhen you're done with a file, call f.close() to close it and free up any system resources taken up by the open file. After calling f.close(), attempts to use the file object will automatically fail."

f.close()
f.read()


