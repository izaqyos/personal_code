package main

import "fmt"

func main(){
    colors := map[string]string {
        "red": "#ff0000",
        "green": "#ff0001", 
        "white": "#ff0002", 
    }

    var emptyMap map[string]string
    madeMap:= make(map[string]string)
    madeMap["white"] = "#ff0002"
    delete(madeMap, "white")

    fmt.Println(colors)
    fmt.Println(emptyMap)
    fmt.Println(madeMap)
    printMap(colors)

    
}

func printMap(m map[string]string) {
    for k,v:= range m {
        fmt.Println("k=",k, " v=",v)
    }
}


