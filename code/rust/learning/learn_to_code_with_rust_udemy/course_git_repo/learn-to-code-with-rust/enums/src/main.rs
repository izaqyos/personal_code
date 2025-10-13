fn enums_demo() {
    println!("Enums in Rust:");

    #[derive(Debug)]
    enum Direction {
        Up,
        Down,
        Left,
        Right,
    }

    let player_direction = Direction::Up;

    match player_direction {
        Direction::Up => println!("Player is moving up!"),
        Direction::Down => println!("Player is moving down!"),
        Direction::Left => println!("Player is moving left!"),
        Direction::Right => println!("Player is moving right!"),
    }

    println!("Player direction is {:#?}.", player_direction);

    #[derive(Debug)]
    enum WeekDays {
        Monday,
        Tuesday,
        Wednesday,
        Thursday,
        Friday,
        Saturday,
        Sunday,
    }

    let today = WeekDays::Monday;
    println!("Today is {:?}.", today);

    println!("Demo enums associated values:");
    println!("assciate tuple values to enum variants");
    #[derive(Debug)]
    struct CustomColorScheme {
        primary: String,
        secondary: String,
        background: String,
    }

    #[derive(Debug)]
    enum Color {
        Rgb(u8, u8, u8),
        Cmyk {
            cyan: u8,
            magenta: u8,
            yellow: u8,
            black: u8,
        },
        CustomScheme(CustomColorScheme),
    }

    let black = Color::Cmyk {
        cyan: 0,
        magenta: 0,
        yellow: 0,
        black: 255,
    };
    let orange = Color::Rgb(255, 165, 0);
    let white = Color::Rgb(255, 255, 255);
    let custum_color = Color::CustomScheme(CustomColorScheme {
        primary: String::from("#FF5733"),
        secondary: String::from("#33FF57"),
        background: String::from("#3357FF"),
    });

    // demo nested enums
    #[derive(Debug)]
    enum SunGlasses {
        RayBan(Color),
        Oakley(Color),
        Gucci(Color),
        Prada(Color),
    }

    let my_sunglasses = SunGlasses::RayBan(Color::Cmyk {
        cyan: 0,
        magenta: 0,
        yellow: 0,
        black: 255,
    });

    println!(
        "Black color: {:?}, white color: {:?}, Orange: {:#?}, custom color: {:#?}, my black sunglasses: {:#?}",
        black, white, orange, custum_color, my_sunglasses
    );

    println!("End of enums demo.");
}

fn demo_match() {
    println!("Demo match statement:");

    enum TrafficLight {
        Red,
        Yellow,
        Green,
        Blue,
        Cyan,
    }

    let light = TrafficLight::Red;

    // demo match invoking functions
    match light {
        TrafficLight::Red => println!("Stop! The light is red."),
        TrafficLight::Yellow => println!("Caution! The light is yellow."),
        TrafficLight::Green => println!("Go! The light is green."),
        _ => println!("light color not supported for traffic lights!"),
    }

    // demo match returning values
    let action = match light {
        TrafficLight::Red => {
            println!("The light is red, stopping the car.");
            "Stop"
        }
        TrafficLight::Yellow => "Caution",
        TrafficLight::Green => "Go",
        _ => "Unknown action",
    };

    println!("The action for the current light is: {}", action);

    println!("Demo match access to enum associated values:");
    enum Shape {
        Circle(f64),          // radius
        Rectangle(f64, f64),  // width, height
        Square { side: f64 }, // side length
    }
    let shape = Shape::Rectangle(10.0, 20.0);
    let square_shape = Shape::Square { side: 15.0 };
    let circle_shape = Shape::Circle(7.0);
    fn calculate_area(shape: &Shape) -> f64 {
        match shape {
            Shape::Circle(radius) => std::f64::consts::PI * radius * radius,
            Shape::Rectangle(width, height) => width * height,
            Shape::Square { side } => side * side,
        }
    }
    let area = calculate_area(&shape);
    let square_area = calculate_area(&square_shape);
    let circle_area = calculate_area(&circle_shape);
    println!("The area of the shape is: {}", area);
    println!("The area of the square shape is: {}", square_area);
    println!("The area of the circle shape is: {}", circle_area);

    println!("Demo match impl functions:");
    impl Shape {
        fn calc_area(&self) -> f64 {
            match self {
                Shape::Circle(radius) => std::f64::consts::PI * radius * radius,
                Shape::Rectangle(width, height) => width * height,
                Shape::Square { side } => side * side,
            }
        }
    }
    println!(
        "The area of the shape using impl function is: {}",
        shape.calc_area()
    );
    println!(
        "The area of the square shape using impl function is: {}",
        square_shape.calc_area()
    );
    println!(
        "The area of the circle shape using impl function is: {}",
        circle_shape.calc_area()
    );

    println!("End of match demo.");
}

fn main() {
    enums_demo();
    demo_match();
}
