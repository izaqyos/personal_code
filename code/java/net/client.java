import java.net.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class client {

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("The client requires file name as parameter");
            return;
        }
        String filename = args[0];
        String hostname="localhost";
        String fileContent=""; 

        int port = 2222;
        System.out.printf("This is a TCP client that sends content of a file to %s:%d", hostname, port);

        try {
            fileContent = new String( Files.readAllBytes(Paths.get(filename)));
            fileContent += "\n\n\n";
        } catch(IOException e){
            e.printStackTrace();
        }

      try (AsynchronousSocketChannel client =
            AsynchronousSocketChannel.open()) {
         Future<Void> result = client.connect(
         new InetSocketAddress(hostname, port));
         result.get();
         ByteBuffer buffer = ByteBuffer.wrap(fileContent.getBytes());
         Future<Integer> writeval = client.write(buffer);
         System.out.println("Writing to server: "+fileContent);
         writeval.get();
         buffer.flip();


         ByteBuffer rbuffer = ByteBuffer.allocate((int) Math.pow(2,20));
         Future<Integer> readval = client.read(rbuffer);
          readval.get();
         System.out.println("Received from server: "
            +new String(rbuffer.array()).trim());
         buffer.clear();
      }
      catch (ExecutionException | IOException e) {
         e.printStackTrace();
      }
      catch (InterruptedException e) {
         System.out.println("Disconnected from the server.");
      }

    }
    
}
