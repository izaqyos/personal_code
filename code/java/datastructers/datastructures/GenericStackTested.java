public class GenericStackTested {

    public static class GenericStack<T> {

        private static class Node<T> {
            private T data;
            private Node<T> next;

            public Node(T data) {
                this.data = data;
            }
        }

        private Node<T> top;

        public GenericStack() {
            this.top = null;
        }

        public boolean isEmpty() {
            return top == null;
        }

        public void push(T item) {
            Node<T> newNode = new Node<>(item);
            newNode.next = top;
            top = newNode;
        }

        public T peek() {
            if (isEmpty()) {
                throw new RuntimeException();
            }
            return top.data;
        }

        public T pop() {
            if (isEmpty()) {
                throw new RuntimeException();
            }
            T data = top.data;
            top = top.next;
            return data;
        }
    }

    public static void testPushPop(GenericStack<String> stack) {
        stack.push("Test1");
        stack.push("Test2");

        String topElement = stack.peek();
        System.out.println("Stack topElement: "+topElement);
        if (!topElement.equals("Test2")) {
            throw new AssertionError("Peek failed!");
        }

        String poppedElement = stack.pop();
        if (!poppedElement.equals("Test2")) {
            throw new AssertionError("Pop failed!");
        }
    }

    public static void testEmpty(GenericStack<String> stack) {
        if (!stack.isEmpty()) {
            throw new AssertionError("stack not empty");
        }
    }

    public static void testNotEmpty(GenericStack<String> stack) {
        if (stack.isEmpty()) {
            throw new AssertionError("isEmpty failed on empty stack!");
        }
    }

    public static void main(String[] args) {
        GenericStack<String> myStack = new GenericStack<>();
        testPushPop(myStack); // Test push and pop operations
        testNotEmpty(myStack); // Test isEmpty method
        myStack.pop();
        testEmpty(myStack);

        System.out.println("All tests passed!");
    }
}
