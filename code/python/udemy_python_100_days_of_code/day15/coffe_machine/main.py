from coffee_machine import coffeeMachine
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
def testCoffeMachine():
    myCoffeMachine = coffeeMachine()
    myCoffeMachine.printReport()
    myCoffeMachine.showPrompt()

def main():
    myCoffeMachine = coffeeMachine()
    myCoffeMachine.run()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# TODO write program
class coffeeMachine:
    """
   A coffee machine
    """

