class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_list = [None] * num_vertices

    def add_edge(self, source, destination):
        new_node = Node(destination)
        new_node.next = self.adj_list[source]
        self.adj_list[source] = new_node

        # For undirected graphs, add the reverse edge as well
        new_node = Node(source)
        new_node.next = self.adj_list[destination]
        self.adj_list[destination] = new_node

    def print_graph(self):
        for i in range(self.num_vertices):
            temp = self.adj_list[i]
            print(f"Adjacency list of vertex {i}:", end="")
            while temp:
                print(f" -> {temp.data}", end="")
                temp = temp.next
            print()

# Example usage:
graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(0, 4)
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 3)
graph.add_edge(3, 4)

graph.print_graph()
