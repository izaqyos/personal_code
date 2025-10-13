import java.time.*;
import java.time.format.DateTimeFormatter;

public class DateTimeExample {
    public static void main(String[] args) {
        // Getting the current date and time
        LocalDateTime now = LocalDateTime.now();
        System.out.println("Current Date and Time: " + now);

        // Creating a specific date and time
        LocalDate date = LocalDate.of(2023, Month.SEPTEMBER, 11); //the day this demo was created...
        LocalTime time = LocalTime.of(18, 37);
        LocalDateTime dateTime = LocalDateTime.of(date, time);
        System.out.println("Demo Creation Specific Date and Time: " + dateTime);

        // Formatting date and time
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formattedDateTime = dateTime.format(formatter);
        System.out.println("Formatted Date and Time: " + formattedDateTime);

        // Adding and subtracting time
        LocalDateTime futureDateTime = dateTime.plusYears(1).plusDays(7).minusHours(2);
        System.out.println("Future Date and Time: " + futureDateTime);

        // Duration between two times
        Duration duration = Duration.between(dateTime, futureDateTime);
        System.out.println("Duration: " + duration.toDays() + " days");
        System.out.println("Duration: " + duration.toHours() + " hours");
        System.out.println("Duration: " + duration.toSeconds() + " seconds");
        System.out.println("Duration: " + duration.toMillis() + " milliseconds");

        // Working with time zones
        ZoneId newYorkZone = ZoneId.of("America/New_York");
        ZonedDateTime newYorkTime = ZonedDateTime.of(dateTime, newYorkZone);
        System.out.println("New York Time: " + newYorkTime);

        // Checking for leap years
        boolean isLeapYear = Year.of(2024).isLeap();
        System.out.println("Is 2024 a leap year? " + isLeapYear);
    }
}
