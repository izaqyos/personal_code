package main 

import "fmt"

type bot interface{
    getGreeting() string
}
type englishBot struct{}    
type spanishBot struct{}    


func main() {
    eb1 := englishBot{}
    printGreeting(eb1)
    sb1 := spanishBot{}
    printGreeting(sb1)
    
}

func ( englishBot) getGreeting() string {
    return "hello world"
}

//func ( sb spanishBot) getGreeting() string { //note when receiver ref is not used it can be ommited
func ( spanishBot) getGreeting() string {
    return "hola"
}


func  printGreeting(b bot) {
    fmt.Println(b.getGreeting())
}

// Demo why interfaces are needed
// func main() {
//     eb1 := englishBot{}
//     printGreeting(eb1)
//     sb1 := spanishBot{}
//     printGreeting(sb1)
//     
// }
// 
// func ( englishBot) getGreeting() string {
//     return "hello world"
// }
// 
// //func ( sb spanishBot) getGreeting() string { //note when receiver ref is not used it can be ommited
// func ( spanishBot) getGreeting() string {
//     return "hola"
// }
// 
// 
// func  printGreeting(eb englishBot) {
//     fmt.Println(eb.getGreeting())
// }
// 
// //printGreeting redeclared in this block error. no overloading in go!
// func  printGreeting(sb spanishBot) {
//     fmt.Println(sb.getGreeting())
// }








