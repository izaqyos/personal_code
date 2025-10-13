package main

import (
	"os"
	"testing"
)

func TestNewDeck(t *testing.T) {
	cards := newDeck()
	size := len(cards)

	if size != 16 {
		t.Errorf("Expected size 16. Got %d ", size)
	}

	if "Ace of Clubs" != cards[0] {
		t.Errorf("Expected Ace of Clubs. Got %s ", cards[0])
	}
	if "Four of Spades" != cards[len(cards)-1] {
		t.Errorf("Expected Four of Spades. Got %s ", cards[len(cards)-1])
	}
}

func TestSaveToDeckAndNewDeckFromFile(t *testing.T) {
	os.Remove("_decktesting")
	d := newDeck()
	d.saveToFile("_decktesting")
	d1 := readFromFile("_decktesting")

	if len(d1) != len(d) {
		t.Errorf("Read deck len %d. Expected %d", len(d1), len(d))
	}
	os.Remove("_decktesting")
}
