fn demo_slices() {
    let str = String::from("a string");
    println!("Demo rust slices. String slices are of type str");

    let slice1 = &str[0..1];
    let sameas_slice1 = &str[..1];
    let slice2 = &str[2..str.len()];
    let sameas_slice2= &str[2..];
    let strCopy= &str[..];
    println!("slice1={}, slice2={}", slice1, slice2);

}

fn main(){

    demo_slices();
}
