/*
Our goal is to build a program that will transform a
string using a pipeline of one or more transformations.
The transformations should be applicable in any order.

We'll build two text transformations to start:
- A whitespace transformation that removes whitespace
  from the beginning of the string, the end of the
  string, or both ends of the string
- A case transformation that converts the string to
  uppercase or lowercase

See the `main` function for the final code we want
to support. We'll build up a vector of trait objects,
each of which implements the `TextTransformer` trait.
The vector represents a pipeline, a sequential
collection of steps/transforms to apply to the target
String. We'll pass the vector to an `apply_transformations`
function that will apply the transformations in the
vector in order, passing each resulting String to the
next transformation.

If we encounter an error in a transformation, we want
to print the error out to the user, skip the
transformation, and pass the string to the next
transformation in the pipeline.

------------

Begin by defining a `TextTransformer` trait that
requires a `transform` method. The method will accept
an immutable reference to the instance and a string
slice. It should return a `Result` where the success
data will be a String and the error data will be a
dynamic error/trait object.

------------

Define a `WhitespaceTransformer` struct that stores
`start` and `end` fields, both set to Booleans. These
fields will dictate whether whitespace should be removed
from the start, the end, or both ends of the string.

Implement the `TextTransformer` trait for
`WhitespaceTransformer`. The `transform` method should
remove the whitespace from the appropriate end(s) of
the string, then return a `Result` with the String.

The `transform` method should also handle two errors:
- If the string contains a 🍕 emoji
- If the string is completely empty after whitespace
  has been removed

For both of these errors, define a new error type that
implements the `Error` trait.

In the `transform` method, check for both of the two
scenarios and return the appropriate error type. You'll
need to figure out a way to support different types of
errors being returned in the `Err` variant of the
returned `Result`.

------------

Define a `Case` enum with two variants: `Uppercase`
and `Lowercase`.

Define a `CaseTransformer` struct that stores a `case`
field set to a `Case` enum.

Implement the `TextTransformer` trait for
`CaseTransformer`. The `transform` method should
either capitalize or lowercase the passed-in string
and return the value in an `Ok` variant.

------------

Define an `apply_transformations` function that will
accept a String and a vector of trait objects that all
implement the `TextTransformer` trait. Find a way to iterate
over the vector, perform a transformation over the
starting string, then pass the resulting String to the
next transformation in sequence.

If you encounter an error (such as having a 🍕 emoji in
the string), gracefully handle the error by skipping the
current transformation and passing the current string
to the next transformation in line.

------------

In the `main` function, run the program with the 3
sample string inputs and confirm you see the expected
outputs and error messages print out.
*/

fn main() {
    // Input
    let text = String::from("  homer simpson  ");
    // Output
    // Content: "HOMER SIMPSON"

    // Input
    let text = String::from("  data  🍕  ");
    // Output
    // Error Message: Something went wrong: Hey, there's a pizza emoji in the text. So cheesy. Moving on to next transform
    // Content: "  DATA  🍕  "

    // Input
    let text = String::from("    ");
    // Output:
    // Error Message: Something went wrong: The string has nothing left in it. Moving on to next transform
    // Content: "    "

    let pipeline: Vec<Box<dyn TextTransformer>> = vec![
        Box::new(WhitespaceTransformer {
            start: true,
            end: true,
        }),
        Box::new(CaseTransformer {
            case: Case::Uppercase,
        }),
    ];

    let transformed_text = apply_transformations(text, pipeline);
    println!("Output: {transformed_text}");
}
