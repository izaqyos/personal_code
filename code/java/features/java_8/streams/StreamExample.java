import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collector;
import java.util.stream.Collectors;

public class StreamExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // Example 1: Filtering
        List<Integer> evenNumbers = numbers.stream()
                .filter(n -> n % 2 == 0)
                .collect(Collectors.toList());
        System.out.println("Even numbers: " + evenNumbers);

        // Example 2: Mapping
        List<String> squareStrings = numbers.stream()
                .map(n -> n * n)
                .map(Object::toString)
                .collect(Collectors.toList());
        System.out.println("Square strings: " + squareStrings);

        // Example 3: Reducing
        int sum = numbers.stream()
                .reduce(0, Integer::sum);
        System.out.println("Sum of numbers: " + sum);

        // Example 4: Sorting
        List<Integer> sortedNumbers = numbers.stream()
                .sorted((a, b) -> b.compareTo(a)) // Descending order
                .collect(Collectors.toList());
        System.out.println("Sorted numbers (descending): " + sortedNumbers);

        // Example 4: Sorting ascending
        List<Integer> sortedNumbersAsc = numbers.stream()
                .sorted((a, b) -> a.compareTo(b)) // Descending order
                .collect(Collectors.toList());
        System.out.println("Sorted numbers (ascending): " + sortedNumbersAsc);

        List<Integer> numbers2 = Arrays.asList(1, 2,2,2, 3, 4, 5, 6, 6,7, 8, 8,8, 9, 10);
        Set<Integer> uniqNumbers = numbers.stream()
                .collect(Collectors.toSet());
                System.out.println("Unique list of numbers is:");
                uniqNumbers.forEach( elem -> System.out.printf("%d, ", elem));
                System.out.println("");
    }
}
