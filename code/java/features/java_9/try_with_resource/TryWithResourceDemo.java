import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;

public class TryWithResourceDemo{
   public static void main(String[] args) throws IOException {
      System.out.println(readData("Try-With-Resource demo. resource will auto close after try clause"));
   } 

   static String readData(String message) throws IOException {
      Reader inputString = new StringReader(message);
      BufferedReader br = new BufferedReader(inputString);
      try (br) {
         return br.readLine();
      }
   }
}
