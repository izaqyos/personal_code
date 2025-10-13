#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

/*
Rules:

Case-insensitive: treat “Tea” and “eat” as anagrams.

Ignore non-letters inside a word (so rock’n’roll → rocknroll for matching).

Output groups sorted by size desc, then by first word asc.

Inside each group, sort words asc (case-insensitive).
*/

// sanitize word: keep letters only, make lowercase
static std::string normalized_letters(std::string_view s) {
    std::string out;
    out.reserve(s.size());
    for (unsigned char ch : s) {
        if (std::isalpha(ch)) out.push_back(static_cast<char>(std::tolower(ch)));
    }
    return out;
}

// signature: sorted letters of normalized word
static std::string signature(std::string_view s) {
    std::string t = normalized_letters(s);
    std::sort(t.begin(), t.end());
    return t;
}

std::vector<std::vector<std::string>>
group_anagrams(const std::vector<std::string>& words) {
    // TODO:
    // 1) bucket words by signature (unordered_map<string, vector<string>>)
    // 2) sort each bucket case-insensitively
    // 3) move buckets into a vector
    // 4) sort groups by (size desc, first word asc)
    // 5) return groups
    std::vector<std::vector<std::string>> groups;
    std::unordered_map<std::string, std::vector<std::string>> buckets;
    buckets.reserve(words.size());
    for (const auto& word : words) {
        std::string sig = signature(word);
        buckets[sig].push_back(word);
    }
    for (auto& [sig, bucket] : buckets) {
        std::sort(bucket.begin(), bucket.end(), 
                    [](const std::string&a, const std::string& b) {
                        return std::lexicographical_compare(
                            a.begin(), a.end(), b.begin(), b.end(), 
                            [](unsigned char c1, unsigned char c2) {
                                return std::tolower(c1) < std::tolower(c2);
                            });
                            });
        groups.emplace_back(std::move(bucket));
                    }
    groups.reserve(buckets.size());
    std::sort(groups.begin(), groups.end(), 
        [] (const std::vector<std::string>& a, const std::vector<std::string>& b) {
            if (a.size() != b.size()) return a.size() > b.size();
            // for tie break sort by first word lexicographically ascending
            return std::lexicographical_compare(
                a[0].begin(), a[0].end(), b[0].begin(), b[0].end(), 
                [](unsigned char c1, unsigned char c2) {
                    return std::tolower(c1) < std::tolower(c2);
                });
        });
    return groups;
}

int main(int argc, char** argv) {
    // Input: words from argv (if present) else from stdin (one per line)
    std::vector<std::string> words;
    if (argc > 1) {
        for (int i = 1; i < argc; ++i) words.emplace_back(argv[i]);
    } else {
        std::string w;
        while (std::getline(std::cin, w)) {
            if (!w.empty()) words.emplace_back(w);
        }
    }

    auto groups = group_anagrams(words);

    // Print: one group per line: size: word1, word2, ...
    for (const auto& g : groups) {
        std::cout << g.size() << ": ";
        for (size_t i = 0; i < g.size(); ++i) {
            if (i) std::cout << ", ";
            std::cout << g[i];
        }
        std::cout << "\n";
    }
    return 0;
}
