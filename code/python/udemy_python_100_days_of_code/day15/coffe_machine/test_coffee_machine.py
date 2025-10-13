import pytest
from coffee_machine_exceptions import *
from coffee_machine import *


def test_coffee_machine_resources():
    expected = {
        "water": 300,
        "milk": 200,
        "coffee": 100,
    }
    cm = coffeeMachine()
    assert (cm.resources == expected)


def test_coffee_machine_menu():

    expected = {
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
    cm = coffeeMachine()
    assert (cm.MENU == expected)


def test_areResourcesSufficient_WrongProduct():
    cm = coffeeMachine()
    with pytest.raises(unknownProductError):
        cm.areResourcesSufficient("coke-zero")


def test_areResourcesSufficient_not_sufficient():
    cm = coffeeMachine()
    cm.resources["water"] = 0
    with pytest.raises(insufficientIngredientError):
        cm.areResourcesSufficient("espresso")

def test_areResourcesSufficient_allgood():
    cm = coffeeMachine()
    is_sufficient = cm.areResourcesSufficient("espresso")
    assert (is_sufficient == True)
    is_sufficient = cm.areResourcesSufficient("latte")
    assert (is_sufficient == True)
    is_sufficient = cm.areResourcesSufficient("cappuccino")
    assert (is_sufficient == True)

def test_calc_total():
    cm = coffeeMachine()
    quarters, dimes, nickles, pennies = 0,0,0,0
    total = cm._calc_total(quarters, dimes, nickles, pennies)
    assert (total == 0)

    quarters, dimes, nickles, pennies = 4,2,5,6
    total = cm._calc_total(quarters, dimes, nickles, pennies)
    assert (total == 1.51)

    with pytest.raises(invalidCoinAmount):
        quarters, dimes, nickles, pennies = 4,2,-5,6
        cm._calc_total(quarters, dimes, nickles, pennies)

def test_process_transaction_positive():
    cm = coffeeMachine()
    cm.process_transaction(2, "espresso")
    assert (cm.resources["water"] == 250)
    assert (cm.resources["milk"] == 200)
    assert (cm.resources["coffee"] == 82)
    assert (cm.money == 1.5)
    cm.process_transaction(5, "latte")
    assert (cm.resources["water"] == 50)
    assert (cm.resources["milk"] == 50)
    assert (cm.resources["coffee"] == 58)
    assert (cm.money == 4)

def test_process_transaction_negative_short():
    cm = coffeeMachine()
    cm.process_transaction(2, "cappuccino")
    assert (cm.resources["water"] == 300)
    assert (cm.resources["milk"] == 200)
    assert (cm.resources["coffee"] == 100)
    assert (cm.money == 0)

def test_process_transaction_negative_out_of_water():
    cm = coffeeMachine()
    cm.process_transaction(3, "cappuccino")
    assert (cm.resources["water"] == 50)
    assert (cm.resources["milk"] == 100)
    assert (cm.resources["coffee"] == 76)
    assert (cm.money == 3.0)
    with pytest.raises(insufficientIngredientError):
        cm.process_transaction(3, "cappuccino")


