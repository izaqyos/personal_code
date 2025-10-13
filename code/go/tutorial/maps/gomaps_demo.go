package main
import "fmt"

func main()  {
	fmt.Println("golang map basic demo")
	var familyAges map[string]int
	familyAges = make(map[string]int)
	familyAges["yosi"] = 45
	familyAges["deby"] = 44
	familyAges["may"] = 15
	familyAges["itay"] = 11
	familyAges["kay"] = 8
	familyAges["aimy"] = 6
	familyAges["jandoe"] = 65
	fmt.Println("range iterate all k,v pairs in map:")
	for name := range familyAges{
		fmt.Println(name, "age is", familyAges[name])
	}
	fmt.Println("test key in map")
	var age, found = familyAges["Guy"]
	if (found) {
		fmt.Println("Guy, of age:",age, "exists in dict")
	} else {
		fmt.Println("Guy, of age:",age, "doesn't exist in dict")
	}
	var _, found1 = familyAges["yosi"]
	if (found1) {
		fmt.Println("yosi exists in dict")
	} else {
		fmt.Println("yosi doesn't exist in dict")
	}


	fmt.Println("delete from map by key. note jandoe is deleted")
	delete(familyAges, "jandoe")
	for name := range familyAges{
		fmt.Println(name, "age is", familyAges[name])
	}
	
	fmt.Println("declare and init a map in one line")
	var capitols = map[string]string{"usa":"washington", "israel":"tel-aviv", "france": "paris"}
	fmt.Println(capitols)
}