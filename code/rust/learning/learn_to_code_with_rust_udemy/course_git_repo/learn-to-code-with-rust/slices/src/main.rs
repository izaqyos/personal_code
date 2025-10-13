fn slices_demo() {
    println!("--- Slices Demo ---");
    let my_string = String::from("hello world");
    let my_str_slice = &my_string[0..5];
    let my_2nd_slice = &my_string[6..11];
    println!("String: {}", my_string);
    println!(
        "Prefix Slice: {}, Suffix Slice: {my_2nd_slice}",
        my_str_slice
    );

    println!("Note that slices are references, so the original string is still accessible:");
    println!(
        "Also note that slice length is in bytes, not characters. This matters for non-ASCII characters."
    );
    let unicode_str = String::from("🙏🥳❤️");
    let unicode_slice = &unicode_str[0..8]; // Each emoji is 4 bytes
    println!("Unicode String: {}", unicode_str);
    println!("Unicode Slice: {}", unicode_slice);
    println!("Unicode Slice Length (in bytes): {}", unicode_slice.len());

    println!("slices shortcuts...");
    let shortcut1 = &my_string[..5]; // same as &my_string[0..5]
    let shortcut2 = &my_string[6..]; // same as &my_string[6..my_string.len()]
    let shortcut3 = &my_string[..]; // same as &my_string[0..my_string.len()]
    println!(
        "Shortcut1: {}, Shortcut2: {}, Shortcut3: {}",
        shortcut1, shortcut2, shortcut3
    );

    println!("Demo deref coercion with slices...");
    fn print_str(s: &str) {
        println!("Str is: {}", s);
    }
    let s = String::from("Hello, Rust!");
    let s_slice = &s[..];

    print_str(s_slice);
    print_str(&s); // String is coerced to &str, doesn't work the other way around
    // meaning you can't pass a &str to a function expecting a String

    println!("--- End of Slices Demo ---");
}

fn array_slices_demo() {
    println!("--- Array Slices Demo ---");
    let arr = [1, 2, 3, 4, 5];
    let arr_slice = &arr[1..4]; // Slicing from index 1 to 3
    let arr_full_slice = &arr[..]; // Full slice of the array
    println!("Array: {:?}", arr);
    println!("Array Slice: {:?}", arr_slice);
    println!("Array Full Slice: {:?}", arr_full_slice);

    println!("Demo deref coercion with array slices...");
    fn print_array_slice(s: &[i32]) {
        println!("Array slice is: {:?}", s);
    }
    print_array_slice(arr_slice);
    print_array_slice(&arr); // Array is coerced to slice
    println!("Array slices can be used similarly to string slices.");

    println!("Mutable array slices...");
    let mut arr_mut = [10, 20, 30, 40, 50];
    {
        let arr_mut_slice = &mut arr_mut[1..4]; // Mutable slice from index 1 to 3
        arr_mut_slice[0] = 99; // Modify the first element of the slice
        println!("Modified Array Slice: {:?}", arr_mut_slice);
    }
    println!("Array after modifying slice: {:?}", arr_mut);
    println!("--- End of Array Slices Demo ---");
}

fn final_project() {
    /*
    Define a `cereals` array with 5 heap Strings
      - Cookie Crisp
      - Cinnamon Toast Crunch
      - Frosted Flakes
      - Cocoa Puffs
      - Captain Crunch

    Declare a `first_two` variable that extracts a slice
    of the first two cereals. Print the slice.

    Declare a `mid_three` variable that extracts a slice
    of the middle three cereals (Cinnamon Toast Crunch
    up to and including Cocoa Puffs). Print the slice.

    Declare a `last_three` variable that extracts a slice
    of the last three cereals. Print the slice.

    Using the `last_three` slice, target the last element
    ("Captain Crunch") and replace it with "Lucky Charms".
    Print the complete `cereals` array.

    Declare a `cookie_crisp` variable that references the
    "Cookie Crisp" String.

    Declare a `cookie` variable that extracts a slice of
    the text "Cookie" from the String. Print the slice.

    Declare a `cocoa_puffs` variable. Make it a reference
    to the "Cocoa Puffs" String (in other words, a &String).

    Declare a `puffs` variable that extracts a slice of
    the text "Puffs" from the String. Print the slice.
    */

    let mut cereals = [
        String::from("Cookie Crisp"),
        String::from("Cinnamon Toast Crunch"),
        String::from("Frosted Flakes"),
        String::from("Cocoa Puffs"),
        String::from("Captain Crunch"),
    ];
    let first_two = &cereals[0..2];
    println!("First two cereals: {:?}", first_two);

    let mid_three = &cereals[1..4];
    println!("Middle three cereals: {:?}", mid_three);

    let last_three = &mut cereals[2..];
    println!("Last three cereals: {:?}", last_three);
    last_three[2] = String::from("Lucky Charms");
    println!("Cereals after modification: {:?}", cereals);

    let cookie_crisp = &cereals[0];
    let cookie = &cookie_crisp[..6];
    println!("Slice of 'Cookie' from 'Cookie Crisp': {}", cookie);
    let cocoa_puffs = &cereals[3];
    let puffs = &cocoa_puffs[6..];
    println!("Slice of 'Puffs' from 'Cocoa Puffs': {}", puffs);
}
fn main() {
    slices_demo();
    array_slices_demo();
    final_project();
}
