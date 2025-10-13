use core::time;
use std::thread::sleep;

fn demo_if_assignment() {
    println!(
        "Demonstrating if expression assignment, can be used to replace ternary operator ?: which doesn't exist in Rust :"
    );
    let condition = true;
    let cond_eval = if condition { "True" } else { "False" };
    println!("The value of cond_eval is: {}", cond_eval);
}

fn demo_match_statement() {
    println!("Demonstrating match statement:");
    let number = 13;
    match number {
        1 => println!("One!"),
        2 | 3 | 5 | 7 | 11 => println!("This is a prime number."),
        _ => println!("This is not a prime number."),
    }

    let programming_language = "C++";
    match programming_language {
        "Rust" => println!("{programming_language} is a great choice!"),
        "Python" => println!("{programming_language} is very popular!"),
        "JavaScript" => println!("{programming_language} is used for web development!"),
        "C++" => println!("{programming_language} is known for systems programming!"),
        "Perl" => println!("{programming_language} is known for text processing!"),
        _ => println!("{programming_language} is an interesting choice!"),
    }

    let number = 27;
    let match_result = match number {
        1 => "One!",
        2 | 3 | 5 | 7 | 11 => "This is a prime number.",
        13..=19 => "A teen number.",
        27 => "A number that is the cube of 3.",
        _ => "A number greater than 19 or less than 1. Not 27",
    };
    println!("The match result is: {}", match_result);

    let numbers = [1, 2, 3, 4, 5];
    println!("Demonstrating match guards, use conditionals and assign to temp variables:");
    match numbers {
        second_elem if numbers[1] % 2 == 0 => {
            println!(
                "The second element {} is even? {:?}",
                numbers[1], second_elem
            )
        }
        third_elem if numbers[2] % 2 != 0 => {
            println!("The third element {} is odd? {:?}", numbers[2], third_elem)
        }
        _ => println!("No specific conditions met for the second or third elements."),
    }
    println!("End of match statement demonstration.");
}

fn demo_loops() {
    println!("Demonstrating loops:");
    // use loop for timer
    println!("Demo break keyword. Starting a countdown timer:");
    let mut timer = 5; // seconds
    loop {
        println!("Timer: {} seconds remaining", timer);
        sleep(std::time::Duration::from_secs(1));
        timer -= 1;
        if timer == 0 {
            break;
        }
    }

    println!("Demo continue keyword. Print even numbers from 1 to 20:");
    for number in 1..=20 {
        if number % 2 != 0 {
            continue;
        }
        println!("Even number: {}", number);
    }
}

fn demo_while_loop() {
    println!("Demonstrating while loop:");
    let mut timer = 5;
    while timer > 0 {
        println!("Timer: {} seconds remaining", timer);
        sleep(std::time::Duration::from_secs(1));
        timer -= 1;
    }
    println!("End of while loop demonstration.");
}

fn demo_recursion() {
    println!("Demonstrating recursion:");
    fn factorial(n: u32) -> u32 {
        if n == 0 { 1 } else { n * factorial(n - 1) }
    }
    let number = 9;
    let result = factorial(number);
    println!("The factorial of {} is {}", number, result);
}

fn final_project() {
    /*
    Define a `color_to_number` function that accepts a 'color'
    parameter (a string). Use if, else if, and else
    statements to return a corresponding numeric value based
    on the following rules:
    1. If the color is "red", return 1.
    2. If the color is "green", return 2.
    3. If the color is "blue", return 3.
    4. If the color is any other string, return 0.

    Refactor the function above to use the `match` statement
    instead of if, else if, and else.

    Define a `factorial` function that calculates the
    factorial of a number. The factorial is the product
    of multiplying a number by every incremental
    number leading up to it, starting from 1.

    Examples:
    The factorial of 5 is 5 * 4 * 3 * 2 * 1 = 120
    factorial(5) should return 120.

    The factorial of 4 is 4 * 3 * 2 * 1 = 24
    factorial(4) should return 24.

    Implement two solutions/functions for the problem.
    The first solution should not use recursion.
    The second solution should use recursion.
    */

    fn color_to_number_if(color: &str) -> u32 {
        if color == "red" {
            1
        } else if color == "green" {
            2
        } else if color == "blue" {
            3
        } else {
            0
        }
    }

    fn color_to_number(color: &str) -> u32 {
        match color {
            "red" => 1,
            "green" => 2,
            "blue" => 3,
            _ => 0,
        }
    }

    fn fact_non_recursive(n: u32) -> u32 {
        let mut result = 1;
        for i in 1..=n {
            result *= i;
        }
        result
    }

    fn fact_recursive(n: u32) -> u32 {
        if n == 0 { 1 } else { n * fact_recursive(n - 1) }
    }

    // test the functions
    let colors = ["red", "green", "blue", "yellow", "purple"];
    for &color in &colors {
        let num_if = color_to_number_if(color);
        let num_match = color_to_number(color);
        println!(
            "Color: {}, If-Else Result: {}, Match Result: {}",
            color, num_if, num_match
        );
    }
    let test_numbers = [5, 4, 3, 2, 1, 0];
    for num in test_numbers {
        let fact_non_rec = fact_non_recursive(num);
        let fact_rec = fact_recursive(num);
        println!(
            "Number: {}, Non-Recursive Factorial: {}, Recursive Factorial: {}",
            num, fact_non_rec, fact_rec
        );
    }
}

fn main() {
    demo_if_assignment();
    demo_match_statement();
    demo_recursion();
    demo_loops();
    demo_while_loop();
    final_project();
}
