interface MyInterface {
    // Abstract method (no implementation required)
    void regularMethod();

    // Default method with implementation
    default void defaultMethod() {
        System.out.println("This is a default method.");
    }

    // Static method with implementation
    static void staticMethod() {
        System.out.println("This is a static method.");
    }
}

// Implement the interface in a class
class MyClass implements MyInterface {
    @Override
    public void regularMethod() {
        System.out.println("This is the regular method implementation.");
    }
}

// // Implement the interface in a class
// // uncomment will yeild error: InterfaceExample.java:25: error: MyClass2 is not abstract and does not override abstract method regularMethod() in MyInterface
// class MyClass2 implements MyInterface {
// }

public class InterfaceExample {
    public static void main(String[] args) {
        MyClass myClass = new MyClass();
        //MyClass2 myClass2 = new MyClass2();

        System.out.println("calling myClass methods:");
        // Calling regularMethod from the implemented class
        myClass.regularMethod();

        // Calling defaultMethod from the interface
        myClass.defaultMethod();

        // Calling staticMethod from the interface
        MyInterface.staticMethod();

        // System.out.println("calling myClass2 methods:");
        // myClass2.regularMethod();
        // myClass2.defaultMethod();
        // myClass2.staticMethod();
    }
}
