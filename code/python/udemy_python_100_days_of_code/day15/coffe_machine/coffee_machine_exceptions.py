class coffeMachineError(Exception):
    """ Base exception for all coffee machine errors """


class unknownProductError(coffeMachineError):
    """ Product is not in list of valid products """


class insufficientIngredientError(coffeMachineError):
    """ Ingredients are not sufficient to make product """

    def __init__(self, ingredient, required_amount, available_amount, message="Ingredients are not sufficient to "
                                                                              "make product"):
        self.ingredient = ingredient
        self.required_amount = required_amount
        self.available_amount = available_amount
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (
            f"{self.message}. Details: required ingredient={self.ingredient}, required amount={self.required_amount},"
            f"available amount={self.available_amount}"
        )

class invalidCoinAmount(coffeMachineError):
    """ invalid amount of coins. like negative"""

    def __init__(self, coin_type, coin_amount, message="Invalid coin amount"):
        self.coin_type = coin_type
        self.coin_amount= coin_amount
        self.message = f"{message}. coin: {coin_type}, amount: {coin_amount}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
