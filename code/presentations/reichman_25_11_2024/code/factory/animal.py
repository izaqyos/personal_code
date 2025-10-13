from abc import ABC, abstractmethod

class Animal(ABC):
    """
    Abstract base class for animals.
    """
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    """
    Concrete class for a Dog.
    """
    def speak(self):
        return "Woof!"

class Cat(Animal):
    """
    Concrete class for a Cat.
    """
    def speak(self):
        return "Meow!"

class AnimalFactory:
    """
    Factory class for creating Animal objects.
    """
    @staticmethod
    def create_animal(animal_type):
        """
        Factory method to create and return an Animal object based on the given type.
        """
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            return None  # Or raise an exception for invalid animal types
