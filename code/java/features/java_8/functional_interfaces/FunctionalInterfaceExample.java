// Define a functional interface with a single abstract method
@FunctionalInterface
interface Calculator {
    double calculate(double num1, double num2);
}

public class FunctionalInterfaceExample {
    public static void main(String[] args) {
        // Using a lambda expression to implement the Calculator functional interface
        Calculator addition = (a, b) -> a + b;
        Calculator subtraction = (a, b) -> a - b;
        Calculator multiplication = (a, b) -> a * b;
        Calculator division = (a, b) -> {
            if (b == 0) {
                throw new ArithmeticException("Division by zero is not allowed");
            }
            return a / b;
        };
        Calculator exponent = (a, b) -> {
            double ret = 1;
            if (b==0) {
                ret = 1;
            }
            else if (b >0) {
                ret = 1;
                for (int i = 0; i < b; i++) {
                    ret *= a;
                }
            }
            else {
                ret = 1;
                for (int i = 0; i < -b; i++) {
                    ret *= a;
                }
                ret = 1/a;
            }
            return ret;
        };

        // Using the functional interfaces to perform calculations
        double result1 = addition.calculate(10, 5);
        double result2 = subtraction.calculate(10, 5);
        double result3 = multiplication.calculate(10, 5);
        double result4 = division.calculate(10, 5);
        double result5 = exponent.calculate(10, 5);
        double result6 = exponent.calculate(3, 0);
        double result7 = exponent.calculate(2, -2);

        System.out.println("Addition: " + result1);
        System.out.println("Subtraction: " + result2);
        System.out.println("Multiplication: " + result3);
        System.out.println("Division: " + result4);
        System.out.println("Exponent: " + result5);
        System.out.println("Exponent: " + result6);
        System.out.println("Exponent: " + result7);
    }
}
