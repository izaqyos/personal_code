def astar(start_node, end_node):
    open_set = set(start_node)
    closed_set = set()
    g = dict() #g(v) = v distance from start_node
    parents = dict() #adjacency map
    g[start_node] = 0 # dist(start_node) from start_node = 0
    parents[start_node] = start_node # start_node is root so it is set to be it's own parent

    while open_set: #in boolean context true iff set not empty, open_set is possible expansion nodes, when empty no way to expand further
        print(f"open_set is {open_set}")
        cur = None
        for v in open_set:
            print(f"{cur}")
            if cur == None or g[v]+heuristic(v)<g[cur]+heuristic(cur):
                cur=v
                print(f"Changing  cur to {cur}")
        if cur == end_node or Graph_nodes[cur] == None:
            pass
        else:
            for (m,weight) in get_neighbors(cur):
                print(f"exploring {cur} neighbor node {m} with weight {weight}")
                if m not in open_set and m not in closed_set:
                    print(f"adding {m} to open_set")
                    open_set.add(m)
                    parents[m] = cur
                    g[m] =g[cur] + weight #remember g(v) true distance from start_node
                else:
                    #if not m in g:
                    #    g[m] = float('inf')
                    print(f"distance of {m} from {start_node} is {g[m]}. distance via {cur} is {g[cur] + weight}")
                    if g[m] > g[cur] + weight:
                        g[m] = g[cur] +weight #we found a shorter distance to m, via cur so update m distance
                        parents[m] = cur
                        if m in closed_set: #since we found a shorter path via m, remove from close and add to open
                            closed_set.remove(m)
                            open_set.add(m)

        if cur == None:
            print(f"no path from {start_node} to {end_node}")
            return None

        if cur == end_node: #path found to end_node now reconstruct path
            path=[]
            while parents[cur] != cur:
                path.append(cur)
                cur = parents[cur]
            path.append(start_node)
            path.reverse()
            print(f"Path is: {path}")
            return path

        #we have added all of cur (current node under inspection) to open_set, updated their parents and distance and returned them to open_set if needed
        #so we can add cur to closed_set
        open_set.remove(cur)
        closed_set.add(cur)


#define fuction to return neighbor and its distance
#from the passed node
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None


#for simplicity we ll consider heuristic distances given
#and this function returns heuristic distance for all nodes
def heuristic(n):
    H_dist = {
        'A': 11,
        'B': 6,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }
    return H_dist[n]

##Describe your graph here
#Graph_nodes = {
#    'A': [('B', 6), ('F', 3)],
#    'B': [('A', 6), ('C', 3), ('D', 2)],
#    'C': [('B', 3), ('D', 1), ('E', 5)],
#    'D': [('B', 2), ('C', 1), ('E', 8)],
#    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
#    'F': [('A', 3), ('G', 1), ('H', 7)],
#    'G': [('F', 1), ('I', 3)],
#    'H': [('F', 7), ('I', 2)],
#    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
#}

Graph_nodes = {
    'A': [('B', 2), ('E', 3)],
    'B': [('A', 2), ('C', 1), ('G', 9)],
    'C': [('B', 1)],
    'D': [('E', 6), ('G', 1)],
    'E': [('A', 3), ('D', 6)],
    'G': [('B', 9), ('D', 1)]
}
def test():
    astar('A', 'G')

if __name__ == "__main__":
    test()

