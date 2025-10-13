type Kilograms = i32;
fn main() {
    println!("Type alias demo, for this demo will alias int 32 to Kilograms");
    let weight1: Kilograms = 70;
    let weight2: Kilograms = 80;
    let _unused_var_no_warning: Kilograms = 90;
    #[allow(unused_variables)]
    let unused_var_use_compiler_directive_to_allow: Kilograms = 100;
    let total_weight = weight1 + weight2;
    println!("Total weight: {} kg", total_weight);
}
