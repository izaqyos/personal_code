fn main() {
    println!("Demo scoping principal. inner capture outer, not vice versa");
    let outer_var = "I'm an outer variable";
    let inner_var = "I'm an inner variable, declared in outer scope";
    {
        let inner_var = "I'm an inner variable, declared in inner scope";
        println!("Inner scope: outer_var = {}, inner_var = {}", outer_var, inner_var);
        {
            let inner_2nd_var = "I'm a second inner variable, declared in inner inner scope";
            println!("Second level inner scope: outer_var = {}, inner_var = {}, inner_2nd_var = {}", outer_var, inner_var, inner_2nd_var);
        }
        // next line will give: error[E0425]: cannot find value `inner_2nd_var` in this scope
        // print!("Trying to access an inner var in outer scope will fail, inner_2nd_var = {inner_2nd_var} ");
    }
    println!("Outer scope: outer_var = {}, inner_var = {}", outer_var, inner_var);
}
