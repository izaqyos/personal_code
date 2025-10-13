#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

// ---------- API ----------
// Rotate array to the RIGHT by k, in place.
// Use the "three reverses" method.
// Handle k < 0 (i.e., left rotation), and any |k| >= n.
void rotate(std::vector<int>& a, int k) {
    /*
    in my python solution I used the gcd method to calculate number of cycles
    then in inner loop I swapped elements in place for each cycle
    in this cpp solution I will use the three-reverses method
    works b/c lets say A =XY where X is first n-k elements and Y is last k elements
    then reversing A gives us Y'X' (where ' means reversed)
    then reversing first k elements gives us YX'
    then reversing last n-k elements gives us YX which is the desired result
    */
    if (a.empty()) return;
    unsigned int n = a.size();
    k = k % n;
    if (k == 0) return;
    if (k < 0) k += n; // normalize left rotation to right rotation

    std::reverse(a.begin(), a.end());
    std::reverse(a.begin(), a.begin() + k);
    std::reverse(a.begin()+k, a.end());
}

// ---------- Minimal test utilities (no macros) ----------
static void expect(bool cond, const char* msg) {
    if (!cond) throw std::runtime_error(msg);
}

static void expect_eq_vec(const std::vector<int>& expected,
                          const std::vector<int>& actual,
                          const char* msg) {
    if (expected != actual) {
        std::cerr << msg << "\nExpected: [";
        for (size_t i = 0; i < expected.size(); ++i) {
            if (i) std::cerr << ", ";
            std::cerr << expected[i];
        }
        std::cerr << "]\nActual:   [";
        for (size_t i = 0; i < actual.size(); ++i) {
            if (i) std::cerr << ", ";
            std::cerr << actual[i];
        }
        std::cerr << "]\n";
        throw std::runtime_error("vector mismatch");
    }
}

// ---------- Individual test cases ----------
static void test_basic_right() {
    std::vector<int> v{1,2,3,4,5};
    rotate(v, 2);
    expect_eq_vec({4,5,1,2,3}, v, "basic right-rotate by 2");
}

static void test_k_zero_and_multiple_of_n() {
    std::vector<int> v1{1,2,3,4,5};
    rotate(v1, 0);
    expect_eq_vec({1,2,3,4,5}, v1, "k=0 should be identity");

    std::vector<int> v2{1,2,3,4,5};
    rotate(v2, 5);
    expect_eq_vec({1,2,3,4,5}, v2, "k==n should be identity");

    std::vector<int> v3{1,2,3,4,5};
    rotate(v3, 12); // 12 % 5 == 2
    expect_eq_vec({4,5,1,2,3}, v3, "k>n normalized by modulo");
}

static void test_negative_k() {
    std::vector<int> v{1,2,3,4,5};
    rotate(v, -1); // left by 1
    expect_eq_vec({2,3,4,5,1}, v, "k<0 should rotate left by |k|");
}

static void test_large_negative_k() {
    std::vector<int> v{1,2,3,4,5};
    rotate(v, -12); // -12 % 5 == -2 -> normalize to +3 right
    expect_eq_vec({3,4,5,1,2}, v, "large negative k normalized");
}

static void test_edge_cases() {
    std::vector<int> empty;
    rotate(empty, 3);
    expect(empty.empty(), "empty vector should stay empty");

    std::vector<int> one{42};
    rotate(one, 999);
    expect_eq_vec({42}, one, "single-element stays same");
}

// ---------- Test driver ----------
static void test() {
    test_basic_right();
    test_k_zero_and_multiple_of_n();
    test_negative_k();
    test_large_negative_k();
    test_edge_cases();
}

// ---------- Clean main ----------
int main() {
    try {
        test();
        std::cout << "All tests passed.\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "TEST FAIL: " << e.what() << "\n";
        return 1;
    }
}
