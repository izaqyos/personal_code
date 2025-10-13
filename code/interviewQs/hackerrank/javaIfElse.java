import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;
/*
   Given an integer, , perform the following conditional actions:
If  is odd, print Weird
If  is even and in the inclusive range of  to , print Not Weird
If  is even and in the inclusive range of  to , print Weird
If  is even and greater than , print Not Weird
Complete the stub code provided in your editor to print whether or not  is weird.
Input Format
A single line containing a positive integer, .
Constraints

Output Format
Print Weird if the number is weird; otherwise, print Not Weird.
Sample Input 0
3
Sample Output 0
Weird
Sample Input 1
24
Sample Output 1
Not Weird
Explanation
Sample Case 0:
 is odd and odd numbers are weird, so we print Weird.
Sample Case 1:
 and  is even, so it isn't weird. Thus, we print Not Weird.
 */

public class javaIfElse {



    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        int N = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
        if (N%2 == 1) {
            System.out.printf("Number %d is Weird\n", N); 
        }
        else {
            if ((N>=6) && (N<=20)){
            System.out.printf("Number %d is Not Weird\n", N); 
            }
            else {
            System.out.printf("Number %d is Weird\n", N); 
        }
        }

        scanner.close();
    }
}
