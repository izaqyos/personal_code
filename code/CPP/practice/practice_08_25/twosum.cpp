#include "util.hpp"
#include <iostream>
#include <vector>
#include <utility>
#include <unordered_map>


//void print_vector(const std::vector<int>& v) {
//    std::cout << "[ ";
//    for (const auto& n : v) {
//        std::cout << n << " ";
//    }
//    std::cout << "]\n";
//}
//
//void print_map(const std::unordered_map<int, int>& m) {
//    std::cout << "{ ";
//    for (const auto& kv : m) {
//        std::cout << kv.first << ": " << kv.second << ", ";
//    }
//    std::cout << "}\n";
//}

std::pair<int, int> two_sum(const std::vector<int>& nums, int target) {
    std::cout << "Input array: ";
    util::print_vector(nums);

    std::unordered_map<int, int> num_to_index;
    for (auto &n: nums) {
        // std::cout<< "checking " << n << "\n";
        if (num_to_index.find(n) != num_to_index.end()) {
            // std::cout << "found pair: " << n << " + " << target - n << " at indices: "<< num_to_index[n] << "," << &n - &nums[0] << "\n";
            return {num_to_index[n], &n - &nums[0]};
        }
        num_to_index[target - n] = &n - &nums[0];   
        // util::print_map(num_to_index);
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