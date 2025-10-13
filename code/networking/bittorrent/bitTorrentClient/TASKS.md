# Tasks

## Phase 1: CLI Client

This phase focuses on building a functional command-line BitTorrent client in Rust.

### Core Functionality

*   [ ] **Project Setup:**
    *   [ ] Initialize Rust project (`cargo new`).
    *   [ ] Define basic module structure (`src/main.rs`, `src/lib.rs`, submodules like `parser`, `tracker`, `peer`, `storage`, etc.).
    *   [ ] Add core dependencies (`tokio`, `serde`, `serde_derive`, `serde_bencode`, `reqwest`, `sha1`, `hex`, `clap`, `thiserror`, `tracing`, `tracing-subscriber`) to `Cargo.toml`.
    *   [ ] Set up basic logging/tracing infrastructure.
*   [ ] **Torrent File Parsing:**
    *   [ ] Define Rust structs for Metainfo (`.torrent`) file structure using `serde`.
    *   [ ] Implement Bencoding decoding for `.torrent` files (using `serde_bencode`).
    *   [ ] Add function to load and parse a `.torrent` file from disk.
    *   [ ] Calculate `info_hash`.
    *   [ ] Write unit tests for torrent parsing and `info_hash` calculation.
*   [ ] **Tracker Communication (HTTP):**
    *   [ ] Define Rust structs for HTTP tracker requests (announce parameters) and responses (`serde`).
    *   [ ] Implement logic to build the announce URL with proper URL encoding.
    *   [ ] Implement function to make HTTP GET requests to tracker using `reqwest`.
    *   [ ] Parse Bencoded tracker responses.
    *   [ ] Extract peer list (IP addresses and ports).
    *   [ ] Handle tracker errors.
    *   [ ] Write unit tests for HTTP tracker request building and response parsing.
*   [ ] **Peer Connection & Handshake:**
    *   [ ] Implement asynchronous TCP connection logic to peers using `tokio::net::TcpStream`.
    *   [ ] Define the structure for the BitTorrent handshake message.
    *   [ ] Implement handshake serialization and deserialization.
    *   [ ] Implement logic to send and receive/validate the handshake.
    *   [ ] Write unit tests for handshake logic.
*   [ ] **Peer Wire Protocol (Core Messages):**
    *   [ ] Define Rust enums/structs for peer message types (ID, payload).
    *   [ ] Implement serialization/deserialization for message framing (length prefix + ID + payload).
    *   [ ] Implement handling for `keep-alive`, `choke`, `unchoke`, `interested`, `not interested` messages.
    *   [ ] Establish basic read/write loop for peer communication using `tokio` tasks.
    *   [ ] Write unit tests for message serialization/deserialization and basic message handling.
*   [ ] **Piece Management & Bitfield:**
    *   [ ] Implement data structure(s) to track piece status (have, needed, requested, downloaded).
    *   [ ] Implement `Bitfield` message sending (after handshake).
    *   [ ] Implement handling for incoming `Bitfield` messages to update peer piece availability.
    *   [ ] Implement handling for `Have` messages.
    *   [ ] Write unit tests for piece state tracking and bitfield/have message handling.
*   [ ] **Data Transfer (`Request`, `Piece`, `Cancel`):**
    *   [ ] Implement serialization/deserialization for `Request`, `Piece`, `Cancel` messages.
    *   [ ] Implement logic to send `Interested` message when a peer has desired pieces.
    *   [ ] Implement logic to send `Request` messages for specific piece blocks when unchoked.
    *   [ ] Implement logic to handle incoming `Piece` messages, verify block data (length), and store temporarily.
    *   [ ] Write unit tests for data transfer message handling.
*   [ ] **Storage Management:**
    *   [ ] Implement logic to create/open file(s) based on torrent metadata.
    *   [ ] Implement asynchronous file I/O (`tokio::fs`) to write verified piece data to the correct file offset(s).
    *   [ ] Implement piece hash verification (SHA-1) against hashes in torrent metadata.
    *   [ ] Implement logic to read piece data from disk for uploading.
    *   [ ] Write unit tests for storage operations (writing, reading, verification).
*   [ ] **Download Strategy & Orchestration:**
    *   [ ] Implement a basic piece selection strategy (e.g., rarest first based on peer bitfields).
    *   [ ] Implement logic to manage concurrent peer connections and tasks.
    *   [ ] Implement a main loop coordinating tracker updates, peer connections, and data transfer.
    *   [ ] Implement basic rate limiting or connection management.
*   [ ] **Upload Logic:**
    *   [ ] Implement logic to handle incoming `Request` messages from peers.
    *   [ ] Read requested block data from storage.
    *   [ ] Send `Piece` messages to requesting peers.
    *   [ ] Implement basic choking/unchoking logic for upload management (can be simple initially).
*   [ ] **CLI Interface:**
    *   [ ] Integrate `clap` for command-line argument parsing (e.g., `client <torrent_file>`).
    *   [ ] Implement basic output to display download progress (e.g., percentage, speed).
    *   [ ] Handle graceful shutdown (Ctrl+C).

### Advanced/Optional (Phase 1)

*   [ ] **Tracker Communication (UDP):**
    *   [ ] Research and implement the UDP tracker protocol.
    *   [ ] Write unit tests for UDP tracker interaction.
*   [ ] **Error Handling & Resilience:**
    *   [ ] Improve error handling across all modules using `thiserror` or similar.
    *   [ ] Add more robust peer connection retry logic.
*   [ ] **Configuration:**
    *   [ ] Implement loading configuration from a file (e.g., download directory, port bindings).

### Documentation & Testing

*   [ ] Maintain `README.md`, `ARCHITECTURE.md`, `PLAN.md`, `TASKS.md`.
*   [ ] Ensure reasonable unit test coverage for all core components. 