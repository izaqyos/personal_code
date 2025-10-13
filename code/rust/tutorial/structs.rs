
#[derive(Debug)]
struct MyFirstStruct  {
    name: String,
    age: u32,
    is_male: bool
}

#[derive(Debug)]
struct Rect  {
    width: u32,
    height: u32,
}

impl Rect{
    fn square(length: u32) -> Rect{
        println!("associated function (no &self arg) square was called.");
        Rect{width: length, height: length}
    }

    fn area(&self) -> u32{
        self.width * self.height
    }
}

fn fillStruct(name: String, age: u32) -> MyFirstStruct{
    println!("using field init shorthand (when struct key and param name are same)");
    MyFirstStruct{
        name,
        age,
        is_male: true
    }
}

fn tuple_structs(){
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);
let msg = String::from("
Tuple structs have the added meaning the struct name provides but don’t have names associated with their fields; rather, they just have the types of the fields. Tuple structs are useful when you want to give the whole tuple a name and make the tuple be a different type from other tuples, and naming each field as in a regular struct would be verbose or redundant
                       ");
println!("{}", msg);
}

fn main(){

    let yosi = MyFirstStruct {
        name: String::from("yosi izaq"),
        age: 42,
        is_male: true
    };

//    yosi.age = 44; //oops this is not mutable
//    error[E0594]: cannot assign to field `yosi.age` of immutable binding
//  --> structs.rs:16:5
//   |
//10 |     let yosi = MyFirstStruct {
//   |         ---- help: make this binding mutable: `mut yosi`
//...
//16 |     yosi.age = 44;
//   |     ^^^^^^^^^^^^^ cannot mutably borrow field of immutable binding
//
//error: aborting due to previous error

    let mut dan = MyFirstStruct{
        name: String::from("Dan Shalom"),
        age: 32,
        is_male: true
    };
    dan.age=40;
    println!("mutable instance of struct MyFirstStruct {:?}",dan);

    let moshe = fillStruct("moshe".to_string(), 27);
    println!("moshe: {:?}",moshe);

    tuple_structs();

    let rect = Rect{width: 10, height: 20};
    println!("rect area = {}", rect.area());
}
