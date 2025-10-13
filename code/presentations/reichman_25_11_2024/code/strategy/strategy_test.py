import unittest
from strategy import CreditCardPayment, PayPalPayment, Order

class StrategyPatternTest(unittest.TestCase):

    def test_credit_card_payment(self):
        order = Order(CreditCardPayment())
        order.checkout(100)  # Output: Paying $100 using Credit Card

    def test_paypal_payment(self):
        order = Order(PayPalPayment())
        order.checkout(50)  # Output: Paying $50 using PayPal

if __name__ == '__main__':
    unittest.main()
