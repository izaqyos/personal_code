package main

import "fmt"

func switchValDemo(n int)  {

    switch n {
    case 40,50:
        fmt.Printf("n is 40,50\n")
    case 64:
        fmt.Printf("n is 64\n")
    }
}

func switchTypeDemo(x interface{})  {
    switch x.(type) {
    case nil:
        fmt.Printf("type of x :%T\n",x)
    case int:
        fmt.Printf("x is int\n")
    case float64:
        fmt.Printf("x is float64\n")
    case func(int) float64:
        fmt.Printf("x is func(int)\n")
    case bool, string:
        fmt.Printf("x is bool or string\n")
    default:
        fmt.Printf("don't know the type\n")
    }

}
func main() {
    var x float64 //static type declaration
    x = 1.0
    fmt.Printf("x=%f, type %T\n", x, x)
    
    y:= 64 //dynamic type declaration
    fmt.Printf("y=%d, type %T\n", y, y)

    const PIE = 3.14
    fmt.Printf("pie is %f\n", PIE)
    switchValDemo(y)
    switchValDemo(40)
    switchTypeDemo(4.1)

}


