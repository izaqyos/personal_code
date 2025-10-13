import unittest
from observer import Subject, Observer, ConcreteObserverA, ConcreteObserverB

class ObserverPatternTest(unittest.TestCase):

  def test_observer_pattern(self):
    subject = Subject()
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()

    subject.attach(observer_a)
    subject.attach(observer_b)

    subject.state = 0  # Should notify both observers
    subject.state = 2  # Should notify observer_b

    subject.detach(observer_b)  # Detach observer_b
    subject.state = 3  # Should not notify any observer

if __name__ == '__main__':
  unittest.main()
