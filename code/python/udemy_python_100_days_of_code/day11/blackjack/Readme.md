# Description

a game of blackjack


# Run

## Run 
``` bash
py3 src/main.py
```

## Run in debug mode
``` bash
py3 src/main.py --log=DEBUG
```

# Test

## Test all

``` bash
pytest
```

-s for stdout prints

``` bash
pytest 
```

## Test specific file

``` bash
$ pytest -s test/test_deck.py
```


Test specific method

``` bash
$ pytest -s test/test_deck.py::test_deal_cards
```

By keywords in test classes/methods names. And, or, not operator supported
Ex:

``` bash
$ pytest -s -k "deal or card"
```
