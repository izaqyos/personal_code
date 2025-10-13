
fn foo(_x: &'static str) -> &'static str{ //foo is a function that gets a string argument and returns same type
    "world" //return is optional. last statmement in block w/o ; is return value
}

fn main() {

    // simple hello world
   // let world = "world";
   // println!("Hello, {}", world);
   
    println!("Hello {}", foo("bar"));

}
