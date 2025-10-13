package main 
import (
	"fmt"
	"math"
)

func letterCombinations(digits string) []string {
	var digitsLetters = map[byte]string{'2':'abc', '3':'def', '4':'ghi', '5':'jkl', '6':'mno', '7', 'pqrs', '8', 'tuv', '9', 'wxyz'}
	ret := make([]string, 0, math.Pow(len(digits),4)
	for d := range digits {
		if (len(ret) == 0) {
			for c := range digitsLetters[d] {
				ret.append(c)
			} else {
				for c := range digitsLetters[d] {
					for retstr := range ret {
						
					}
			}
				
			}
		}
	}
    
}