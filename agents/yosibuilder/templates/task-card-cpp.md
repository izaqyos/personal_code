id: C1
title: feat(text): add slugify
lang: cpp
edit: src/text.cpp include/text.h tests/text_test.cc
test: cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug && cmake --build build --target text_test && ctest --test-dir build -R Slugify --output-on-failure
lint: clang-tidy src/text.cpp -p build --warnings-as-errors=*
mutants: 20
---
Goal: one sentence on what this card delivers.

## Design (implement exactly these, nothing more)

    std::string slugify(std::string_view text, std::size_t max_len);  // throws std::invalid_argument if max_len == 0

## Test plan (write exactly these tests in tests/text_test.cc, GoogleTest)

TEST(Slugify, JoinsWordsWithDashes)
TEST(Slugify, TruncatesWithoutTrailingDash)
TEST(Slugify, RejectsZeroMaxLen)
