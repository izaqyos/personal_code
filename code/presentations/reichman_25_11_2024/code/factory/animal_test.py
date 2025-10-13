import unittest
from animal import Animal, Dog, Cat, AnimalFactory

class AnimalFactoryTest(unittest.TestCase):

    def test_create_dog(self):
        animal = AnimalFactory.create_animal("dog")
        self.assertIsInstance(animal, Dog)
        self.assertEqual(animal.speak(), "Woof!")

    def test_create_cat(self):
        animal = AnimalFactory.create_animal("cat")
        self.assertIsInstance(animal, Cat)
        self.assertEqual(animal.speak(), "Meow!")

    def test_create_invalid_animal(self):
        animal = AnimalFactory.create_animal("bird")
        self.assertIsNone(animal)  # Or check for an exception if you raise one

if __name__ == '__main__':
    unittest.main()
