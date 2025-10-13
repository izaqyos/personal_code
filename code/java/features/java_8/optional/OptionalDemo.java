import java.util.Optional;

public class OptionalDemo{ 
 
   public static void main(String[] args) { 
        String[] str = new String[10]; 
        Optional<String> checkNull =
                       Optional.ofNullable(str[5]); 
        if (checkNull.isPresent()) { 
            String word = str[5].toLowerCase(); 
            System.out.print(str); 
         } else
           System.out.println("string is null"); 

          String nullVal = null;
          Optional<String> optionalStrWithNull = Optional.ofNullable(nullVal);

          if (optionalStrWithNull.isPresent()) {
            System.out.println("found non null value");
          }
          else {
            System.out.println("found null value");
          }
    } 
}