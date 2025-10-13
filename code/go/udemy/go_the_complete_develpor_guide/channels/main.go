cat main.go
package main

import (
	"fmt"
	"net/http"
    "time"
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

    // // Variant 1. for loop that contains a call blocking on channel
    // for { 
    //     go checklink(<-c, c)
    // }

    //// Variant 2. Prefered syntax for loop that contains a call blocking on channel
    //for l:= range c { 
    //    time.Sleep(1*time.Second) // wrong place to sleep. sleeps main routine so it will only process one value on channel every 5 seconds
    //    go checklink(l, c)
    //}

    // // Variant 3. use function-literal to sleep after response on channel
    // for l:= range c { 
    //     go func(){
    //         time.Sleep(1*time.Second) 
    //         checklink(l,c) // l variable is referencing outer scope variable. That's a big problem since both main routine and child
    //         // routines reference the same var. This will lead to race condition and unexpected results.
    //     }()
    // }

    // Variant 4. use function-literal to sleep after response on channel
    for l:= range c { 
        go func(link string ){
            time.Sleep(1*time.Second) 
            checklink(link,c) 
        }(l)// fix l variable is referencing outer scope variable. pass by value. now main and sub routines have separate copies
    }




}

func checklink(link string, c chan string) {
    // time.Sleep(1*time.Second) // another wrong place to sleep. each sub routine will wait 5 seconds before it starts 
	_, err := http.Get(link)
	if err != nil {
        fmt.Println(link,  " is not responding")
		c<-link
	}

    fmt.Println(link, " is up")
	c <- link
}

