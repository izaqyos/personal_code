
fn main(){

    let x = 1; //inmutable - this is the default
    println!("x = {}", x);
    //x = 2; // ^^^^^ cannot assign twice to immutable variable
    //println!("x = {}", x);

    let mut y = 1; //mutable
    println!("y = {}", y);
    y = 2; // ^^^^^ cannot assign twice to immutable variable
    println!("y = {}", y);

    const PIE :f32 = 3.14159; //real const. can only be assigned constant expressions. not a result of a function or a RT value
    println!("a const, PIE = {}", PIE);

    let z = 3; //inmutable
    let z = z+1; //shadow original z, allow to set a new value and reuse name but still keep original z inmutable
    let z = z*3;
    println!("value of shadow z is {}", z);

    let str = "a string";
    println!("str = {}", str);
    let str = str.len(); //here we shadow for keeping same name after cast
    println!("str len = {}", str);

    //let mut str2 = "a string";
//    str2 = str2.len(); // This will gen error:
//    26 |     str2 = str2.len();
//   |            ^^^^^^^^^^ expected &str, found usize
//   |
//   = note: expected type `&str`
//              found type `usize`
//
}
