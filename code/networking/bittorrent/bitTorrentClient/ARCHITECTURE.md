# Architecture

This document outlines the high-level architecture of the Rust-based BitTorrent client.

## Core Components (Phase 1 - CLI)

*   **Torrent Parser:** Reads `.torrent` files, decodes Bencoded metadata using `serde_bencode`.
*   **Tracker Client:** Communicates with HTTP/UDP trackers (using `reqwest` or similar) to announce, get peers.
*   **Peer Wire Protocol:** Implements the BitTorrent peer protocol for communication with other peers (`tokio::net`).
    *   Handshake
    *   Message Handling (keep-alive, choke, unchoke, interested, not interested, have, bitfield, request, piece, cancel, port)
*   **Piece Manager:** Manages the state of pieces (needed, requested, downloaded, verified).
*   **Download/Upload Manager:** Orchestrates requests to peers, handles incoming requests, manages concurrency (`tokio` tasks).
*   **Storage Manager:** Reads/writes piece data to disk.
*   **Main Loop/Orchestrator:** Ties all components together, manages the overall download/upload process.
*   **CLI Interface:** Provides user interaction (e.g., adding torrents, viewing status).

## Phase 2 - GUI Integration

*   **API Layer:** The Rust core will expose an API (likely REST or WebSockets using crates like `actix-web`, `warp`, or `axum`) for the GUI.
*   **React Frontend:** A separate web application built with React that consumes the API to display status, manage torrents, etc. 