import java.util.Base64;

public class Base64Demo {
    public static void main(String[] args) {
        String text = "base64 demo";
        byte[] encoded_text = Base64.getEncoder().encode(text.getBytes());
        System.out.printf("Text: %s, encode: %s\n", text, encoded_text);
        byte[] decoded_text = Base64.getDecoder().decode(encoded_text);
        System.out.printf("Decoded Text: %s\n", text, decoded_text);
    }
}