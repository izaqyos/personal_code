#pragma once
#include <iostream>
#include <unordered_map>
#include <vector>

namespace util {

template <class T>
inline void print_vector(const std::vector<T>& v, std::ostream& os = std::cout) {
    os << "[ ";
    for (const auto& x : v) os << x << ' ';
    os << "]\n";
}

template <class K, class V>
inline void print_map(const std::unordered_map<K, V>& m, std::ostream& os = std::cout) {
    os << "{ ";
    bool first = true;
    for (const auto& kv : m) {
        if (!first) os << ", ";
        os << kv.first << ": " << kv.second;
        first = false;
    }
    os << " }\n";
}

} // namespace util
