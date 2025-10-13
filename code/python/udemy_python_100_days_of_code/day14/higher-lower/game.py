class Game:
    """
    main game class
    """

    class DataItems:
        """
        generator class for getting random items of data
        """
        def __init__(self):
            from game_data import data
            self.data = data

        def __iter__(self):
            import random
            while True:
                selected = random.randint(0, len(self.data)-1)
                yield self.data[selected]
                del self.data[selected]
                

    def __init__(self):
        self.data_items_generator = self.DataItems()
        self.data_items_iterator = iter(self.data_items_generator)

    def _greet_banner(self):
        from art import logo
        print(logo)

    def _get_random_item(self):
        return next(self.data_items_iterator)
        


    def display_prompt(self, a_choice, b_choice):
        import os
        from art import vs
        self._greet_banner()
        print(f"Compare A: {a_choice['name']}, a {a_choice['description']}, from {a_choice['country']}")
        print(vs)
        print(f"Against B: {b_choice['name']}, a {b_choice['description']}, from {b_choice['country']}")
        selection = ''
        while not (selection == 'A' or selection == 'B'):
            selection = input(f"Who has more followers?- Type 'A' or 'B' ").upper()
        os.system('clear')
        return selection

    def start_game(self):
        """
        display banner, enter main loop (num wrong answers left).
        choose two random entries, compare them 
        ask player who has more
        correct continue loop 
        wrong reduce guesses left

        on 0 guesses game over
        """
        a_choice = self._get_random_item()
        game_over = False
        score = 0
        while not game_over:
            b_choice = self._get_random_item()
            selection = self.display_prompt(a_choice, b_choice)
            if selection == 'A':
                if a_choice['follower_count']>b_choice['follower_count']:
                    score+=1
                else:
                    game_over = True
            if selection == 'B':
                if b_choice['follower_count']>a_choice['follower_count']:
                    score+=1
                else:
                    game_over = True
            if not game_over:
                print(f"You're right! score: {score}\n")
            a_choice = b_choice

        self._greet_banner()
        print(f"Wrong answer :( - You lose. Your score: {score}")








