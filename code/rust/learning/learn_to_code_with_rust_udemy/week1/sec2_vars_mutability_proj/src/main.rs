
/*
Declare a `season` variable set to a string with
your favorite season. Provide an explicit type annotation.
The type of a string is a `&str`. We'll discuss what
the & symbol means later in the course.
 
Declare a `points_scored` variable set to 28.
Provide an explicit type annotation. The type of
an integer is `i32`.
 
It's time to update the team's score. Declare the
`points_scored` variable to be mutable. Set its
new value to 35.
 
Declare a `TOUCHDOWN_POINTS` constant at the file
level set to the value 6.
 
Declare a `event_time` variable set to a string of
"06:00".
 
Use variable shadowing to redeclare `event_time` set
to a integer of 6.
 
Use interpolation to print out all of the
declared variables and constants in a println! call.
Practice using direct interpolation {value}, sequential
arguments ( {} ), and numeric arguments ( {0} ).
 
Declare a `favorite_beverage` variable set to a string
of your favorite drink. Use an underscore to silence
the compiler warning about the variable being unused.
 
Remove the underscore. Provide a compiler directive
to silence the compiler warning about the variable
being unused.
 */

type POINTS = i32;
const TOUCHDOWN_POINTS: POINTS = 6;

fn main() {
    println!("Section 2 final project");
    let season: &str = "Summer";

    #[allow(unused_mut)]
    let mut points_scored: POINTS = 28;

    #[allow(unused_variables)]
    let event_time: &str = "06:00";
    let event_time: i32 = 6;

    // silence unused variable warning using _ prefix
    let _favorite_beverage: &str = "Coffee";
    // silence unused variable warning using a directive
    #[allow(unused_variables)]
    let _favorite_beverage: &str = "Coffee";
    println!("Printing all variables using sequential arguments. TOUCHDOWN_POINTS: {}, season: {}, points_scored: {}, event_time: {}", TOUCHDOWN_POINTS, season, points_scored, event_time);    
    println!("Printing all variables using positional arguments. TOUCHDOWN_POINTS: {0}, season: {1}, points_scored: {2}, event_time: {3}", TOUCHDOWN_POINTS, season, points_scored, event_time);    
    println!("Printing all variables using variable interpolation. TOUCHDOWN_POINTS: {TOUCHDOWN_POINTS}, season: {season}, points_scored: {points_scored}, event_time: {event_time}");    
}


