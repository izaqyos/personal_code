import unittest
from singelton import Singelton

class SingeltonTest(unittest.TestCase):

  def test_unique_instance(self):
    s1 = Singelton()
    s2 = Singelton()
    self.assertIs(s1, s2)  # Check if both instances are the same

  def test_value_increment(self):
    s = Singelton()
    s.increment_value()
    self.assertEqual(s.get_value(), 1)

if __name__ == '__main__':
  unittest.main()
