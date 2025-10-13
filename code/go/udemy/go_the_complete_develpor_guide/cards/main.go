package main

func main() {
	// // ver1
	// // var card string = "Ace of spades"
	// card := newCard() //shorthand form of above
	// fmt.Println(card)

	// ver2 pre types
	// cards := []string{"card1", newCard()}

	cards := newDeck()
	// // convert to string
	// fmt.Println(cards.toString())
	cards.shuffle()
	cards.saveToFile("saved.deck")

	cards2 := readFromFile("saved.deck")
	// cards2 := readFromFile("nofile")
	cards2.print()

	// // ver 3 deal cards
	// // cards.print()
	// hand, remainingCards := deal(cards, 5)
	// hand.print()
	// remainingCards.print()

}

func newCard() string {
	return "Five of diamonds"
}
