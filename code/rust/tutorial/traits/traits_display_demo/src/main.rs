use std::fmt::{self, Display, Formatter};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Suit { Clubs, Diamonds, Hearts, Spades }

impl Display for Suit {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let s = match self {
            Suit::Clubs    => "♣",
            Suit::Diamonds => "♦",
            Suit::Hearts   => "♥",
            Suit::Spades   => "♠",
        };
        f.write_str(s)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Card { rank: u8, suit: Suit }

impl Display for Card {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        // Support an alternate form with {:#} for a verbose rendering.
        if f.alternate() {
            let rank_name = match self.rank {
                1  => "Ace".to_string(),
                11 => "Jack".to_string(),
                12 => "Queen".to_string(),
                13 => "King".to_string(),
                n @ 2..=10 => n.to_string(),
                _ => "?".into(),
            };
            // Use Debug for the suit name (Spades, Hearts, …)
            return write!(f, "{} of {:?}", rank_name, self.suit);
        }

        // Default compact form like "A♠", "10♥"
        let rank = match self.rank {
            1  => "A".into(),
            11 => "J".into(),
            12 => "Q".into(),
            13 => "K".into(),
            n @ 2..=10 => n.to_string(),
            _ => "?".into(),
        };
        write!(f, "{}{}", rank, self.suit)
    }
}

fn main() {
    let a_spades = Card { rank: 1,  suit: Suit::Spades };
    let ten_hearts = Card { rank: 10, suit: Suit::Hearts };

    // Debug vs Display
    println!("Debug:   {:?}", a_spades);    // Card { rank: 1, suit: Spades }
    println!("Display: {}",  a_spades);     // A♠

    // Alternate form with {:#}
    println!("Verbose: {:#}", a_spades);    // Ace of Spades

    // to_string() uses Display
    let s = ten_hearts.to_string();
    println!("String:  {}", s);             // 10♥

    // Works seamlessly in format strings
    println!("Hand: {}, {}", a_spades, ten_hearts);
}
