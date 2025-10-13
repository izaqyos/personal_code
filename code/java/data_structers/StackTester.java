package datastructures;

public class StackTester {

    public static void testPushPop(GenericStack<String> stack) {
        stack.push("Test1");
        stack.push("Test2");

        String topElement = stack.peek();
        if (!topElement.equals("Test2")) {
            throw new AssertionError("Peek failed!");
        }

        String poppedElement = stack.pop();
        if (!poppedElement.equals("Test2")) {
            throw new AssertionError("Pop failed!");
        }
    }

    public static void testIsEmpty(GenericStack<Object> stack) {
        if (!stack.isEmpty()) {
            throw new AssertionError("isEmpty failed on empty stack!");
        }

        stack.push(new Object());
        if (stack.isEmpty()) {
            throw new AssertionError("isEmpty failed on non-empty stack!");
        }
    }

    public static void main(String[] args) {
        GenericStack<Integer> intStack = new GenericStack<>();
        testPushPop(intStack); // Test push and pop operations
        testIsEmpty(intStack); // Test isEmpty method

        System.out.println("All tests passed!");
    }
}
