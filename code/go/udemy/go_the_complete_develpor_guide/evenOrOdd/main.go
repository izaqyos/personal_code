package main

import "fmt"

func main() {
	nums := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	for i := range nums {
		if i%2 != 0 {
			fmt.Println(i, " is odd")
		} else {
			fmt.Println(i, " is even")
		}
	}

}
