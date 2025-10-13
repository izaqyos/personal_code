package main

import "fmt"

type contactInfo struct {
	email string
	zip   int
}
type person struct {
	firstName string
	lastName  string
	contact   contactInfo //can also just declare type like below
	// contactInfo //can also just declare type
}

func main() {
	fmt.Println("Demo structs")

	yosi := person{
		firstName: "Yosi",
		lastName:  "Izaq",
		contact: contactInfo{
			email: "izaqyos@gmail.com",
			zip:   342431,
		},
	} // order matters!!

	// deby := person{firstName: "Deby", lastName: "Izaq"} // init by name is better
	deby := person{
		firstName: "Deby",
		lastName:  "Izaq",
		contact: contactInfo{
			email: "idebyosi@gmail.com",
			zip:   342431,
		},
	} // order matters!!
	var may person // assigns zero values (string "", num 0, etc)
	may.firstName = "May"
	//fmt.Println(yosi)
	// fmt.Println(deby)
	//fmt.Printf("%+v\n", may) //print by k,v

	debyPtr := &deby
	debyPtr.updateName("Debora")
	deby.print()
	//or shortcut version, go will automatically pass the address
	yosi.updateName("Josepe")
	yosi.print()
}

func (p person) updateNameByVal(newName string) {
	p.firstName = newName //Note, no change will happen - pass by value
}

func (p *person) updateName(newName string) {
	// (*p).firstName = newName //long form
	p.firstName = newName // short form will work.
}

func (p person) print() {
	fmt.Printf("%+v\n", p) //print by k,v
}
