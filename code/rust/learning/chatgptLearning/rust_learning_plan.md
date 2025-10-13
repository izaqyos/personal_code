# Rust Learning Plan (90 Days, ~5–7 hrs/week)
**Owner:** Yosi  
**Start date:** 2025-08-25  
**Goal:** Become productive enough to ship a small Rust component to production, set team policy for Rust usage, and mentor engineers on interop with C++/Node/Python.

---

## TL;DR Objectives
- ✅ Ship **3 deliverables**: (1) a hot-path Rust lib exposed to Node or Python, (2) a small Axum web service with Postgres/Redis, (3) a Rust FFI “island” in a C++ codebase.  
- ✅ Establish **team Rust safety policy** (unsafe review, CI checks, supply-chain hygiene).  
- ✅ Benchmark & document real perf/safety impact vs current stack.

---

## Success Criteria (Definition of Done)
- **Prod artifact:** At least one Rust component used by your team (behind a feature flag is fine).
- **Reliability:** Zero `unsafe` *except* in fenced, reviewed blocks with documented safety invariants.
- **Observability:** Tracing spans, metrics, and logs wired to your stack.
- **Security/Supply chain:** `cargo audit` and `cargo deny` clean in CI; lockfile committed; MSRV defined.
- **Interop:** One of: Node via `napi-rs`, Python via `PyO3`, or C++ via `cxx` landed and exercised in CI.
- **Knowledge transfer:** Short internal doc + 30‑min brownbag delivered.

---

## Prereqs (install once)
- Toolchain: `rustup`, `cargo`, `rust-analyzer`, `rustfmt`, `clippy`.
- Testing: `cargo-nextest`, `cargo-tarpaulin` (coverage, optional), `cargo-llvm-cov` (alt).
- Perf: `cargo-flamegraph` (requires `perf`/`dtrace`), `hyperfine`, `criterion`.
- Security/Quality: `cargo-audit`, `cargo-deny`, `cargo-fuzz` (libFuzzer).
- Interop:  
  - Node: `napi-rs`, `@napi-rs/cli`  
  - Python: `pyo3`, `maturin`  
  - C/C++: `cxx`, `cbindgen`, `bindgen`
- DB/Net: `sqlx` (w/ offline mode), `tokio`, `axum`, `reqwest`, `tracing`, `tracing-subscriber`.
- Build accel: `sccache` (optional, recommended).

```bash
# Minimal setup
curl https://sh.rustup.rs -sSf | sh
rustup component add rustfmt clippy
cargo install cargo-nextest cargo-audit cargo-deny hyperfine
# Optional: fuzz, profiling, coverage
cargo install cargo-fuzz flamegraph cargo-llvm-cov
```

---

## Timeboxed Plan

### Phase 1 — Foundations (Days 1–30)
**Focus:** Ownership & borrowing, error handling, traits; build one real “hot path” library.

**Weekly checkpoints**
- **Week 1**
  - [ ] Read/skim: ownership/borrowing, slices, lifetimes, `Result`/`?`, `From`/`Into`.
  - [ ] Exercises: rewrite 2 tiny utilities from your toolbox (e.g., checksum, fast CSV scan).
  - [ ] Tooling: enable `clippy` and `rustfmt` in editor; set `RUSTFLAGS` for debuginfo.
- **Week 2**
  - [ ] Iterators & zero‑cost abstractions; avoid premature allocation.
  - [ ] Bench harness with `criterion` and quick‑n‑dirty `hyperfine`.
  - [ ] Start **Project 1** (below).
- **Week 3**
  - [ ] Error strategy: `thiserror` or `anyhow` (lib vs binary).
  - [ ] Public API design: traits, `&[u8]`/`Cow<'_, [u8]>`, `FromStr`, `Display`.
  - [ ] Add docs (`cargo doc`), examples, and `#[deny(warnings)]` via clippy config.
- **Week 4**
  - [ ] Fuzz parsers (`cargo fuzz`) if applicable.
  - [ ] Ship v0.1 of Project 1 to an internal consumer (Node/Python).

**Project 1 — “Hot Path in Rust” (2–3 weeks)**
- **Idea bank:** log/metric line parser, base‑N encoder/decoder, streaming JSON/CBOR transform, domain-specific hashing, URL sanitizer, small DSL interpreter.
- **Interop option A (Node):** `napi-rs` wrapper; publish a local npm package.
- **Interop option B (Python):** `PyO3` + `maturin develop`; expose a simple function/class.
- **Acceptance:**
  - [ ] ≥2× speedup vs JS/Python baseline on real data.
  - [ ] Zero `unsafe` or fenced with invariants.
  - [ ] Unit tests + property tests; fuzzing if parsing.
  - [ ] Bench results and a 1‑page “why Rust here” note.

---

### Phase 2 — Services & Async (Days 31–60)
**Focus:** Async I/O, observability, SQL safety, backpressure.

**Weekly checkpoints**
- **Week 5**
  - [ ] Tokio basics; tasks, cancellations, structured concurrency.
  - [ ] Axum hello world; route extractors; middleware.
- **Week 6**
  - [ ] Postgres with `sqlx` (offline mode, compile‑time checked queries).
  - [ ] Connection pools, timeouts, retries (be explicit).
  - [ ] `tracing` spans; request IDs; error layers.
- **Week 7**
  - [ ] Rate limiting/backpressure; avoid blocking in async.
  - [ ] Structured config (`figment`/`envy`), secrets via env or your vault.
- **Week 8**
  - [ ] Hardening: e2e tests, load tests, flamegraphs.
  - [ ] Ship internal **Project 2** behind a feature flag.

**Project 2 — “Rust Sidecar Service” (3–4 weeks)**
- **Scope:** Axum JSON API; endpoints for a compute-heavy transform + metadata CRUD.
- **Infra:** Postgres (via `sqlx`), Redis cache (optional), `reqwest` to call an upstream.
- **Obs:** `tracing` + OpenTelemetry exporter; percentiles on latency; error rates.
- **Acceptance:**
  - [ ] SLO: p95 latency & error budget documented.
  - [ ] Graceful shutdown; timeouts on all I/O.
  - [ ] Load-test report + flamegraphs checked in.
  - [ ] CI: tests, format, lint, audit, deny pass on PR.

---

### Phase 3 — Interop & Safety Leadership (Days 61–90)
**Focus:** C++ FFI, safety policy, supply chain, repeatability.

**Weekly checkpoints**
- **Week 9**
  - [ ] Pick a crash‑prone or security‑exposed C++ path (parser/crypto/IO).
  - [ ] Define the FFI boundary; value vs pointer semantics; ownership doc.
- **Week 10**
  - [ ] Implement Rust lib; expose C ABI via `cbindgen` or use `cxx` bridge.
  - [ ] Add ASan/UBSan to C++ CI; fuzz the Rust lib.
- **Week 11**
  - [ ] Write the **Rust Safety RFC**: `unsafe` policy, review checklist, crate selection rules, MSRV.
  - [ ] Add `cargo audit` & `cargo deny` gates to CI; license policy defined.
- **Week 12**
  - [ ] Integrate FFI module into staging; run shadow traffic/tests.
  - [ ] Deliver 30‑min internal talk and publish READMEs.

**Project 3 — “Rust Island in C++” (3–4 weeks)**
- **Acceptance:**
  - [ ] Ownership at boundary documented; `unsafe` sections justified with invariants.
  - [ ] Sanitizers (C++) + fuzz (Rust) green; perf not worse; ideally better.
  - [ ] Rollout plan (flagged); fallback path defined.

---

## CI Template (GitHub Actions, sketch)

```yaml
name: rust-ci
on:
  pull_request:
  push:
    branches: [ main ]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: {{toolchain: stable, components: rustfmt, clippy}}
      - name: Cache cargo
        uses: Swatinem/rust-cache@v2
      - name: Format
        run: cargo fmt --all -- --check
      - name: Clippy
        run: cargo clippy --all-targets --all-features -- -D warnings
      - name: Tests
        run: cargo nextest run --all
      - name: Audit
        run: cargo audit || true   # set to hard-fail once backlog is cleared
      - name: Deny (licenses/deps)
        run: cargo deny check
```

*(Add separate jobs for fuzz, coverage, and FFI matrix with ASan/UBSan on C++.)*

---

## Team Rust Safety Policy (one-page starter)
- **Crate selection:** maintained, MSRV >= 1.74 (example), recent release ≤ 6 months, no critical advisories.
- **`unsafe` rule:** only inside leaf modules; each block has a doc comment stating invariants and why Rust’s borrow checker cannot encode them; code review by 2 seniors.
- **Fuzzing:** required for all parsers and binary protocols.
- **I/O:** timeouts are mandatory; no unbounded channels/queues without backpressure.
- **Logging:** structured logs with request IDs; no secrets in logs.
- **Panics:** never cross FFI boundary; binaries use panic hooks; libraries return `Result`.

---

## Reference Skeletons

**Axum + SQLX service**
```
svc/
  Cargo.toml
  src/
    main.rs
    routes.rs
    db.rs
    models.rs
    error.rs
    telemetry.rs
  .sqlx/            # offline checks
  migrations/       # sqlx migrate
```

**Node interop (napi-rs)**
```
myaddon/
  Cargo.toml
  src/lib.rs
  package.json
  npm scripts: build via @napi-rs/cli
```

**C++ interop (cxx)**
```
ffi/
  Cargo.toml
  src/lib.rs
  include/bridge.h
  src/bridge.cc
  build.rs
```

---

## Common Pitfalls → Counters
- **Borrow checker pain** → narrow mutability, split types, favor `&[u8]` over `Vec<u8>`.
- **Async blocking** → audit with `tokio-console`; move CPU work to `spawn_blocking`.
- **Compile times** → workspaces, feature flags, `sccache`, avoid macro-heavy crates.
- **Crate sprawl** → baseline on std + a few well-curated deps; review transitive deps with `cargo deny`.

---

## Minimal Cheatsheet
```rust
// Error ergonomics
type Result<T> = std::result::Result<T, anyhow::Error>;

// Borrowing APIs
fn scan(input: &[u8]) -> Result<usize> {{ /* ... */ }}

// Traits for testability
trait Store {{ fn put(&self, k: &str, v: &[u8]) -> Result<()>; }}

// Tracing
#[tracing::instrument(skip_all, fields(req_id=%req_id))]
async fn handle(...) -> Result<Response> {{ /* ... */ }}

// FFI guardrail
#[no_mangle]
pub extern "C" fn do_thing(ptr: *const u8, len: usize) -> i32 {{
    let slice = unsafe {{ std::slice::from_raw_parts(ptr, len) }};
    match core_logic(slice) {{ Ok(_) => 0, Err(_) => -1 }}
}}
```

---

## Reading/Practice (shortlist)
- *The Rust Programming Language (TRPL)* — ownership, lifetimes, traits.
- *Rust by Example* — quick pattern drills.
- *Rustonomicon* — only when you touch `unsafe`.
- `tokio`, `axum`, `sqlx` official guides; `napi-rs`, `PyO3`, `cxx` docs.
- Write 10 small katas: iterators, `FromStr`, `Display`, `TryFrom`, error types, `Arc/RwLock` vs channels, async cancellation.

---

## Personal Backlog (fill in)
- [ ] Candidate hot path(s):
- [ ] Service idea(s):
- [ ] C++ island target(s):
- [ ] Metrics to track (latency, CPU, allocs):
- [ ] Rollout plan / stakeholders:

---

## Review Cadence
- **Weekly:** update checkboxes; record learnings, TODOs, perf deltas.
- **Monthly:** 1‑pager progress note + risks; adjust scope ruthlessly.

> **Bottom line:** Don’t rewrite working C++. Carve sharp, well‑bounded Rust islands where perf/safety pay off, prove value with numbers, and codify the guardrails so the team can scale it.
