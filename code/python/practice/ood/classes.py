class base:
    'this is me practicing ood in python doc string'

    classVar = "This is an example of a class variable"

    def __init__(self, msg):
        self.msg = msg

    def __del__(self):
        print 'base dtor called'
       
    def printMe(self):
        print 'Message: {}'.format(self.msg)

class derived(base):
    'derived class'

    def __init__(self, msg):
        self._protectedMsg = msg
        self.__privateMsg = msg

    def __del__(self):
        print 'derived dtor called'

    def __str__(self):
        return 'derived class msg. Protected member: {}. Private member: {}. '.format(self._protectedMsg , self.__privateMsg)

def main():
    b = base("from base class")
    b.printMe()
    d = derived('of derived class')


    print str(d)

    if issubclass(derived, base):
        print 'derived is a subclass of base'

    if isinstance(d, derived):
        print 'd is an instance of derived'

    if hasattr(b, 'classVar'):
        print "Instance b has attribute classVar. value: {}".format(getattr(b,'classVar'))
        setattr(b, 'classVar', 'modified message')
        print "changed value to: ".format(getattr(b,'classVar'))
        delattr(b,'classVar')
        if not hasattr(b, 'classVar'):
            print "attr classVar was deleted"
        else:
            print 'cant delete class variable with delattr'


if __name__ == "__main__":
    main()
