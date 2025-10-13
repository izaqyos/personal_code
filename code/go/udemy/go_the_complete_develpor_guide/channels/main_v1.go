package main

import (
	"fmt"
	"net/http"
)

func main() {
	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://golang.org",
		"http://amazon.com",
		"http://stackoverflow.com",
	}

    c := make(chan string)
	for _, link := range links {
        go checklink(link, c)
        // fmt.Println(link, <-c) // also serial, since it blocks for input
	}

    // // Demo, how to get the five expected inputs from channel
    // fmt.Println(<-c)
    // fmt.Println(<-c)
    // fmt.Println(<-c)
    // fmt.Println(<-c)
    // fmt.Println(<-c)
    // // fmt.Println(<-c) // This line will block forever

    for i:=0; i<len(links); i++ {
        fmt.Println(<-c)
    }
}

func checklink(link string, c chan string) {
	_, err := http.Get(link)
	if err != nil {
		c<-link + " is not responding"
	}

	c <- link + " is up"
}
