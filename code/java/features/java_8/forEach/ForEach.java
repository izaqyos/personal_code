import java.util.ArrayList;
import java.util.List;

/**
 * ForEach
 */
public class ForEach {

        public static void main(String[] args) {
            List<String> myList = new ArrayList<String>();
            myList.add("Deby");
            myList.add("May");
            myList.add("Itay");
            myList.add("Kay");
            myList.add("Aimy");
            System.out.println("Family members names");
            myList.forEach(name -> System.out.println(name));
            System.out.println("Family members upper case");
            myList.forEach((name) -> System.out.println(name.toUpperCase()));
        }
}