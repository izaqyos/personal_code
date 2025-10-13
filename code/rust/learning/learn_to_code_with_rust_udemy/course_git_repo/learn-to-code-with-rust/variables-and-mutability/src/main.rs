fn main() {
    let oranges: i32 = 5;
    let bananas: i32 = 20;
    let total_fruits = oranges + bananas;
    let _unused_variable = 10; // This variable is intentionally unused, use _ to tell rustc to ignore it
    println!(
        "Total fruits: {} = {oranges} oranges + {bananas} bananas",
        total_fruits
    );
    println!(
        "rust supports printing by using positional arguments: {0}, {1}, {2}",
        total_fruits, oranges, bananas
    );
}
