use std::{
    char,
    fmt::{self, Display, Formatter, write},
};

fn ints_demo() {
    println!("Demo of integer types in Rust");
    // demo different signed and unsigned integer types in rust
    // and print allowed range for each
    let i8_min: i8 = i8::MIN;
    let i8_max: i8 = i8::MAX;
    let i8_val = 42i8; // suffix to force type

    /* compile error: error: literal out of range for `i8`
      --> src/main.rs:10:23
       |
    10 |     let i8_val2: i8 = 2500;
       |                       ^^^^
       |
       = note: the literal `2500` does not fit into the type `i8` whose range is `-128..=127`
       = help: consider using the type `i16` instead
       */
    // let i8_val2: i8 = 2500;
    println!("i8 min: {}, i8 val: {}, i8 max: {}", i8_min, i8_val, i8_max);

    let i16_min: i16 = i16::MIN;
    let i16_max: i16 = i16::MAX;
    let i16_val: i16 = -32000;
    println!(
        "i16 min: {}, i16 val: {}, i16 max: {}",
        i16_min, i16_val, i16_max
    );

    let i32_min: i32 = i32::MIN;
    let i32_max: i32 = i32::MAX;
    let i32_val: i32 = 42;
    println!(
        "i32 min: {}, i32 val: {}, i32 max: {}",
        i32_min, i32_val, i32_max
    );

    let i64_min: i64 = i64::MIN;
    let i64_max: i64 = i64::MAX;
    let i64_val: i64 = 42;
    println!(
        "i64 min: {}, i64 val: {}, i64 max: {}",
        i64_min, i64_val, i64_max
    );

    let i128_min: i128 = i128::MIN;
    let i128_max: i128 = i128::MAX;
    let i128_val: i128 = 42;
    println!(
        "i128 min: {}, i128 val: {}, i128 max: {}",
        i128_min, i128_val, i128_max
    );

    // unsigned
    let u8_min: u8 = u8::MIN;
    let u8_max: u8 = u8::MAX;
    let u8_val: u8 = 42;
    println!("u8 min: {}, u8 val: {}, u8 max: {}", u8_min, u8_val, u8_max);

    let u16_min: u16 = u16::MIN;
    let u16_max: u16 = u16::MAX;
    let u16_val: u16 = 42;
    println!(
        "u16 min: {}, u16 val: {}, u16 max: {}",
        u16_min, u16_val, u16_max
    );

    let u32_min: u32 = u32::MIN;
    let u32_max: u32 = u32::MAX;
    let u32_val: u32 = 42;
    println!(
        "u32 min: {}, u32 val: {}, u32 max: {}",
        u32_min, u32_val, u32_max
    );

    let u64_min: u64 = u64::MIN;
    let u64_max: u64 = u64::MAX;
    let u64_val: u64 = 42;
    println!(
        "u64 min: {}, u64 val: {}, u64 max: {}",
        u64_min, u64_val, u64_max
    );

    let u128_min: u128 = u128::MIN;
    let u128_max: u128 = u128::MAX;
    // compiler ignores _ in int values representation
    // so use for readability
    let u128_val: u128 = 543_210_987_654_321_0;
    println!(
        "u128 min: {}, u128 val: {}, u128 max: {}",
        u128_min, u128_val, u128_max
    );
}

fn strs_demo() {
    println!("Demo of strings in Rust");
    // demo different string types in rust
    // demo special characters \n \r \t
    // demo raw strings r#" "# r##" "##
    let s1: &str = "\\hello\n\tmy love\n";
    let s2: String = String::from("world");
    println!("s1: {}, s2: {}", s1, s2);

    let raw_str1: &str = r"C:\Windows\File\Path";
    println!("raw_str1: {}\n", raw_str1);
}

fn methods_demo() {
    println!("Demo of methods in Rust");
    let neg_val: i16 = -20;
    let require_trim = "     rust    ";
    println!("neg_val: {}, abs: {}", neg_val, neg_val.abs());
    println!(
        "invoking pow method on {neg_val} to get square value {}.",
        neg_val.pow(2)
    );
    println!(
        "require_trim: '{}', trimmed: '{}'",
        require_trim,
        require_trim.trim()
    );

    let float_val: f64 = 3.14159;
    println!(
        "floor and ceil methods called on pi, floor: {}, ceil: {}, formatted for 3 decimal places: {float_val:.3} and for 5 decimal places: {:.5}",
        float_val.floor(),
        float_val.ceil(),
        float_val
    );
}

fn casting_demo() {
    println!("Demo of casting in Rust");
    let float_val: f64 = 65.7834;
    let int_val: i64 = float_val as i64;
    println!("float_val: {}, casted int_val: {}", float_val, int_val);
}

fn math_ops_demo() {
    //demo common math operators in rust
    println!("Demo of math operations in Rust");

    // demo arithmetic ops
    let a: i32 = 10;
    let b = 3;
    println!(
        "a: {}, b: {}, a*b={}, b/a (q only - will be floored) = {}, b/a (r) = {}, b/a float = {}, a-b={}, a+b={}",
        a,
        b,
        a * b,
        b / a,
        b % a,
        b as f64 / a as f64,
        a - b,
        a + b
    );
}

fn augmented_assignment_demo() {
    println!("Demo of augmented assignment in Rust");
    let mut a = 10;
    let b = 3;
    a += b;
    println!("a += b: {}", a);
    a -= b;
    println!("a -= b: {}", a);
    a *= b;
    println!("a *= b: {}", a);
    a /= b;
    println!("a /= b: {}", a);
    a %= b;
    println!("a %= b: {}", a);
}

fn bools_demo() {
    println!("Demo of booleans in Rust");
    let t = true;
    let f = false;
    println!("t: {}, f: {}", t, f);
    println!("expression evaluation examples");
    println!("10 > 5: {}", 10 > 5);
    println!("is 10 positive {}", 10i32.is_positive());
    println!("! operator on false: {}", !f);

    println!("Equal/not equal operators");
    println!("10 == 10: {}", 10 == 10);
    println!("10 != 5: {}", 10 != 5);

    println!("Logical operators and && , or || , xor ^");
    println!("true && false: {}", true && false);
    println!("true || false: {}", true || false);
    println!("true ^ false: {}", true ^ false);

    println!(" bitwise operators");
    println!("10 & 5: {}", 10 & 5);
    println!("10 | 5: {}", 10 | 5);
    println!("10 ^ 5: {}", 10 ^ 5);
}

fn unicode_demo() {
    println!("Demo of Unicode in Rust");
    let heart_eyed_cat = '😻';
    let grinning_face = '😀';
    let rocket = '🚀';
    let heart: char = '\u{2764}';
    let alphabetic_char: char = 'd';
    let uppercase_char: char = 'E';

    println!(
        "Unicode characters: {}, {}, {}, {}",
        heart_eyed_cat, grinning_face, rocket, heart
    );

    println!(
        "Is '{}' alphabetic? {}, is '{}' a digit? {}, is '{}' alphabetic? {}, is '{}' uppercase? {}",
        alphabetic_char,
        alphabetic_char.is_alphabetic(),
        alphabetic_char,
        alphabetic_char.is_digit(10),
        rocket,
        rocket.is_alphabetic(),
        uppercase_char,
        uppercase_char.is_uppercase()
    );
}

fn arrays_demo() {
    println!("Demo of arrays in Rust");
    let numbers: [i32; 5] = [1, 2, 3, 4, 5];
    let apples: [&str; 3] = ["Grand smith", "Pink lady", "Granny"];
    // note that {} invokes the display trait fmt method
    // {:?} invokes the debug trait fmt method
    // which is useful for inspecting complex data structures that
    // don't implement the display trait, e.g. arrays
    // also note that {:#?} pretty prints the output
    println!("numbers: {:?}, apples: {:#?}", numbers, apples);
    println!("Number of apples: {}", apples.len());

    // access array elements by index
    println!("First apple: {}", apples[0]);
    println!("Second apple: {}", apples[1]);
    println!("Third apple: {}", apples[2]);
}

fn traits_demo() {
    println!("Demo of traits in Rust");
    // demo display trait
    #[derive(Debug)] // derive debug trait for dbg! macro
    struct Cat {
        name: String,
        age: u8,
    }

    impl Display for Cat {
        fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
            if !f.alternate() {
                // check if concise print requested
                return write!(f, "Cat: {}, Age: {}", self.name, self.age);
            }

            write!(f, "Cat: {}, Age: {}", self.name, self.age)
        }
    }

    let cat1 = Cat {
        name: String::from("Whiskers"),
        age: 3,
    };
    println!("Cat details: {}", cat1); // use Cat Display trait
    // demo dbg! macro
    dbg!(cat1);
}

fn tuples_demo() {
    println!("Demo of tuples in Rust");
    // demo tuple
    let person = ("Yosi", "Izaq", 49);
    let (yosi_name, yosi_surname, yosi_age) = person;
    println!("Person details: {:?}", person);
    println!("First name: {}", person.0);
    println!("Last name: {}", person.1);
    println!("Age: {}", person.2);
    println!(
        "Destructured: Name: {}, Surname: {}, Age: {}",
        yosi_name, yosi_surname, yosi_age
    );
}

fn ranges_demo() {
    println!("Demo of ranges in Rust");
    let range = 1..5; // exclusive range
    let range2 = 3..=20; // inclusive range
    for i in range {
        println!("Iterating over exclusive range: {}", i);
    }

    println!("Inclusive range: {range2:?}");
    let chars_range = 'd'..='k'; // inclusive range
    for c in chars_range {
        println!("Iterating over character range: {}", c);
    }
}
fn main() {
    println!("--------------------------------");
    ints_demo();
    println!("--------------------------------");
    strs_demo();
    println!("--------------------------------");
    methods_demo();
    println!("--------------------------------");
    casting_demo();
    println!("--------------------------------");
    math_ops_demo();
    println!("--------------------------------");
    augmented_assignment_demo();
    println!("--------------------------------");
    bools_demo();
    println!("--------------------------------");
    unicode_demo();
    println!("--------------------------------");
    arrays_demo();
    println!("--------------------------------");
    traits_demo();
    println!("--------------------------------");
    tuples_demo();
    println!("--------------------------------");
    ranges_demo();
    println!("--------------------------------");
}
