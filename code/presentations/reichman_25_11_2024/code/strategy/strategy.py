from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """
    Abstract base class for payment strategies.
    """
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    """
    Concrete strategy for paying with a credit card.
    """
    def pay(self, amount):
        print(f"Paying ${amount} using Credit Card")

class PayPalPayment(PaymentStrategy):
    """
    Concrete strategy for paying with PayPal.
    """
    def pay(self, amount):
        print(f"Paying ${amount} using PayPal")

class Order:
    """
    Context class that uses a PaymentStrategy to process payments.
    """
    def __init__(self, payment_strategy):
        self._payment_strategy = payment_strategy

    def checkout(self, amount):
        self._payment_strategy.pay(amount) 
