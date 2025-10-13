import java.io.PrintWriter;
import java.io.StringWriter;

public class ExceptionDemo {
    public static void main(String[] args) {
        try {
            int result = 1 / 0; // This will throw an ArithmeticException
        } catch (Exception e) {
            // Print the exception stack trace to the console
            e.printStackTrace();
            System.out.println("Exception: "+ e);

            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
            String exceptionStackTrace = sw.toString();
            System.out.println("Exception with stack trace: "+ exceptionStackTrace);
        }
    }
}
