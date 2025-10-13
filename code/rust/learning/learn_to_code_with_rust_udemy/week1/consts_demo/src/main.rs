const MAX_POINTS: u32 = 100_000;
const CELSIUS_TO_FAHRENHEIT: f32 = 1.8;
const FAHRENHEIT_OFFSET: f32 = 32.0;
const PI: f32 = 3.14159;
const SIEZE_THE_DAY_LATIN: &str = "Carpe Diem";

fn main() {
    println!("constants (known at compile time, can have global scope) demo");
    println!("Max points: {}", MAX_POINTS);
    println!("Celsius to Fahrenheit: {}", CELSIUS_TO_FAHRENHEIT);
    println!("Fahrenheit offset: {}", FAHRENHEIT_OFFSET);
    println!("Pi: {}", PI);
    println!("Seize the day (Latin): {}", SIEZE_THE_DAY_LATIN);
}
