Language notes (Rust): no unwrap/expect/panic in library code, return Result with a specific error type;
borrow instead of clone unless ownership is needed; no unsafe; clippy-clean; unit tests in a
`#[cfg(test)] mod tests` at the end of the file, integration tests under tests/.
