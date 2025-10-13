class expenses:
    wood_meter_price = 1500
    total_closets = 50000
    riad = 30000
    ACs=20000

    def printMe():
        #todo, auto print props
        print(vars(expenses))

def main():
    expenses.printMe()

if __name__ == "__main__":
    main()

