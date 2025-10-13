package datastructures;

public class GenericStack<T> {

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
