use std::io;
use rand::Rng;
use std::cmp::Ordering;

fn main() {
    println!("guessing game :)");

    let secret = rand::thread_rng().gen_range(1,101);

    loop {
        println!("plz enter a number !");
        let mut guess = String::new();

        io::stdin().read_line(&mut guess)
            .expect("Failed to read line");

        ////cast guess to u32 and crash if not castable to int
        //let guess :u32 = guess.trim().parse()
        //    .expect("Please type a number");
        
        //cast guess to u32 and retake input if not castable to int
        let guess :u32 = match guess.trim().parse() {
            Ok(n) => n,
            Err(_) => continue,
        };

        println!("you guessed {}", guess);

        match guess.cmp(&secret){
            Ordering::Less => print!("too small\n"),
            Ordering::Greater => print!("too big\n"),
            Ordering::Equal => {
                print!("you win\n");
                break;
            },
        }
    }
}
