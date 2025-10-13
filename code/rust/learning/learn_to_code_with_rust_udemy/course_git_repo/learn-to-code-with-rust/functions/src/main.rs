fn demo_explicit_return() -> i32 {
    println!("This function uses an explicit return statement.");
    return 42;
}

fn demo_implicit_return() -> i32 {
    println!("This function uses an implicit return statement returning the last expression.");
    24 // No semicolon means this is the return value
}

fn demo_unit() {
    println!("This function returns the unit type ().");
    println!("a unit - empty tuple () is returned by default if no return value is specified.");
    // ()
}

fn main_functions_project() {
    /*
    Define an apply_to_jobs function that accepts a
    'number' parameter (an i32) and a 'title' parameter
    (a string). It should print out the string:
    "I'm applying to {number} {title} jobs".

    Example:
    apply_to_jobs(35, "Rust Developer")
    -> "I'm applying to 35 Rust Developer jobs"

    Define an is_even function that accepts a 'number'
    parameter (an i32). The function should return a true
    if the number is even and a false if the number is
    odd.
    Examples:
    is_even(8) -> true
    is_even(9) -> false

    Define an alphabets function that accepts a 'text'
    parameter (an &str). The function should return a
    tuple of two Booleans. The first Boolean should check
    if the text contains the letter 'a'. The second
    Boolean should check if the text contains the letter
    'z'. You can use the 'contains' method to check if a
    string contains a specific character. See the documentation:
    https://doc.rust-lang.org/std/primitive.str.html#method.contains

    Examples:
    println!("{:?}", alphabets("aardvark")); -> (true, false)
    println!("{:?}", alphabets("zoology"));  -> (false, true)
    println!("{:?}", alphabets("zebra"));    -> (true, true)
    */

    fn apply_to_jobs(number: i32, title: &str) {
        println!("I'm applying to {} {} jobs", number, title);
    }

    fn is_even(number: i32) -> bool {
        number % 2 == 0
    }

    fn alphabets(text: &str) -> (bool, bool) {
        (text.contains('a'), text.contains('z'))
    }

    apply_to_jobs(3, "Software Engineer");
    apply_to_jobs(2, "Data Scientist");
    println!("is_even(8) -> {}", is_even(8));
    println!("is_even(9) -> {}", is_even(9));
    println!("alphabets(\"aardvark\") -> {:?}", alphabets("aardvark"));
    println!("alphabets(\"zoology\") -> {:?}", alphabets("zoology"));
    println!("alphabets(\"zebra\") -> {:?}", alphabets("zebra"));
}

fn main() {
    let value = demo_explicit_return();
    println!("The returned value is: {}", value);

    let second_value = demo_implicit_return();
    println!("The returned value is: {}", second_value);

    let unit_value = demo_unit();
    println!("The returned unit value is: {:?}", unit_value);

    main_functions_project();
}
