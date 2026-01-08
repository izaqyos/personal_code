# Changelog

## [Unreleased] - 2026-01-07

### Added
- **Atlassian Token Validation Improvements**
  - Process-based validation fallback when API validation fails
  - Detection of running `mcp-remote` processes to determine token validity
  - Support for MCP-scoped tokens that don't work with REST APIs
  - Comprehensive troubleshooting guide: `docs/ATLASSIAN_TOKEN_ISSUES.md`

- **Re-authentication Support**
  - New `--reauth` CLI flag for full OAuth re-authentication
  - `reauth_atlassian()` method to spawn `npx mcp-remote` for fresh OAuth
  - Automatic stale token cleanup before re-authentication
  - Fallback from auto-refresh to re-auth when refresh token is invalid

- **Enhanced Error Detection**
  - Specific detection of `unauthorized_client` errors for invalid refresh tokens
  - Better error messages with actionable instructions
  - Cursor MCP toggle instructions in notifications

### Changed
- **Atlassian Validator (`validators/atlassian.py`)**
  - Now checks for running `mcp-remote` processes as validation fallback
  - Returns `VALID` status when process is detected, even if API returns 401
  - Added warning messages about MCP-scoped token limitations
  - Updated refresh instructions to prioritize Cursor toggle method

- **OAuth Refresher (`refresh/oauth.py`)**
  - Added `ReauthStatus` and `ReauthResult` dataclasses
  - Implemented `reauth_atlassian()` for spawning OAuth flow
  - Enhanced `_handle_error()` to detect invalid refresh tokens
  - Added `_clear_stale_tokens()` helper for cleanup

- **CLI (`cli.py`)**
  - Added `--reauth` flag to all check commands
  - Updated `_validate_server()` to handle re-auth flow
  - Automatic fallback from refresh to re-auth when needed
  - Propagated reauth parameter through all validation functions

- **User Notifications (`refresh/notifier.py`)**
  - Updated Atlassian notification with Cursor toggle instructions
  - Added `--reauth` command as alternative option
  - Simplified steps for better user experience

### Fixed
- **Hash-Prefixed Token Files**
  - Fixed token file detection for `*_tokens.json` pattern
  - Both validators and refreshers now search for hash-prefixed files
  - Supports multiple token file patterns in subdirectories

- **Stale Token Detection**
  - `mcp-health` no longer reports false negatives when `mcp-remote` is running
  - Process detection compensates for stale token files on disk
  - Better handling of in-memory vs persisted token discrepancies

### Documentation
- Added `docs/ATLASSIAN_TOKEN_ISSUES.md` - comprehensive troubleshooting guide
  - Architecture comparison: Claude Code vs Cursor
  - Why `mcp-remote` is required for desktop clients
  - Why there's no alternative to `mcp-remote`
  - Technical deep dive with token flow diagrams
  - Comparison of different MCP clients
  - Recommendations for users, teams, and developers
- Updated `README.md` with Atlassian special considerations section
- Added documentation link in main documentation table
- Inline code comments explaining MCP-scoped token behavior

## Root Cause Analysis

### The Problem
Atlassian MCP uses `mcp-remote` which manages OAuth tokens with unique characteristics:

1. **MCP-Scoped Tokens**: Tokens work for MCP protocol but not standard REST APIs
2. **In-Memory Management**: `mcp-remote` keeps fresh tokens in memory
3. **Delayed Persistence**: Token files on disk can become stale
4. **API Validation Fails**: Even valid MCP tokens return 401 from REST endpoints
5. **No Alternative**: `mcp-remote` is the official Atlassian-recommended proxy

### Why Claude Code Works Better

**Architecture Difference:**

| Client | Connection | OAuth | Token Storage | Issues |
|--------|------------|-------|---------------|--------|
| **Claude Code** | Direct to cloud | Native | Managed by Anthropic | None |
| **Cursor** | Via `mcp-remote` | External | Local files | Token sync issues |

Claude Code has **native MCP OAuth support** and connects directly to `https://mcp.atlassian.com/v1/sse`, eliminating the need for `mcp-remote` and its associated token file issues.

### The Solution
Multi-layered validation approach:

1. **Primary**: Try API validation (expected to fail for MCP-scoped tokens)
2. **Fallback**: Check if `mcp-remote` process is running
3. **Result**: Report as valid if process is active, with appropriate warnings
4. **Re-auth**: Provide clear instructions to toggle MCP in Cursor
5. **Documentation**: Explain why Claude Code works seamlessly

### User Experience
- **Before**: False negatives, confusing "expired" messages when MCP works
- **After**: Accurate status, clear instructions, automatic fallback detection
- **Alternative**: Use Claude Code for Atlassian-heavy workflows (no issues)

## Testing

All changes tested with:
- Running `mcp-remote` processes
- Stale token files on disk
- Fresh OAuth flows via Cursor toggle
- Manual re-authentication via `--reauth`
- Auto-refresh with invalid refresh tokens

## Breaking Changes

None. All changes are backward compatible.

## Migration Guide

No migration needed. Existing installations will automatically benefit from improved validation.

## Future Enhancements

1. **MCP-Native Validation**: Use MCP protocol directly instead of REST API
2. **Token Freshness Tracking**: Add `issued_at` timestamps to persisted tokens
3. **Automatic Process Monitoring**: Real-time detection of `mcp-remote` state changes
4. **Better Token Persistence**: Work with `mcp-remote` team to ensure immediate persistence

