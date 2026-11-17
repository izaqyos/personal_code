id: R1
title: feat(text): add slugify
edit: src/text.rs tests/text.rs
read: src/lib.rs
test: cargo test -q --test text
lint: cargo clippy -q --all-targets -- -D warnings
---
Goal: one sentence on what this card delivers.

## Design (implement exactly these, nothing more)

File src/text.rs:

    pub fn slugify(text: &str, max_len: usize) -> Result<String, SlugError>

## Test plan (write exactly these tests in tests/text.rs)

fn slugify_joins_words_with_dashes()
fn slugify_truncates_without_trailing_dash()
fn slugify_rejects_zero_max_len()
