"""
generic topological sort
"""

from collections import defaultdict

class Graph:
    def __init__(self):
        self.G = defaultdict(list)

    def addVert(self, v1):
        self.G[v1] = []

    def addEdge(self, v1, v2):
        self.G[v1].append(v2)
    
    def remEdge(self, v1,v2):
        if v1 in G:
            G[v1].remove[v2]

    def remVert(self, v1):
        if v1 in G:
            del G[v1]

    def isVinGraph(self,v):
        return v in self.G

    def getNeighbors(self,v):
        return self.G[v]

    def getNodes(self):
        return self.G.keys()

    def __str__(self):
        return self.G.__str__()

def topsort(G):
    """
    G is a dictionary of vertices. each has a list of neighbors.
    r is the root/starting node
    use 2 stacks. the normal dfs one and a top sort stack.
    now during DFS traversal we will use the dfs stack to also store the
    topological sort path
    For this we will push a marker for each parent so that when we pop it after processing
    all its childs we can push it to top sort stack.
    since I use positive integers for V the marker will be push -1*V.
    otherwize change the dfs stack to push/pop pairs of (V, isParent) instead of -1*V
    """
    from collections import deque

    print('topsort. got graph ', G)
    topsortRes = deque()

    visited = {v: False for v in G.getNodes() }
    #print('topsort. init visited ', visited)
    for v in G.getNodes():
        if visited[v]:
            continue

        dfsStack = deque()
        dfsStack.append(v)
        while not len(dfsStack) == 0:
            current = dfsStack.pop()
            if current < 0: #parent node was poped after all its childs were visited
                topsortRes.append(-1*current)
            else:
                dfsStack.append(-1*current)
                for u in G.getNeighbors(current):
                    if not visited[u]:
                        visited[u] = True
                        dfsStack.append(u)
    
    return [ topsortRes.pop() for x in range(len(topsortRes))]
        
def constructDemoGraph():
    """
    
    image: /Users/i500695/work/code/python/Algo/graph/demoGraph.dot.png
    i500695@C02X632CJGH6:2020-07-30 13:29:47:~/work/code/python/Algo/graph:]2016$ cat demoGraph.dot 
digraph d {
 1  [label="1 " fillcolor=red shape=circle fontcolor=blue]
 2  [label="3 " fillcolor=red shape=circle fontcolor=blue]
 3  [label="3 " fillcolor=red shape=circle fontcolor=blue]
 4  [label="4 " fillcolor=red shape=circle fontcolor=blue]
 5  [label="5 " fillcolor=red shape=circle fontcolor=blue]
 6  [label="6 " fillcolor=red shape=circle fontcolor=blue]
 7  [label="7 " fillcolor=red shape=circle fontcolor=blue]
 8  [label="8 " fillcolor=red shape=circle fontcolor=blue]
 9  [label="9 " fillcolor=red shape=circle fontcolor=blue]
 10 [label="10" fillcolor=red shape=circle fontcolor=blue]
 11 [label="11" fillcolor=red shape=circle fontcolor=blue]
 12 [label="12" fillcolor=red shape=circle fontcolor=blue]
 1 -> {2} [label="contextId"] 
 1 -> {3} [label="contextId"] 
 2 -> {4} [label="contextId"] 
 3 -> {4} [label="contextId"] 
 4 -> {5} [label="contextId"] 
 6 -> {7} [label="contextId"] 
 7 -> {8} [label="contextId"] 
 9 -> {8} [label="contextId"] 
 10 -> {11} [label="contextId"] 
}
generate image: 
$ dot -T png -O demoGraph.dot  && open demoGraph.dot.png
    """
    G = Graph()
    G.addEdge(1,2)
    G.addEdge(1,3)
    G.addEdge(2,4)
    G.addEdge(3,4)
    G.addEdge(4,5)
    G.addEdge(6,7)
    G.addEdge(7,8)
    G.addEdge(9,8)
    G.addEdge(10,11)
    G.addVert(12)
    G.addVert(5)
    G.addVert(8)
    G.addVert(11)

    return G

def test():
    G = constructDemoGraph()
    print('using graph ', G)
    sorted = topsort(G)
    print('sort: ', sorted)

    

if __name__ == '__main__':
    test()