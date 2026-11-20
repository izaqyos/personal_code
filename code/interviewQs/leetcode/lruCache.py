"""
LC 146. LRU Cache (Medium)

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
    LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
    int get(int key) Return the value of the key if the key exists, otherwise return -1.
    void put(int key, int value) Update the value of the key if the key exists. Otherwise,
        add the key-value pair to the cache. If the number of keys exceeds the capacity from
        this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Example 1:
    Input
    ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output
    [null, null, null, 1, null, -1, null, -1, 3, 4]

    Explanation
    LRUCache lRUCache = new LRUCache(2);
    lRUCache.put(1, 1); // cache is {1=1}
    lRUCache.put(2, 2); // cache is {1=1, 2=2}
    lRUCache.get(1);    // return 1
    lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    lRUCache.get(2);    // returns -1 (not found)
    lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    lRUCache.get(1);    // return -1 (not found)
    lRUCache.get(3);    // return 3
    lRUCache.get(4);    // return 4

Constraints:
    1 <= capacity <= 3000
    0 <= key <= 10^4
    0 <= value <= 10^5
    At most 2 * 10^5 calls will be made to get and put.

Interview rule: no OrderedDict (the interviewer's usual follow-up). Hash map + your own structure.
"""

"""
# Tip 2 self: Dummy Sentinels (head <-> [real nodes] <-> tail)
Initialize permanent dummy `head` and `tail` nodes pointing to each other. 
Because every real node sits strictly between them, `prev` and `next` are NEVER None. 
Zero null-checks, zero branch edge-cases:

def _remove(self, n: Node):
    n._prev._next, n._next._prev = n._next, n._prev

def _insert_front(self, n: Node):
    n._next, n._prev = self._head._next, self._head
    self._head._next._prev = self._head._next = n

# make_head(n) = _remove(n) + _insert_front(n)
# evict_lru()  = _remove(self._tail._prev)

b/c took me carefull debugging to spot all tail/head/None edgecases 
"""

class Node:
    def __init__(self, key: int, val: int):
        self._key: int = key  # cache key
        self._val: int = val  # cache val
        self._next: Node = None
        self._prev: Node = None

class LRUCache:
    def __init__(self, capacity: int):
        self._head: Node = None 
        self._tail: Node = None
        self._cap: int = capacity
        self._cache: dict = {} # k:ptr

    def make_head(self, node_ptr: Node):
        # first unlink node
        if node_ptr and node_ptr != self._head:
           if node_ptr._next:
               node_ptr._next._prev = node_ptr._prev 
           if node_ptr._prev: #just 2 b safe, since no head will always be valid  
                node_ptr._prev._next = node_ptr._next
           if node_ptr == self._tail:
                self._tail = node_ptr._prev
           node_ptr._prev = None
           node_ptr._next = self._head
           self._head._prev = node_ptr
           self._head = node_ptr

    def get(self, key: int) -> int:
        if key in self._cache:
            self.make_head(self._cache[key])
            return self._cache[key]._val
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self._cache:
            # update branch
            node_ptr: Node = self._cache[key]
            node_ptr._val = value
            self.make_head(node_ptr)
            
        else: #new key branch
            new_node = Node(key, value)
            new_node._next = self._head
            if self._head:
                self._head._prev = new_node
            new_node._prev = None
            self._head = new_node
            if self._tail == None:
                self._tail = self._head
            else:
                self._tail._next = None
            self._cache[key] = new_node

            #evict lru
            if len(self._cache) > self._cap:
                lru_key = self._tail._key
                if self._tail and self._tail._prev:
                    self._tail._prev._next = None 
                    self._tail = self._tail._prev
                del self._cache[lru_key]


def run(ops, args):
    out = []
    cache = None
    for op, a in zip(ops, args):
        if op == "LRUCache":
            cache = LRUCache(*a)
            out.append(None)
        elif op == "get":
            out.append(cache.get(*a))
        else:
            out.append(cache.put(*a))
    return out


if __name__ == "__main__":
    cases = [
        (["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
         [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
         [None, None, None, 1, None, -1, None, -1, 3, 4], "example 1"),
        (["LRUCache", "put", "get", "put", "get", "get"],
         [[1], [2, 1], [2], [3, 2], [2], [3]],
         [None, None, 1, None, -1, 2], "capacity 1"),
        (["LRUCache", "put", "put", "put", "put", "get", "get"],
         [[2], [2, 1], [1, 1], [2, 3], [4, 1], [1], [2]],
         [None, None, None, None, None, -1, 3], "update refreshes recency"),
        (["LRUCache", "put", "put", "get", "put", "get", "get"],
         [[2], [1, 1], [2, 2], [1], [3, 3], [1], [2]],
         [None, None, None, 1, None, 1, -1], "get refreshes recency"),
        (["LRUCache", "get", "put", "get"],
         [[1], [5], [5, 0], [5]],
         [None, -1, None, 0], "miss on empty, value 0 is a hit"),
    ]
    passed = 0
    for ops, args, exp, label in cases:
        got = run(ops, args)
        assert got == exp, f"FAIL [{label}]: expected {exp}, got {got}"
        passed += 1

    # randomized check against a simple reference
    import random
    random.seed(146)
    for t in range(300):
        cap = random.randint(1, 5)
        c, ref = LRUCache(cap), []  # ref: list of [key, value], most recent last
        for _ in range(60):
            k = random.randint(0, 7)
            if random.random() < 0.5:
                idx = next((i for i, kv in enumerate(ref) if kv[0] == k), None)
                exp = -1 if idx is None else ref[idx][1]
                if idx is not None:
                    ref.append(ref.pop(idx))
                got = c.get(k)
                assert got == exp, f"FAIL random #{t}: get({k}) = {got}, expected {exp}"
            else:
                v = random.randint(0, 9)
                ref = [kv for kv in ref if kv[0] != k] + [[k, v]]
                if len(ref) > cap:
                    ref.pop(0)
                c.put(k, v)
        passed += 1
    print(f"All {passed} tests passed")
