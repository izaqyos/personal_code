fn demo_named_structs() {
    println!("----------------------------------");
    println!("Demo named structs");
    // first demo struct declaration
    struct Coffee {
        name: String,
        price: f64,
        milk_type: String,
        is_hot: bool,
    }

    // now we can create instances of Coffee
    let black = Coffee {
        name: String::from("Black Coffee"),
        price: 2.5,
        milk_type: String::from("None"),
        is_hot: true,
    };

    let my_soy = Coffee {
        price: 3.5,
        milk_type: String::from("Soy"),
        name: String::from("Soy Latte"),
        is_hot: true,
    };

    println!(
        "Black coffe - name: {}, price: {}, milk_type: {}, is_hot: {}",
        black.name, black.price, black.milk_type, black.is_hot
    );
    println!(
        "Soy Latte - name: {}, price: {}, milk_type: {}, is_hot: {}",
        my_soy.name, my_soy.price, my_soy.milk_type, my_soy.is_hot
    );

    println!("----------------------------------");
    // demo issue when moving ownership of String fields (or any non-Copy type)
    println!("Demo moving ownership of String field");
    let coffee_name = my_soy.name;
    // println!("Coffee name: {}", my_soy.name); // this line will cause a compile-time error
    println!("Coffee name: {}", coffee_name);

    println!("----------------------------------");
    println!(" Demo struct update syntax");
    let mut my_iced = Coffee {
        name: String::from("Iced Latte"),
        is_hot: false,
        ..my_soy // move remaining fields from my_soy
    };
    my_iced.price = 4.0; // modify price
    my_iced.milk_type = String::from("Almond"); // modify milk_type
    println!(
        "Almond Iced Latte - name: {}, price: {}, milk_type: {}, is_hot: {}",
        my_iced.name, my_iced.price, my_iced.milk_type, my_iced.is_hot
    );

    println!("----------------------------------");
    // demo factory function to create Coffee instances
    fn make_coffee(name: &str, price: f64, milk_type: &str, is_hot: bool) -> Coffee {
        Coffee {
            name: String::from(name),
            price,
            milk_type: String::from(milk_type),
            is_hot,
        }
    }
    let cappuccino = make_coffee("Cappuccino", 3.0, "Whole", true);
    println!(
        "Factory function created Cappuccino - name: {}, price: {}, milk_type: {}, is_hot: {}",
        cappuccino.name, cappuccino.price, cappuccino.milk_type, cappuccino.is_hot
    );

    println!("----------------------------------");
    println!(
        "Demo syntactic sugar for field init shorthand in factory function and instance creation"
    );
    fn make_coffee_shorthand(name: String, price: f64, milk_type: String, is_hot: bool) -> Coffee {
        Coffee {
            name,      // field init shorthand
            price,     // field init shorthand
            milk_type, // field init shorthand
            is_hot,    // field init shorthand
        }
    }
    let espresso = make_coffee_shorthand(String::from("Espresso"), 2.0, String::from("None"), true);
    println!(
        "Factory function created Espresso - name: {}, price: {}, milk_type: {}, is_hot: {}",
        espresso.name, espresso.price, espresso.milk_type, espresso.is_hot
    );

    println!("----------------------------------");
    // instance creation with field init shorthand
    let name = String::from("Latte");
    let price = 3.5;
    let milk_type = String::from("Oat");
    let is_hot = true;
    let latte = Coffee {
        name,
        price,
        milk_type,
        is_hot,
    };
    println!(
        "Instance created Latte - name: {}, price: {}, milk_type: {}, is_hot: {}",
        latte.name, latte.price, latte.milk_type, latte.is_hot
    );

    println!("----------------------------------");
    println!("Demo struct update syntax with ownership transfer (aka spread operator)");
    let my_mocha = Coffee {
        name: String::from("Mocha"),
        price: 4.0,
        milk_type: String::from("Whole"),
        is_hot: true,
    };
    let mut my_iced_mocha = Coffee {
        name: String::from("Iced Mocha"),
        is_hot: false,
        ..my_mocha // move remaining fields from my_mocha
    };
    println!(
        "Iced Mocha - name: {}, price: {}, milk_type: {}, is_hot: {}",
        my_iced_mocha.name, my_iced_mocha.price, my_iced_mocha.milk_type, my_iced_mocha.is_hot
    );
    // println!("My mocha name: {}", my_mocha.name); // this line will cause a compile-time error as name ownership moved

    println!(
        "To avoid ownership issues, we can use .clone() for non copy types like String and arrays"
    );

    println!("----------------------------------");
    println!("Demo passing structs to functions");
    fn print_coffee_info(coffee: Coffee) {
        println!(
            "Coffee - name: {}, price: {}, milk_type: {}, is_hot: {}",
            coffee.name, coffee.price, coffee.milk_type, coffee.is_hot
        );
    }

    // fn bad_mutate_coffee(coffee: Coffee) {
    //     // this function won't compile as we are trying to mutate an immutable binding
    //     coffee.price += 1.0; // increase price by 1.0
    //     coffee.is_hot = !coffee.is_hot; // toggle is_hot
    // }

    fn good_mutate_coffee(coffee: &mut Coffee) {
        // this function will compile as we are taking ownership and mutating a mutable binding
        println!(
            "Mutating Coffee inside function. Note that we can access field to a refed struct using dot notation since rust auto-derefs (*coffee).field to coffee.field...  "
        );
        coffee.price += 1.0; // increase price by 1.0
        coffee.is_hot = !coffee.is_hot; // toggle is_hot
        println!(
            "Mutated Coffee inside function - name: {}, price: {}, milk_type: {}, is_hot: {}",
            coffee.name, coffee.price, coffee.milk_type, coffee.is_hot
        );
    }

    good_mutate_coffee(&mut my_iced_mocha); // pass a clone to avoid ownership issues
    println!("After good_mutate_coffee function call");
    print_coffee_info(my_iced_mocha);
    println!("Note: my_iced_mocha ownership moved into function");
    // println!("{}", my_iced_mocha); // this line will cause a compile-time error as ownership moved

    println!("End of demo named structs");
}

fn second_struct_demo() {
    println!("----------------------------------");
    println!("Second struct demo");

    println!("Demo derive debug trait for printing struct instances");
    #[derive(Debug)] // automatically implement the Debug trait for Coffee
    struct Coffee {
        name: String,
        price: f64,
        milk_type: String,
        is_hot: bool,
    }
    let my_coffee = Coffee {
        name: String::from("Flat White"),
        price: 3.0,
        milk_type: String::from("Whole"),
        is_hot: true,
    };
    println!("My coffee using debug trait: {:?}", my_coffee);
    println!("My coffee using pretty print debug trait: {:#?}", my_coffee);

    // demo printing a struct with debug trait
    #[derive(Debug)]
    struct Point {
        x: i32,
        y: i32,
    }
    let p = Point { x: 10, y: 20 };
    println!("Point using debug trait: {:?}", p);
    println!("Point using pretty print debug trait: {:#?}", p);

    // demo methods on structs
    println!("Demo methods on structs");
    println!(
        "First method parameter is self, which represents the instance the method is called on"
    );
    println!(
        "Self can be passed by value (self), by mutable value (mut self), by reference (&self), or by mutable reference (&mut self)"
    );
    println!(
        "self type is either StructName, Self or abbreviated to pass no type (same as : Self)"
    );
    #[derive(Debug)]
    struct Person {
        name: String,
        age: u32,
        occupation: String,
    }

    impl Person {
        // associated function (like a static method)
        fn new(name: String, age: u32, occupation: String) -> Person {
            Person {
                name,
                age,
                occupation,
            }
        }

        fn print_name(self: Self) {
            println!("Person's name is: {}", self.name);
        }

        // method to display person's info
        fn display_info(&self) {
            println!(
                "Person - name: {}, age: {}, occupation: {}",
                self.name, self.age, self.occupation
            );
        }

        // method to have a birthday (increment age)
        fn have_birthday(&mut self) {
            self.age += 1;
            println!(
                "Happy birthday, {}! You are now {} years old.",
                self.name, self.age
            );
        }

        fn is_older(&self, other: &Self) -> bool {
            self.age > other.age
        }
    }

    let mut alice = Person::new(String::from("Alice"), 30, String::from("Engineer"));
    // demo instantiation without using the new function
    let rabbit = Person {
        name: String::from("White Rabbit"),
        age: 5,
        occupation: String::from("Timekeeper"),
    };
    let knave_of_hearts = Person {
        name: String::from("Knave of Hearts"),
        age: 15,
        occupation: String::from("Card Soldier"),
    };

    alice.display_info();
    alice.have_birthday();
    alice.display_info();
    alice.print_name();
    // next line would cause a compile-time error as print_name takes self by value and ownership moves
    // alice.print_name(); takes ownership of alice self instance and moves it
    // since its not captured we lose access to alice after this call!!
    //println!("Debug print of alice: {:?}", alice);
    rabbit.display_info();
    println!(
        "Is Knave of Hearts older than White Rabbit? {}",
        knave_of_hearts.is_older(&rabbit)
    );
    knave_of_hearts.display_info();

    println!("End of second struct demo");
}

fn associated_functions_demo() {
    println!("----------------------------------");
    println!("Demo associated functions (static methods)");
    #[derive(Debug)]
    struct Rectangle {
        width: u32,
        height: u32,
    }

    impl Rectangle {
        // associated function to create a square
        fn square(size: u32) -> Rectangle {
            Rectangle {
                width: size,
                height: size,
            }
        }

        // associated function to create a rectangle
        fn new(width: u32, height: u32) -> Rectangle {
            Rectangle { width, height }
        }
    }
    //demo that impl can have multiple blocks
    impl Rectangle {
        // method to calculate area
        fn area(&self) -> u32 {
            self.width * self.height
        }
    }

    let my_square: Rectangle = Rectangle::square(10);
    let my_rectangle: Rectangle = Rectangle::new(10, 20);
    println!("My square: {:?}, area: {}", my_square, my_square.area());
    println!(
        "My rectangle: {:?}, area: {}",
        my_rectangle,
        my_rectangle.area()
    );

    println!("End of associated functions demo");
}

fn builder_pattern_demo() {
    println!("----------------------------------");
    println!("Demo builder pattern");

    #[derive(Debug)]
    struct ProductState {
        name: String,
        price: f64,
        category: String,
        state: String,
    }

    impl ProductState {
        fn new(name: String, price: f64, category: String) -> ProductState {
            ProductState {
                name,
                price,
                category,
                state: String::from("Created"),
            }
        }

        fn move_to_be_shipped(&mut self) -> &mut Self {
            self.state = String::from("Pending Shipment");
            self
        }

        fn ship_product(&mut self) -> &mut Self {
            self.state = String::from("Shipped");
            self
        }

        fn deliver_product(&mut self) -> &mut Self {
            self.state = String::from("Delivered");
            self
        }
    }

    let mut my_product = ProductState::new(
        String::from("Ipone 17 Pro Max"),
        1199.99,
        String::from("Smartphones"),
    );
    println!("Initial product state: {:?}", my_product);
    my_product
        .move_to_be_shipped()
        .ship_product()
        .deliver_product();
    println!("Final product state: {:#?}", my_product);

    println!("End of builder pattern demo");
}

fn tuple_structs_demo() {
    println!("----------------------------------");
    println!("Demo tuple structs");

    #[derive(Debug)]
    struct Color(u8, u8, u8); // RGB color

    #[derive(Debug)]
    struct Point(i32, i32); // 2D point

    let black = Color(0, 0, 0);
    let white = Color(255, 255, 255);
    let origin = Point(0, 0);
    let point_a = Point(10, 20);

    println!("Black color: {:?}", black);
    println!("White color: {:?}", white);
    println!("Origin point: {:?}", origin);
    println!("Point A: {:#?}", point_a);

    // Accessing fields by index
    println!(
        "Black color - R: {}, G: {}, B: {}",
        black.0, black.1, black.2
    );
    println!("Point A - x: {}, y: {}", point_a.0, point_a.1);

    impl Point {
        fn translate(&mut self, dx: i32, dy: i32) {
            self.0 += dx;
            self.1 += dy;
        }

        fn distance_from_origin(&self) -> f64 {
            ((self.0.pow(2) + self.1.pow(2)) as f64).sqrt()
        }

        fn add_point(&mut self, other: &Point) {
            self.0 = self.0 + other.0;
            self.1 = self.1 + other.1;
        }
    }

    let mut p = Point(3, 4);
    let q = Point(1, 2);
    p.add_point(&q);
    println!("Point p before translation: {:?}", p);
    p.translate(1, 2);
    println!("Point p after translation: {:?}", p);
    println!(
        "Distance of point p from origin: {}",
        p.distance_from_origin()
    );

    println!("End of tuple structs demo");
}

fn unit_like_struct_demo() {
    println!("----------------------------------");
    println!("Demo unit-like structs");

    struct Marker; // unit-like struct

    let _m1 = Marker;
    let _m2 = Marker;

    println!("Unit-like struct instances created: _m1 and _m2");

    impl Marker {
        fn identify(&self) {
            println!("This is a unit-like struct instance.");
        }
    }

    _m1.identify();
    _m2.identify();

    println!("End of unit-like structs demo");
}

fn final_project() {
    /*
    Define a Flight struct with the following fields:
      - an `origin` field (String)
      - a `destination` field (String)
      - a `price` field (f64)
      - a `passengers` field (u32)

    Derive a Debug trait implementation for the Flight struct.

    Define a `new` constructor function that returns a new
    instance of a Flight.

    Define a `change_destination` method that accepts a new
    destination and overwrites the value of the `destination`
    field.

    Define a `increase_price` method that raises the value
    of the `price` by 20% (multiply the `price` field by 1.20).
    Make sure to save the new `price` field value.

    Define a `itinerary` method that prints out both the
    `origin` and `destination` fields in the following format
    (origin -> destination).

    Use the constructor function to create a new Flight instance
    in the main function. Invoke all of the defined methods.
    Print out the struct in Debug format to confirm the struct
    updates as you expect.

    Use struct update syntax to copy the `price` and `passengers`
    fields to a new Flight struct instance. Make sure to provide
    new Strings for the remaining fields to ensure ownership
    doesn't transfer. Assign the new Flight to a separate variable.
    */

    println!("----------------------------------");
    println!("Final project, flight struct with methods");
    #[derive(Debug)]
    struct Flight {
        origin: String,
        destination: String,
        price: f64,
        passengers: u32,
    }

    impl Flight {
        fn new(origin: String, destination: String, price: f64, passengers: u32) -> Flight {
            Flight {
                origin,
                destination,
                price,
                passengers,
            }
        }

        fn change_destination(&mut self, new_destination: String) {
            self.destination = new_destination;
        }

        fn increase_price(&mut self) {
            self.price *= 1.20;
        }

        fn itinerary(&self) {
            println!("Itinerary: {} -> {}", self.origin, self.destination);
        }
    }

    let mut inbount_to_argentina = Flight::new(
        String::from("Tel Aviv"),
        String::from("Buenos Aires"),
        1600.0,
        150,
    );
    println!("Initial flight: {:#?}", inbount_to_argentina);
    inbount_to_argentina.change_destination(String::from("Cordoba"));
    inbount_to_argentina.increase_price();
    inbount_to_argentina.itinerary();
    println!("Updated flight: {:#?}", inbount_to_argentina);

    let second_flight = Flight {
        origin: String::from("New York"),
        destination: String::from("London"),
        ..inbount_to_argentina // move price and passengers from inbount_to_argentina
    };
    println!("Second flight: {:#?}", second_flight);
    println!("End of final project");
}

fn main() {
    demo_named_structs();
    second_struct_demo();
    associated_functions_demo();
    builder_pattern_demo();
    tuple_structs_demo();
    unit_like_struct_demo();
    final_project();
}
