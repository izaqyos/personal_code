package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strings"
	"time"
)

type deck []string

func newDeck() deck {

	cards := deck{}
	cardSuites := []string{"Clubs", "Hearts", "Diamonds", "Spades"}
	cardValues := []string{"Ace", "Two", "Three", "Four"}

	// _ instead of real name to avoid unused var error
	for _, suite := range cardSuites {
		for _, val := range cardValues {
			cards = append(cards, val+" of "+suite)
		}
	}
	return cards
}

// d - this, deck - type
// by convention a receiver is abbreviated to 1-2 letters. hence 'd'
func (d deck) print() { // a receiver function only works on deck type. sorta equivalent to deck.print() in OO
	for i, card := range d {
		fmt.Println(i, card)
	}
}

func deal(d deck, handSize int) (deck, deck) {
	return d[:handSize], d[handSize:]
}

func (d deck) toString() string {
	return strings.Join([]string(d), ",")
}

func (d deck) saveToFile(fname string) error {
	return ioutil.WriteFile(fname, []byte(d.toString()), 0666)
}

func readFromFile(fname string) deck {
	bs, err := ioutil.ReadFile(fname)
	if err != nil {
		fmt.Println("read file got error", err)
		os.Exit(1)
	}
	return deck(strings.Split(string(bs), ","))
}

func (d deck) shuffle() {

	src := rand.NewSource(time.Now().UnixNano())
	r := rand.New(src)
	for i := range d {
		j := r.Intn(len(d))
		d[i], d[j] = d[j], d[i]
	}
}
