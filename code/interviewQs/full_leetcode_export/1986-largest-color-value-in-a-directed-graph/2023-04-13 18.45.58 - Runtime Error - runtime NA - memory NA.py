class Solution:
    def getTotal(self, colors, path):
        from collections import defaultdict
        node_vals_dict = defaultdict(int)
        for n in path:
            node_vals_dict[colors[n]]+=1
        total = 0
        for v in node_vals_dict.values():
            total = max(v, total)
        return total


    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        visited = {n:0 for n in range(len(edges)+1)} #0 - not visited, 1 - explored, 2 - visited
        st = [] 
        max_total = -1

        for n in range(len(edges)):
            st.append((n, [n])) # append node and path
            #print(f"starting node {n}. visited {visited}")
            while st:
                cur, path = st.pop()
                #print(f"processing {cur}, path {path}")
                visited[cur] = 1 #set to being explored
                neighbors = [ y[1] for y in edges if y[0] == cur ]
                #print(f" neighbors {neighbors}")
                if not neighbors:
                    max_total = max(max_total, self.getTotal(colors, path)) 
                    #print(f"max_total {max_total}")
                    
                for neighbor in neighbors :
                    #print(f"checking neighbor {neighbor}")
                    if visited[neighbor]  == 1: #we double back to an already explored node => we have a cycle:
                        #print("cycle detected")
                        return -1
                    elif visited[neighbor]  == 0: #not explored
                        #print("exploring neighbor")
                        visited[neighbor] = 1
                        new_path = path[:]
                        new_path.append(neighbor)
                        st.append((neighbor, new_path ))
                    elif visited[neighbor]  == 2: #complete, do nothing (just put it as reference)
                        #print("already visited")
                        pass

                visited[cur] = 2 #mark as visited 
        return max_total
