fn copy_trait_demo() {
    println!("--- copy_trait_demo ---");
    let time = 2025;
    let year = time; // i32 implements Copy trait, so time is still valid after this line, year is a copy of time pushed to the stack
    println!("time is {}, time duplicate, year, is {}", time, year);
}

fn string_demo() {
    println!("--- String_demo ---");
    #[allow(unused_variables)]
    let str_val_stored_in_binary = "hello"; // str literal, stored in binary, immutable
    let mut s1 = String::new();
    s1.push_str("hello"); // concatenate string
    s1.push_str(" world");
    let s2 = String::from("world");
    println!("s1 created by new is {}, s2 created by from is {}", s1, s2);
    println!(
        "Note that String memory is partly on the call stack (reference to heap actually allocated strings, length and total capacity) , and partly on the heap (actual string data)"
    );
    println!("--- end of String_demo ---");
}

fn move_demo() {
    println!("--- move_demo ---");
    let s1 = String::from("hello");
    let s2 = s1; // s1 is moved to s2, s1 is no longer valid, note that its moved not copied because String does not implement Copy trait
    // in contrast to c++ who on = invoke copy constructor, Rust on = invokes move semantics
    // if we try to use s1 after this line, it will cause a compile error
    // println!("s1 is {}, s2 is {}", s1, s2); // this line would cause a compile error
    println!("s2 is {}", s2);
    let x = 5;
    let y = x; // i32 implements Copy trait, so x is still valid after this line, y is a copy of x pushed to the stack
    println!("x is {}, y is {}", x, y);
    println!("--- end of move_demo ---");
}

fn drop_demo() {
    println!("--- drop_demo ---");
    {
        let s = String::from("hello"); // s is valid from this point forward
        println!("s is {}", s);
    } // this scope is now over, and s is no longer valid, Rust calls drop function automatically to free the memory
    println!("s was auto dropped as it is out of scope now");

    #[allow(unused_variables)]
    let person = String::from("Alice");
    drop(person); // person is moved to drop function, and is no longer valid after this line
    // println!("person is {}", person); // this line would cause a compile error
    println!("person was manually dropped using drop function");
    println!("--- end of drop_demo ---");
}

fn clone_demo() {
    println!("--- clone_demo ---");
    let s1 = String::from("hello");
    let s2 = s1.clone(); // s1 is cloned to s2, both are valid and independent
    println!("s1 is {}, s2 is {}", s1, s2);
    println!("Note that clone performs a deep copy, and is more expensive than a simple move");
    println!("Also note that because we used clone s1 is still valid after the clone operation");
    println!("--- end of clone_demo ---");
}

fn burrow_demo() {
    println!("--- burrow_demo ---");
    let s1 = String::from("hello");
    let s1_ref = &s1; // s1_ref is a reference to s1, s1 is not moved, so it is still valid
    println!("s1 = '{}' s1_ref = '{}' .", s1, s1_ref);
    println!("--- end of burrow_demo ---");
}

fn ref_deref_demo() {
    println!("--- ref_dereff_demo ---");
    let num = 42;
    let num_ref = &num; // reference to num
    let num_deref = *num_ref; // dereference num_ref to get the value of num
    println!(
        "num = '{}' num_ref = '{}' num_deref = '{}' .",
        num, num_ref, num_deref
    );
    println!("Note that dereferencing a reference gives us back the original value");
    println!(
        "Also note that because of display trait, we can print a reference directly without dereferencing it explicitly"
    );
    println!("--- end of ref_dereff_demo ---");
}

fn pass_by_copy_vs_move_demo() {
    println!("--- pass_by_copy_vs_move_demo ---");
    println!("Note that in rust all parameters are immutable by default");
    let my_string = String::from("hello");
    fn takes_ownership(s: String) {
        println!(
            "Since String has no copy trait function takes_ownership / move: {}",
            s
        );
    } // s goes out of scope and is dropped here
    takes_ownership(my_string);
    //println!("{my_string} is no longer valid here"); // this line would cause a compile error

    fn makes_copy(x: i32) {
        println!(
            "Since i32 has a copy trait makes_copy creates a copy: {}",
            x
        );
    } // x goes out of scope here, but nothing special happens

    let x = 5;
    makes_copy(x); // x is copied to the function, and is still valid after this line
    println!("x is {}", x);

    fn concat(s: String) -> String {
        // note that without mut this function would not compile because s is immutable by default
        s + " world" // note that + operator takes ownership of the left operand and borrows the right operand
    }

    println!("concatenated string is {}", concat(String::from("hello")));
    println!("--- end of pass_by_copy_vs_move_demo ---");
}

fn ret_vals_demo() {
    println!("--- ret_vals_demo ---");
    fn gives_ownership() -> String {
        let some_string = String::from("hello");
        some_string // some_string is returned and moves out to the caller
    }

    let s1 = gives_ownership(); // s1 now owns the string returned by gives_ownership
    println!("s1 is {}", s1);

    fn takes_and_gives_back(a_string: String) -> String {
        a_string // a_string is returned and moves out to the caller
    }

    let s2 = String::from("world");
    let s3 = takes_and_gives_back(s2); // s2 is moved to the function and then returned, so s3 now owns it
    // println!("s2 is {}", s2); // this line would cause a compile error because s2 is no longer valid
    println!("s3 is {}", s3);
    println!("--- end of ret_vals_demo ---");
}

fn section_six_final_project() {
    /*
    Declare a `is_concert` variable set to a boolean.
    Declare a `is_event` variable assigned to `is_concert`.
    Will Rust move ownership? State your answer, then confirm
    by trying to printing both variables out.

    Declare a `sushi` variable to set to a string literal of "Salmon"
    Declare a `dinner` variable assigned to the `sushi` variable.
    Will Rust move ownership? State your answer, then confirm
    by trying to printing both variables out.

    Repeat the previous example but use a heap String instead.
    Will Rust move ownership? Explain why the result is different
    from the previous operation.

    The `clear` method modifies a heap String to have no content.
    Declare an `eat_meal` function that accepts a `meal` parameter
    of type String. In the body of `eat_meal`, invoke the `clear`
    method on the `meal` parameter.

    In the `main` function, invoke the `eat_meal` function and pass
    in your "Salmon" String. Explain what happens when the eat_meal
    function runs. Describe the complete movement of ownership of
    the "Salmon" String throughout the program.

    Say we want to keep the String around after `eat_meal` is
    called. How can we continue to have access to the String in
    the `main` function? Print out the (empty) String.
    */

    println!("--- final_project ---");
    let is_concert = true;
    let is_event = is_concert; // bool implements Copy trait, so is_event is a copy of is_concert

    let sushi = "Salmon"; // str literal, stored in binary, immutable
    let dinner = sushi; // str literal implements Copy trait, so dinner is a copy of

    println!("is_concert: {}, is_event: {}", is_concert, is_event);
    println!("sushi: {}, dinner: {}", sushi, dinner);

    let heap_sushi = String::from("Salmon");
    let heap_dinner = heap_sushi; // String does not implement Copy trait, so heap_sushi is moved to heap_dinner
    // println!("heap_sushi: {}, heap_dinner: {}", heap_sushi, heap_dinner); // this line would cause a compile error

    fn eat_meal(mut meal: String) {
        meal.clear(); // clear the content of the meal string
        println!("Inside eat_meal, meal after clear: '{}'", meal);
    } // meal goes out of scope and is dropped here 

    eat_meal(String::from("Salmon")); // "Salmon" is moved to eat_meal function

    // if we want to keep the String around after eat_meal is called, we can return it from the function
    fn eat_meal_and_return(mut meal: String) -> String {
        meal.clear(); // clear the content of the meal string
        meal // return the meal string
    }

    let heap_dinner_copy = eat_meal_and_return(heap_dinner);
    println!(
        "heap_dinner after eat_meal_and_return: '{}'",
        heap_dinner_copy
    );

    println!("--- final_project end ---");
}

fn section_7() {
    fn immutable_and_mutable_references() {
        println!("--- immutable_and_mutable_references ---");
        println!(
            "Since moved parameters must either be returned or dropped, we can use references to avoid moving ownership"
        );
        println!(
            "otherwise we would have to either clone or return the value, which can be inefficient and cumbersome"
        );
        println!(
            "A better approach is to use references, which allow us to refer to some value without taking ownership of it"
        );
        println!(
            "References are immutable by default, good for read only access. But we can create mutable references using the mut keyword for also modifying the value"
        );

        let mut s1 = String::from("hello");
        println!("s1 before modify_string: {}", s1);
        fn modify_string(s: &mut String) {
            s.push_str(" world");
        }
        modify_string(&mut s1);
        println!("s1 after modify_string: {}", s1);
        println!("--- end of immutable_and_mutable_references ---");
    }

    immutable_and_mutable_references();

    fn demo_unlimited_immutable_references() {
        println!("--- demo_unlimited_immutable_references ---");
        println!(
            "We can have multiple immutable references to a value, but only one mutable reference"
        );
        println!("This is to prevent data races at compile time");

        let s = String::from("hello");
        let r1 = &s;
        let r2 = &s;
        let r3 = &s; // we can have multiple immutable references to a value
        println!("r1: {}, r2: {}, r3: {}", r1, r2, r3);
        println!("--- end of demo_unlimited_immutable_references ---");
    }

    demo_unlimited_immutable_references();

    #[allow(unused_variables)]
    fn demo_mutable_and_immutable_references_conflict() {
        println!("--- demo_mutable_and_immutable_references lifecycle conflict ---");
        println!(
            "We cannot have a mutable reference while we have immutable references to the same value"
        );
        println!("Also only a single mutable reference is allowed at any given time");
        println!("This is to prevent data races at compile time");
        let mut s = String::from("hello");
        let r1 = &s; // no problem
        let r2 = &s; // no problem
        let r3 = &mut s; // BIG PROBLEM, cannot borrow `s` as mutable because it is also borrowed as immutable
        // println!("r1: {}, r2: {}, r3: {}", r1, r2, r3); // this line would cause a compile error
        println!("--- end of demo_mutable_and_immutable_references lifecycle conflict ---");
    }

    demo_mutable_and_immutable_references_conflict();

    fn demo_immutable_ref_copy_trait() {
        println!("--- demo_immutable_ref_copy_trait ---");
        println!(
            "immutable references implement the Copy trait, so we can still use the value after passing a reference to it"
        );
        let my_string = String::from("hello");
        let s_ref1 = &my_string;
        let s_ref2 = &s_ref1; // we can have multiple immutable references
        println!(
            "my_string: {}, s_ref1: {}, s_ref2: {}",
            my_string, s_ref1, s_ref2
        );
        println!("--- end of demo_immutable_ref_copy_trait ---");
    }

    demo_immutable_ref_copy_trait();

    fn demo_mutable_ref_move_trait() {
        println!("--- demo_mutable_ref_move_trait ---");
        println!(
            "mutable references do not implement the Copy trait, instead they implement the Move trait"
        );
        let mut my_string = String::from("hello");
        let s_ref1 = &mut my_string;
        let s_ref2 = s_ref1; // we now moved the mutable reference, s_ref1 is no longer valid
        // println!("s_ref1: {}, s_ref2: {}", s_ref1, s_ref2); // this line would cause a compile error, cannot borrow `s_ref1` as it was moved
        println!(
            "s_ref1 is now invalid since its moved to s_ref2. s_ref2 before modify: {}",
            s_ref2
        );
        s_ref2.push_str(" world");
        println!("s_ref2 after modify: {}", s_ref2);
        // println!("my_string after modify: {}", my_string); // this line would cause a compile error, cannot borrow `my_string` as immutable because it is also borrowed as mutable
        println!("--- end of demo_mutable_ref_move_trait ---");
    }
    demo_mutable_ref_move_trait();

    fn demo_dangling_references() {
        println!("--- demo_dangling_references ---");
        println!("Dangling references are references that point to invalid memory");
        println!(
            "Rust prevents dangling references at compile time by ensuring that references always point to valid memory"
        );
        println!("For example, the following code would not compile:");
        /*
        fn dangle() -> &String {
            let s = String::from("hello");
            &s // we are returning a reference to a local variable, which will be dropped when the function ends
        } // s goes out of scope here, and the reference would be dangling
        */
        println!("--- end of demo_dangling_references ---");
    }
    demo_dangling_references();

    fn demo_borrow_from_array() {
        println!("--- demo_borrow_from_array ---");
        let arr = [1, 2, 3];
        let r = arr[0];
        println!(
            "For i32 type when we do r =arr[0] the value is copied so r: {}",
            r
        );

        let arr2 = [String::from("hello"), String::from("world")];
        let r2 = &arr2[0]; // we are borrowing a reference to the first element of the array
        println!(
            "For String type (move, not copy) we can't do r2=arr2[0] as it will compromise the array. instead when we do r2 = &arr2[0] the value is borrowed so r2: {}",
            r2
        );
        println!("--- end of demo_borrow_from_array ---");
    }
    demo_borrow_from_array();

    fn final_project() {
        /*
        Let's model a road trip!

        Define a `start_trip` function that creates and returns
        a String of "The plan is..."

        Invoke the `start_trip` function in `main` and save its
        return value to a `trip` variable.

        We want to pass the String to three separate functions
        that will mutate the String without transferring ownership.

        Define a `visit_philadelphia` function that concatenates
        the text "Philadephia" to the end of the String. Invoke
        the function in `main`. Then, invoke `push_str` on the String
        to concatenate the content " and " to the end. Mak sure to
        include the spaces.

        Define a `visit_new_york` function that concatenates the
        text "New York" to the end of the String. Invoke the function
        in `main`. Repeat the previous logic to concatenate " and "
        to the end of the String.

        Define a `visit_boston` function that concatenates the
        text "Boston." to the end of the String. Invoke the function
        in `main`. Concatenate a period to the end of the
        String/sentence.

        Define a `show_itinerary` function that will print out
        the final version of the String. Find a way to do so
        without transferring ownership.

        Invoke `show_itinerary`. The final output should be:

        "The plan is...Philadelphia and New York and Boston."
        */

        fn start_trip() -> String {
            String::from("The plan is...")
        }

        let mut trip = start_trip();
        fn visit_philadelphia(trip: &mut String) {
            trip.push_str("Philadelphia");
        }

        visit_philadelphia(&mut trip);
        trip.push_str(" and ");
        fn visit_new_york(trip: &mut String) {
            trip.push_str("New York");
        }
        visit_new_york(&mut trip);
        trip.push_str(" and ");
        fn visit_boston(trip: &mut String) {
            trip.push_str("Boston.");
        }
        visit_boston(&mut trip);
        trip.push_str(".");

        fn show_itinerary(trip: &String) {
            println!("{}", trip);
        }

        show_itinerary(&trip);
    }
    final_project();
}

fn section_6() {
    copy_trait_demo();
    string_demo();
    move_demo();
    drop_demo();
    clone_demo();
    burrow_demo();
    ref_deref_demo();
    pass_by_copy_vs_move_demo();
    ret_vals_demo();
    section_six_final_project();
}

fn main() {
    section_6();
    section_7();
}
