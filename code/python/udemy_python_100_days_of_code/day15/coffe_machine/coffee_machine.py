"""
Coffee Machine requirements
a. print report 
b. can serve one of three hot Coffees: espresso, latte, cappuccino 
c. must use its resources, water, milk and Coffee and verfies resources are sufficient to make the order
d. operates on coins, penny, nickel, dime quarter
e. check if payment is sufficient and give change if needed. 
"""

from coffee_machine_exceptions import *


class coffeeMachine:
    """
   A coffee machine
    """

    turn_off_str = "off"
    coins_prompt_str = "Please insert coins."
    coins_how_many_str = "How many "
    coins_value = {"quarters": 0.25, "dimes": 0.10, "nickles": 0.05, "pennies": 0.01, }

    MENU = {
        "espresso": {
            "ingredients": {
                "water": 50,
                "coffee": 18,
                "milk": 0,
            },
            "cost": 1.5,
        },
        "latte": {
            "ingredients": {
                "water": 200,
                "milk": 150,
                "coffee": 24,
            },
            "cost": 2.5,
        },
        "cappuccino": {
            "ingredients": {
                "water": 250,
                "milk": 100,
                "coffee": 24,
            },
            "cost": 3.0,
        }
    }

    resources = {
        "water": 300,
        "milk": 200,
        "coffee": 100,
    }

    def __init__(self):
        self.resources = coffeeMachine.resources.copy()
        self.money = 0

    def showPrompt(self):
        products = coffeeMachine.MENU.keys()
        products_str = '('
        for prod in products:
            products_str += prod
            products_str += "/"
        products_str = products_str[:-1]  # remove trailing )
        products_str += ")"
        promptStr = f"What would you like? {products_str}: "
        userInp = input(promptStr)
        return userInp

    def showCoinsPrompt(self):
        print(coffeeMachine.coins_prompt_str)
        quarters = int(input(f"{coffeeMachine.coins_how_many_str} quarters?: "))
        dimes = int(input(f"{coffeeMachine.coins_how_many_str} dimes?: "))
        nickles = int(input(f"{coffeeMachine.coins_how_many_str} nickles?: "))
        pennies = int(input(f"{coffeeMachine.coins_how_many_str} pennies?: "))
        #print(f"[debug] You gave {quarters} quarters, {dimes} dimes, {nickles} nickles, {pennies} pennies")
        return quarters, dimes, nickles, pennies

    def printReport(self):
        print(f'Water: {self.resources["water"]}')
        print(f'Milk: {self.resources["milk"]}')
        print(f'Coffee: {self.resources["coffee"]}')
        print(f'Money: {self.money}')

    def _validate_product(self, product):
        if product not in coffeeMachine.MENU.keys():
            raise unknownProductError

    def areResourcesSufficient(self, product):
        self._validate_product(product)
        for ingredient, amount in coffeeMachine.MENU[product]["ingredients"].items():
            #print(f"[debug] required {ingredient} amount is {amount}, machine has {self.resources[ingredient]}")
            if amount > self.resources[ingredient]:
                print(f"Sorry there is not enough {ingredient}")
                raise insufficientIngredientError(ingredient, amount, self.resources[ingredient])
            else:
                pass
        return True

    def _validate_coins(self, quarters, dimes, nickles, pennies):
        if quarters<0:
            raise invalidCoinAmount("quarters", quarters)
        if dimes<0:
            raise invalidCoinAmount("dimes", dimes)
        if nickles<0:
            raise invalidCoinAmount("nickles", nickles)
        if pennies<0:
            raise invalidCoinAmount("pennies", pennies)

    def _calc_total(self, quarters, dimes, nickles, pennies):
        self._validate_coins(quarters, dimes, nickles, pennies)
        return quarters*self.coins_value["quarters"]+dimes*self.coins_value["dimes"] + nickles*self.coins_value["nickles"]+pennies*self.coins_value["pennies"]


    def _make_coffe(self, product):
        for resource in self.resources:
            self.resources[resource] -= coffeeMachine.MENU[product]["ingredients"][resource]
        self.money+=self.MENU[product]["cost"]
        print(f"Here is your {product} ☕️. Enjoy!")

    def process_transaction(self, payment, product):
        self.areResourcesSufficient(product)
        if payment >= coffeeMachine.MENU[product]["cost"]:
            change = payment - coffeeMachine.MENU[product]["cost"]
            if change:
                print(f"You paid {payment} for {product} costing {coffeeMachine.MENU[product]['cost']}. Here is your change {change:.4f}$")
            self._make_coffe(product)
        else:
            print("Sorry that's not enough money. Money refunded.")


    def run(self):
        prod = ""
        while prod != "off":
            try:
                prod = self.showPrompt()
                self._validate_product(prod)
            except unknownProductError:
                print(f"{prod} is not a valid product")

            try:
                self.areResourcesSufficient(prod)
            except insufficientIngredientError as iiError:
                print(iiError)

            quarters, dimes, nickles, pennies = self.showCoinsPrompt()
            total = self._calc_total(quarters, dimes, nickles, pennies)
            #print(f"[debug], you paid a total of {total}")
            self.process_transaction(total, prod)
