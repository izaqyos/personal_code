import java.io.IOException;
//import java.nio.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;


public class RecursiveReadFiles {
    static void readFilesDFS(Path root) {
        try (Stream<Path> files = Files.list(root)) {
            files.forEach(filePath -> {
                if (Files.isRegularFile(filePath)) {
                    System.out.println("Content of "+filePath);
                    try {
                    Files.lines(filePath).forEach(line -> {
                        System.out.println(line);
                    });
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                else {
                    System.out.println("DFSing into "+filePath);
                }
            }
            );
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) throws IOException {
       Path cwd = Paths.get(System.getProperty("user.dir"));
       Path cwd_parent = cwd.getParent();

       if (cwd_parent!=null) {
        System.out.println("Recursive read all files in "+cwd_parent);
        readFilesDFS(cwd_parent);
       }
    }
}