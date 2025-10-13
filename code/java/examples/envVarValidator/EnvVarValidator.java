import java.util.Scanner;

public class EnvVarValidator {

    public static int getAndValidateEnvVar(String varName, int minValue, int maxValue) throws IllegalArgumentException {
        System.out.println("Loading env var "+varName);
        String envValue = System.getenv(varName);
        System.out.println("value= "+envValue);
        
        if (envValue == null) {
            throw new IllegalArgumentException("Environment variable " + varName + " is not set.");
        }

        int numericValue;
        try {
            numericValue = Integer.parseInt(envValue);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Environment variable " + varName + " is not a valid integer.");
        }

        if (numericValue < minValue || numericValue > maxValue) {
            throw new IllegalArgumentException("Value of environment variable " + varName + " is not within the range [" + minValue + ", " + maxValue + "].");
        }

        return numericValue;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Please enter the name of the env var to load: ");
        String userInput = scanner.nextLine();
        final int minVal = 1;
        final int maxVal = 100;
        System.out.println("You entered: " + userInput);
        try {
            int value = getAndValidateEnvVar(userInput, minVal, maxVal);
            System.out.println(String.format("min val=%d, max val=%d, got %s", minVal, maxVal, userInput));
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}




