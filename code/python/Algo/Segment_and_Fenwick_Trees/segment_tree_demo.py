class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)  # Initialize with sufficient space
        self.build(arr, 1, 0, self.n - 1)

    def build(self, arr, v, tl, tr):
        if tl == tr:
            self.tree[v] = arr[tl]
        else:
            tm = (tl + tr) // 2
            self.build(arr, 2 * v, tl, tm)
            self.build(arr, 2 * v + 1, tm + 1, tr)
            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.tree[v]
        tm = (tl + tr) // 2
        return self.query(2 * v, tl, tm, l, min(r, tm)) + self.query(2 * v + 1, tm + 1, tr, max(l, tm + 1), r)

    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.tree[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(2 * v, tl, tm, pos, new_val)
            else:
                self.update(2 * v + 1, tm + 1, tr, pos, new_val)
            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

# Example usage
arr = [1, 3, 5, 7, 9, 11]
segment_tree = SegmentTree(arr)
print(segment_tree.query(1, 0, len(arr) - 1, 1, 3))  # Output: 15 (3 + 5 + 7)
segment_tree.update(1, 0, len(arr) - 1, 2, 10)  # Update the 3rd element to 10
print(segment_tree.query(1, 0, len(arr) - 1, 1, 3))  # Output: 20 (3 + 10 + 7)a
