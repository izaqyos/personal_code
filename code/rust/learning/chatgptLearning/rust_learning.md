# week 1

##   ownership/borrowing, slices, lifetimes, `Result`/`?`, `From`/`Into`.
Ownership & Borrowing

What matters:

Moves by default (for non-Copy types).

&T = many readers; &mut T = single writer.

Clone only when you actually need another owned value.

Examples (moves, borrows, reborrows)

``` rust
// Moves vs borrows
pub fn take_ownership(mut s: String) -> usize {
    s.push('!'); // we own it, can mutate
    s.len()
}

pub fn borrow_shared_len(s: &String) -> usize {
    s.len() // many &T allowed
}

pub fn borrow_mut_append(s: &mut String) {
    s.push_str(" +mut"); // only one &mut at a time
}

pub fn reborrow_example() -> String {
    let mut s = "hi".to_string();
    let r1 = &s;             // shared borrow starts
    assert_eq!(r1.len(), 2);
    // shared borrows end here (no further use), so we can take &mut next:
    let r2 = &mut s;         // ok: last use of r1 above
    r2.push_str(" there");
    s                      // moved out (return)
}

```
##
# week 2