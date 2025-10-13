#include <string_view>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <string>
#include <cctype>

#include "util.hpp"


// ---------- helpers  ----------
static inline std::string_view ltrim_sv(std::string_view sv) {
    int i = 0;
    while (std::isspace((unsigned char)sv[i])) {
        ++i;
    }
    sv.remove_prefix(i);
    return sv;
}

static inline std::string_view rtrim_sv(std::string_view sv) {
    int i = 0;
    while (std::isspace((unsigned char) sv[sv.size()-i-1])) {
        ++i;
    }
    sv.remove_suffix(i);
    return sv;
}

static inline std::string_view trim_sv(std::string_view sv) {
    return rtrim_sv(ltrim_sv(sv));
}

// ---------- API ----------
// Split s by 'delim', trim ASCII spaces around each token, and return views.
// No allocations for tokens: returned string_views refer to 's'.
// Keep empty fields (e.g., ",,") as empty views after trimming.
std::vector<std::string_view> split_trim(std::string_view s, char delim) {
    std::cout<<"Splitting string: \""<<s<<"\" by '"<<delim<<std::endl;
    std::vector<std::string_view> result;
    size_t i = 0, lpos = 0;
    while (i<s.size()) {
        if (s[i] == delim) {
            std::string_view token = s.substr(lpos, i - lpos);
            result.push_back(trim_sv(token)); // specifically asked to keep empty fields
            lpos = i + 1;
        }
        ++i;
    }

    // last token - whenever delim is not last char in s will not be empty
    std::string_view last_token = s.substr(lpos, s.size());
    result.push_back(trim_sv(last_token));

    std::cout<<"Returning result:"<<std::endl;
    util::print_vector(result);
    return result;
}


// ---------- Minimal test utilities (no macros) ----------
static void expect(bool cond, const char* msg) {
    if (!cond) throw std::runtime_error(msg);
}

static void expect_eq_sv_vec(const std::vector<std::string_view>& expected,
                             const std::vector<std::string_view>& actual,
                             const char* msg) {
    if (expected.size() != actual.size()) {
        std::cerr << msg << " (size mismatch) exp=" << expected.size()
                  << " got=" << actual.size() << "\n";
        throw std::runtime_error("vector size mismatch");
    }
    for (size_t i = 0; i < expected.size(); ++i) {
        if (expected[i] != actual[i]) {
            std::cerr << msg << " at idx " << i
                      << " exp: \"" << expected[i]
                      << "\" got: \"" << actual[i] << "\"\n";
            throw std::runtime_error("vector content mismatch");
        }
    }
}

// ---------- Individual test cases ----------
static void test_basic() {
    // Keep backing string alive while views are used
    std::string src = " a, bb , c ";
    auto parts = split_trim(std::string_view{src}, ',');
    expect_eq_sv_vec({"a","bb","c"}, parts, "basic split+trim");
}

static void test_empty_fields_and_spaces() {
    std::string src = " , ,x,, ";
    auto parts = split_trim(std::string_view{src}, ',');
    // Keep empty fields (after trimming)
    std::vector<std::string_view> expected = {"", "", "x", "", ""};
    expect_eq_sv_vec(expected, parts, "empties preserved");
}

static void test_no_delim_one_token() {
    std::string src = "   lone   ";
    auto parts = split_trim(std::string_view{src}, ',');
    expect_eq_sv_vec({"lone"}, parts, "no-delim single token");
}

static void test_internal_spaces_preserved() {
    std::string src = "a b, c  d ";
    auto parts = split_trim(std::string_view{src}, ',');
    expect_eq_sv_vec({"a b","c  d"}, parts, "inner spaces kept");
}

static void test_edge_leading_trailing_delims() {
    std::string src = ",a,b,";
    auto parts = split_trim(std::string_view{src}, ',');
    expect_eq_sv_vec({"","a","b",""}, parts, "leading/trailing delim");
}

// ---------- Test driver ----------
static void test() {
    test_basic();
    test_empty_fields_and_spaces();
    test_no_delim_one_token();
    test_internal_spaces_preserved();
    test_edge_leading_trailing_delims();
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
