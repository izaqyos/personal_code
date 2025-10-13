////c++ style
//fn foo(x: i32) -> &'static str{
//
//    let mut res: &'static str;
//
//    if (x<10){
//        res = "x is smaller than ten";
//    }
//    else{
//        res = "x is bigger or equal than ten";
//    }
//}

//rust style
fn bar(x: i32) -> &'static str{
    if x<10 {
        "x is smaller than ten"
    }
    else{
        "x is bigger or equal than ten"
    }
}

fn main() {
//    foo(5);
    println! ("bar is {}", bar(7));

    let mut x = 10;
    while x>0 {
        println!("x={}",x);
        x-=1;
    }
}
