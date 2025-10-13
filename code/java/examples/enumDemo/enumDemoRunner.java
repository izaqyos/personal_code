package enumDemo;

import enumDemo.Animals;

class enumDemoRunner {

public static void main(String[] args) {
    System.out.println("JAVA enum demo");

    Animals dog = Animals.DOG;
    if (dog == Animals.DOG) {
        print("This is a dog");
    }
}
}