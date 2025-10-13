
# Table of Contents

- [Day 1 — Two-Sum (hash map)](#day-1--two-sum-hash-map)
- [Day 2 — Rotate array in-place (3 reverses)](#day-2--rotate-array-in-place-3-reverses)
- [Day 3 — string_view splitter (no allocations)](#day-3--string_view-splitter-no-allocations)
- [Day 4 — Top-K frequent (heap or sort)](#day-4--top-k-frequent-heap-or-sort)
- [Day 5 — Sort groups by size (custom comparator)](#day-5--sort-groups-by-size-custom-comparator)
- [Day 6 — RAII scoped_timer](#day-6--raii-scoped_timer)
- [Day 7 — unique_ptr tree sum](#day-7--unique_ptr-tree-sum)
- [Day 8 — BFS shortest path (unweighted)](#day-8--bfs-shortest-path-unweighted)
- [Day 9 — Parse duration "1h30m15s"](#day-9--parse-duration-1h30m15s)
- [Day 10 — Generic join (templates + iterators)](#day-10--generic-join-templates--iterators)
- [Minimal Stubs + Asserts Template](#minimal-stubs--asserts-template)
- [How to use](#how-to-use)

---

 C++ Practice Plan (10–15 min per session)

```bash
# macOS (clang++)
alias cxx17='clang++ -std=c++17 -O2 -Wall -Wextra -Wpedantic'
# Debug with sanitizers:
alias cxxdbg='clang++ -std=c++17 -g -O0 -fsanitize=address,undefined -fno-omit-frame-pointer -Wall -Wextra -Wpedantic'
```

---

## Day 1 — Two-Sum (hash map)

**Goal:** Return indices of two numbers summing to `target`.
**API:** `std::pair<int,int> two_sum(const std::vector<int>& a, int target);`
**Hint:** `unordered_map<val, idx> m; m.reserve(a.size());`
**Quick test:** `two_sum({2,7,11,15}, 9) → (0,1)`.

done.
### tests
```bash
[i500695@FVN4RQW7J6:2025-08-24 16:29:13:~/work/code/CPP/practice/twosum]1187$ clang++ -std=c++17 -O2 -Wall -Wextra -Wpedantic twosum.cpp 
[i500695@FVN4RQW7J6:2025-08-24 16:30:17:~/work/code/CPP/practice/twosum]1188$ ./a.out 
--------------------------
Running basic test case...
Input array: [ 2 7 11 15 ]
Expecting (0, 1), got (0, 1)
test passed.
--------------------------
--------------------------
Running duplicates test case...
Input array: [ 3 3 ]
Expecting (1, 0), got (0, 1)
test passed.
--------------------------
--------------------------
Running mixed test case...
Input array: [ 3 2 4 ]
Expecting (2, 1), got (1, 2)
test passed.
--------------------------
--------------------------
Running negatives test case...
Input array: [ -5 10 -3 7 ]
Expecting (2, 3), got (2, 3)
test passed.
--------------------------
All tests passed.
```
### Code
```cpp
#include <iostream>
#include <vector>
#include <utility>
#include <unordered_map>


void print_vector(const std::vector<int>& v) {
    std::cout << "[ ";
    for (const auto& n : v) {
        std::cout << n << " ";
    }
    std::cout << "]\n";
}

void print_map(const std::unordered_map<int, int>& m) {
    std::cout << "{ ";
    for (const auto& kv : m) {
        std::cout << kv.first << ": " << kv.second << ", ";
    }
    std::cout << "}\n";
}

std::pair<int, int> two_sum(const std::vector<int>& nums, int target) {
    std::cout << "Input array: ";
    print_vector(nums);

    std::unordered_map<int, int> num_to_index;
    for (auto &n: nums) {
        // std::cout<< "checking " << n << "\n";
        if (num_to_index.find(n) != num_to_index.end()) {
            // std::cout << "found pair: " << n << " + " << target - n << " at indices: "<< num_to_index[n] << "," << &n - &nums[0] << "\n";
            return {num_to_index[n], &n - &nums[0]};
        }
        num_to_index[target - n] = &n - &nums[0];   
        // print_map(num_to_index);
    }
    return {-1, -1}; // Not found
}

inline void expect_eq(const std::pair<int, int>& expected, const std::pair<int, int>& actual, const char* msg) {
    std::cout<< "Expecting (" << expected.first << ", " << expected.second << "), got ("
              << actual.first << ", " << actual.second << ")\n";
    if ( expected == actual  || (expected.first == actual.second && expected.second == actual.first)) {
        std::cout << "test passed.\n";
    }
    else {
        std::cerr << "Expected (" << expected.first << ", " << expected.second << ") but got ("
                  << actual.first << ", " << actual.second << ")\n";
        throw std::runtime_error(msg);
    }
}

// ---------- Individual test cases ----------
static void test_basic() {
    std::cout<< "--------------------------\n";
    std::cout<< "Running basic test case...\n";
    std::vector<int> a{2,7,11,15};
    auto p = two_sum(a, 9);
    expect_eq(std::pair<int, int>{0,1} , p, "basic case wrong pair" );
    std::cout<< "--------------------------\n";
}

static void test_duplicates() {
    std::cout<< "--------------------------\n";
    std::cout<< "Running duplicates test case...\n";
    std::vector<int> a{3,3};
    auto p = two_sum(a, 6);
    expect_eq(std::pair<int, int>{1,0}, p, "duplicates wrong pair");
    std::cout<< "--------------------------\n";
}

static void test_mixed() {
    std::cout<< "--------------------------\n";
    std::cout<< "Running mixed test case...\n";
    std::vector<int> a{3,2,4};
    auto p = two_sum(a, 6);
    expect_eq(std::pair<int, int>{2,1}, p, "mixed case wrong pair");
    std::cout<< "--------------------------\n";
}

static void test_negatives() {
    std::cout<< "--------------------------\n";
    std::cout<< "Running negatives test case...\n";
    std::vector<int> a{-5, 10, -3, 7};
    auto p = two_sum(a, 4); // -3 + 7
    expect_eq(std::pair<int, int>{2,3}, p, "negatives case wrong pair");
    std::cout<< "--------------------------\n";
}

// ---------- Test driver ----------
static void test() {
    test_basic();
    test_duplicates();
    test_mixed();
    test_negatives();
}

int main() {
    try {
        test();
        std::cout << "All tests passed.\n";
        return 0;
    } catch (const std::exception& ex) {
        std::cerr << "Test failed: " << ex.what() << "\n";
    }
}
```
---

## Day 2 — Rotate array in-place (3 reverses)

**Goal:** Rotate right by `k`.
**API:** `void rotate(std::vector<int>& a, int k);`
**Hint:** `k%=n; reverse(all); reverse(first,k); reverse(k,end);` Handle `k<0`.

---

## Day 3 — `string_view` splitter (no allocations)

**Goal:** Split by a char, trim spaces.
**API:** `std::vector<std::string_view> split_trim(std::string_view s, char delim);`
**Focus:** `find`, `substr` on `string_view`, tiny `ltrim/rtrim`.

---

## Day 4 — Top-K frequent (heap or sort)

**Goal:** K most frequent ints, count desc then value asc.
**API:** `std::vector<std::pair<int,int>> topk(const std::vector<int>& a, int k);`
**Routes:** `unordered_map + sort` or `min-heap (priority_queue)`.

---

## Day 5 — Sort groups by size (custom comparator)

**Goal:** Sort `std::vector<std::vector<std::string>>` by **size desc**, then **first word asc (case-insensitive)**.
**API:** `void sort_groups(std::vector<std::vector<std::string>>& g);`

---

## Day 6 — RAII `scoped_timer`

**Goal:** Print elapsed ms on scope exit.
**API:**

```cpp
struct scoped_timer {
  std::string label;
  std::chrono::steady_clock::time_point t0;
  explicit scoped_timer(std::string lbl);
  ~scoped_timer(); // prints "<label>: X ms"
};
```

---

## Day 7 — `unique_ptr` tree sum

**Goal:** Sum node values in a binary tree.
**Types:**

```cpp
struct Node { int v; std::unique_ptr<Node> l,r; };
int sum(const Node* n); // recursive
```

**Focus:** ownership; pass raw pointer for read-only traversal.

---

## Day 8 — BFS shortest path (unweighted)

**Goal:** Distance from `s` to all nodes.
**API:** `std::vector<int> bfs(const std::vector<std::vector<int>>& g, int s);`
**Use:** queue; `INT_MAX` for “INF”.

---

## Day 9 — Parse duration `"1h30m15s"`

**Goal:** Return total seconds.
**API:** `long parse_duration(std::string_view s);`
**Hint:** scan digits → unit (`h/m/s`), accumulate; accept spaces/uppercase.

---

## Day 10 — Generic `join` (templates + iterators)

**Goal:** Join a range into a string with delimiter.
**API:**

```cpp
template <typename It>
std::string join(It first, It last, std::string_view delim);
```

---

## Minimal Stubs + Asserts Template

Paste into `main.cpp`, uncomment the block for today’s task, implement until you see **OK**.

```cpp
#include <bits/stdc++.h>
using namespace std;

// === Implement today's functions here ===

// --- Tiny assert helper ---
#define REQ(cond) do{ if(!(cond)){ cerr<<"Fail: "<<__LINE__<<"\n"; exit(1);} }while(0)

int main() {
  // Day 1:
  // auto p = two_sum({2,7,11,15}, 9);
  // REQ( (p == pair{0,1} || p == pair{1,0}) );

  // Day 2:
  // vector<int> v{1,2,3,4,5}; rotate(v, 2);
  // REQ((v==vector<int>{4,5,1,2,3}));

  // Day 3:
  // auto parts = split_trim(" a, bb , c ", ',');
  // REQ(parts.size()==3 && parts[1]=="bb");

  // Day 4:
  // auto k = topk({1,1,2,3,3,3,2}, 2);
  // REQ(k[0].first==3 && k[0].second==3);

  // Day 5:
  // vector<vector<string>> g{{"b"},{"a","A"},{"c","C","cc"}};
  // sort_groups(g); REQ(g[0].size()==3);

  // Day 6:
  // { scoped_timer t("work"); this_thread::sleep_for(10ms); }

  // Day 7:
  // auto root = make_unique<Node>(
  //   Node{1, make_unique<Node>(Node{2}), make_unique<Node>(Node{3})});
  // REQ(sum(root.get())==6);

  // Day 8:
  // vector<vector<int>> G{{1,2},{0,3},{0,3},{1,2}};
  // auto d = bfs(G,0); REQ(d[3]==2);

  // Day 9:
  // REQ(parse_duration("1h30m15s")==5415);
  // REQ(parse_duration("45s")==45);

  // Day 10:
  // vector<int> x{1,2,3};
  // REQ(join(begin(x),end(x),",")=="1,2,3");

  cout<<"OK\n";
}
```

### Compile & Run

```bash
cxxdbg main.cpp && ./a.out
```

---

### How to use

* Do **one session per day**.
* If you finish early, add a quick stretch: edge cases, second approach (e.g., heap vs sort), or API polish (`std::span`, `std::string_view`).
