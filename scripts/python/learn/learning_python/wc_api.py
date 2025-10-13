def countLines(name) :
	#print "counting lines of %s"%name
	file = open(name,'r')
	return len(file.readlines())

def countChars(name) :
	#print "counting chars of %s"%name
	file = open(name,'r')
	return len(file.read())

def test(name):
	print "# lines in %s is %d"%(name, countLines(name))
	print "# chars in %s is %d"%(name, countChars(name))

if __name__ == '__main__':  test("/cygdrive/c/work/scripts/python/learn/learning_python/wc_api.py")
