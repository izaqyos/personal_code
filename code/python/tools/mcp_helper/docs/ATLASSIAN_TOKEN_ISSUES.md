# Atlassian MCP Token Issues and Solutions

## Overview

The Atlassian MCP server uses OAuth tokens managed by `mcp-remote`, which can exhibit unique behavior compared to other MCP servers. This document explains common issues and their solutions.

### Quick Summary

**Why does Atlassian MCP have token issues in Cursor but not Claude Code?**

- **Claude Code** connects directly to Atlassian's cloud with native OAuth support
- **Cursor** requires `mcp-remote` as a proxy, which stores tokens in local files
- Token files can become stale while in-memory tokens remain fresh
- MCP-scoped tokens don't work with standard REST APIs

**Quick Fix:**
```bash
# Option 1: Toggle in Cursor (most reliable)
Settings → MCP Servers → Toggle Atlassian OFF/ON

# Option 2: Use mcp-health
mcp-health check --server perimeter81-atlassian --reauth

# Option 3: Use Claude Code (no issues)
```

**Is there an alternative to mcp-remote?**

**No.** `mcp-remote` is the official Atlassian-recommended solution for desktop clients. There is no alternative that works with Cursor. Claude Code works seamlessly because it has native MCP OAuth support built-in.

## Why mcp-remote is Required

### Architecture Differences

**Claude Code vs Desktop Clients:**

| Client Type | Connection Method | OAuth Handling | Token Storage |
|-------------|------------------|----------------|---------------|
| **Claude Code / Claude.ai** | Direct to `https://mcp.atlassian.com/v1/sse` | Native (in-app) | Managed by Anthropic |
| **Cursor / VS Code** | Via `mcp-remote` proxy | External (browser) | Local files (`~/.mcp-auth/`) |

### Why Desktop Clients Need mcp-remote

Desktop IDEs like Cursor and VS Code **cannot** connect directly to Atlassian's SSE (Server-Sent Events) endpoint with OAuth 2.1 authentication. They require `mcp-remote` as a **local proxy bridge** that:

1. Spawns a local server to handle OAuth callbacks
2. Opens a browser for user authentication
3. Stores tokens locally for subsequent requests
4. Proxies MCP protocol messages between IDE and Atlassian cloud

**Source:** [Official Atlassian MCP Server Repository](https://github.com/atlassian/atlassian-mcp-server)

### Why Claude Code Works Seamlessly

Claude Code (the Anthropic desktop app) has **native MCP OAuth support** built-in:
- Handles OAuth flows internally without external processes
- Manages token storage securely within the application
- No token file synchronization issues
- Seamless token refresh without user intervention

This is why you experience "flawless and seamless" operation in Claude Code but encounter issues in Cursor.

### Alternative Solutions

**Option 1: Use Claude Code for Atlassian Tasks**
- Most reliable option
- Native OAuth support
- No token persistence issues
- Recommended for heavy Jira/Confluence workflows

**Option 2: Use VS Code with Native MCP Support**
- VS Code has first-party MCP support (as of late 2024)
- May handle token management better than Cursor
- Worth testing if Cursor issues persist

**Option 3: Wait for Cursor Native MCP OAuth**
- Cursor currently spawns `mcp-remote` as external process
- Native OAuth support would eliminate token file issues
- Feature request could be filed with Cursor team

**Option 4: Contribute to mcp-remote**
- Token persistence issues are upstream problems
- Could be fixed in `mcp-remote` itself
- Repository: https://github.com/modelcontextprotocol/mcp-remote

### Current Best Practice for Cursor

Since `mcp-remote` is the **official Atlassian-recommended solution** for desktop clients, and there is no alternative:

1. **Accept the limitations** - Token file issues are inherent to the proxy architecture
2. **Use the workarounds** - `mcp-health` now detects running processes as validation fallback
3. **Toggle when needed** - Cursor MCP toggle is the most reliable re-auth method
4. **Monitor processes** - If `mcp-remote` is running, tokens are likely valid for MCP

## Key Concepts

### MCP-Scoped Tokens

**Important**: Atlassian OAuth tokens from `mcp-remote` are **MCP-scoped only**. This means:

- ✅ They work for MCP protocol communication
- ❌ They **do not** work with standard Atlassian REST APIs (e.g., `/me`, `/oauth/token/accessible-resources`)
- ⚠️ API validation will return `401 Unauthorized` even when tokens are valid for MCP

### Token Storage

Tokens are stored in the `MCP_REMOTE_CONFIG_DIR` with hash-prefixed filenames:

```
~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/
├── bbcf3c111998d8af66c1b0d7523c9a05_client_info.json
├── bbcf3c111998d8af66c1b0d7523c9a05_tokens.json
├── bbcf3c111998d8af66c1b0d7523c9a05_code_verifier.txt
└── bbcf3c111998d8af66c1b0d7523c9a05_lock.json
```

### In-Memory vs Persisted Tokens

`mcp-remote` maintains tokens **in memory** during its session:

- When Cursor starts the MCP server, `mcp-remote` loads tokens from disk
- During OAuth refresh, tokens are updated in memory
- Tokens **may not be immediately persisted** back to disk
- The persisted token file can become stale while the in-memory tokens remain valid

## Common Issues

### Issue 1: "Token Expired" but MCP Works in Cursor

**Symptoms:**
- `mcp-health` reports token as expired
- Atlassian MCP works perfectly in Cursor
- API validation returns 401 Unauthorized

**Root Cause:**
- The token file on disk is stale
- `mcp-remote` has fresh tokens in memory
- MCP-scoped tokens don't work with REST API validation

**Solution:**
`mcp-health` now detects running `mcp-remote` processes and reports tokens as valid if the process is active, even when API validation fails.

### Issue 2: Stale Tokens After Cursor Toggle

**Symptoms:**
- Toggle Atlassian MCP off/on in Cursor
- OAuth completes successfully in browser
- Token file timestamp updates but tokens are still invalid

**Root Cause:**
- `mcp-remote` may write incomplete token data during OAuth
- Token file lacks `issued_at` timestamp
- Refresh token may be invalid

**Solution:**
1. Kill stale `mcp-remote` processes:
   ```bash
   pkill -f "mcp-remote.*atlassian"
   ```

2. Remove stale token files:
   ```bash
   rm ~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/*_tokens.json
   ```

3. Toggle Atlassian MCP off/on in Cursor
4. Complete OAuth in browser

### Issue 3: Refresh Token Invalid

**Symptoms:**
- `mcp-health --auto-refresh` fails with "unauthorized_client - refresh_token is invalid"
- Manual refresh attempts fail

**Root Cause:**
- Refresh token has been revoked or expired
- Full re-authentication required

**Solution:**
Use one of these methods:

**Option 1: Via Cursor (Recommended)**
1. Open Cursor Settings → MCP Servers
2. Toggle OFF the Atlassian MCP server
3. Toggle it back ON
4. Complete OAuth in browser when prompted

**Option 2: Via mcp-health**
```bash
mcp-health check --server perimeter81-atlassian --reauth
```

**Option 3: Manual**
```bash
# Remove stale tokens
rm ~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/*_tokens.json

# Trigger OAuth
npx mcp-remote@0.1.30 https://mcp.atlassian.com/v1/sse
```

## Validation Strategy

`mcp-health` uses a multi-layered validation approach for Atlassian:

1. **Token File Check**: Verify token file exists and has required fields
2. **Expiration Check**: Check if token has expired based on stored metadata
3. **API Validation**: Attempt REST API call (expected to fail for MCP-scoped tokens)
4. **Process Check**: If API fails, check if `mcp-remote` process is running
5. **Fallback**: Report as valid if process is active, even with API failure

## Token File Format

Expected token file structure:

```json
{
  "access_token": "712020-...",
  "token_type": "bearer",
  "expires_in": 3300,
  "scope": "",
  "refresh_token": "712020-..."
}
```

**Note**: The file may lack `issued_at` or `expires_at` timestamps, making expiration calculation impossible. In such cases, `mcp-health` relies on API validation and process detection.

## Troubleshooting

### Check Token File

```bash
cat ~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/*_tokens.json
```

### Check Running Processes

```bash
ps aux | grep -i "mcp-remote.*atlassian"
```

### Check mcp-health Status

```bash
# Basic check
mcp-health check --server perimeter81-atlassian

# Verbose output
mcp-health check --server perimeter81-atlassian -v

# With auto-refresh
mcp-health check --server perimeter81-atlassian --auto-refresh

# With re-authentication
mcp-health check --server perimeter81-atlassian --reauth
```

### Manual Token Refresh

```bash
# Get current tokens
TOKENS=$(cat ~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/*_tokens.json)
REFRESH_TOKEN=$(echo $TOKENS | jq -r '.refresh_token')

# Attempt refresh (will fail if refresh_token is invalid)
curl -X POST https://auth.atlassian.com/oauth/token \
  -H "Content-Type: application/json" \
  -d "{
    \"grant_type\": \"refresh_token\",
    \"client_id\": \"YOUR_CLIENT_ID\",
    \"refresh_token\": \"$REFRESH_TOKEN\"
  }"
```

### Stale Processes Causing Auth Popup Spam

**Problem:** Constant Atlassian OAuth authentication popup tabs opening in browser, even though MCP is working.

**Symptoms:**
- Multiple browser tabs opening for Atlassian OAuth login
- "localhost refused to connect" errors in OAuth callback pages
- Slow MCP responses
- Browser showing authentication prompts repeatedly

**Root Cause:**
- Stale `mcp-remote` processes accumulating over time (can be 20+ processes from multiple days)
- Each process independently attempts token refresh, triggering multiple auth popups
- Processes persist across Cursor sessions and don't auto-terminate

**Diagnosis Commands:**

```bash
# Check for running mcp-remote processes (expect 1-2, problematic if 10+)
ps aux | grep -i "mcp-remote" | grep -v grep

# Count how many are running
ps aux | grep -i "mcp-remote" | grep -v grep | wc -l

# Check token storage directory
ls -la ~/.mcp-auth/mcp-remote-stable/

# Verify MCP_REMOTE_CONFIG_DIR is set (for token persistence)
echo $MCP_REMOTE_CONFIG_DIR
```

**Fix:**

```bash
# Kill all stale mcp-remote processes
pkill -f "mcp-remote"

# Verify they're gone
ps aux | grep -i "mcp-remote" | grep -v grep
```

**After Cleanup:**
- Next MCP call from Cursor will spawn fresh processes
- You'll get a one-time browser auth prompt
- Subsequent calls will use cached tokens

**Prevention:**

1. **Token persistence:** Ensure `MCP_REMOTE_CONFIG_DIR` is set in your shell config (already done in your Cursor mcp.json):
   ```bash
   export MCP_REMOTE_CONFIG_DIR="/Users/yosii/.mcp-auth/mcp-remote-stable"
   ```

2. **Periodic cleanup:** Run when auth popups become excessive:
   ```bash
   pkill -f "mcp-remote"
   ```

3. **Add to mcp-health helper** (TODO - can add `mcp-health cleanup` command)

## Best Practices

1. **Use Cursor Toggle for Re-auth**: The most reliable method is toggling the MCP server in Cursor settings
2. **Monitor Process Status**: If `mcp-remote` is running, tokens are likely valid for MCP
3. **Don't Rely on API Validation**: MCP-scoped tokens won't work with REST APIs
4. **Clean Up Stale Processes**: Kill old `mcp-remote` processes before re-authenticating
5. **Use `--reauth` for Full Re-auth**: When refresh fails, use `--reauth` instead of `--auto-refresh`

## Implementation Details

### Validator Code

The Atlassian validator (`src/mcp_health/validators/atlassian.py`) implements:

- Hash-prefixed token file detection (`*_tokens.json`)
- Process-based validation fallback
- MCP-scoped token awareness
- Enhanced error messages with toggle instructions

### Refresh Code

The OAuth refresher (`src/mcp_health/refresh/oauth.py`) implements:

- Token refresh via Atlassian OAuth API
- Invalid refresh token detection
- Automatic re-authentication via `npx mcp-remote`
- Stale token cleanup before re-auth

## Technical Deep Dive

### Why mcp-remote Exists

The Model Context Protocol (MCP) supports multiple transport mechanisms:
1. **stdio** - Standard input/output (for local processes)
2. **SSE** - Server-Sent Events over HTTP (for remote servers)

Atlassian's MCP server uses **SSE with OAuth 2.1**, which requires:
- HTTP connection management
- OAuth 2.1 PKCE flow (browser-based)
- Token storage and refresh
- Request/response proxying

Desktop IDEs typically only support **stdio** transport natively. `mcp-remote` bridges this gap by:
1. Accepting stdio from the IDE
2. Managing OAuth flow via browser
3. Maintaining HTTP/SSE connection to Atlassian
4. Proxying MCP messages bidirectionally

### Token Flow Diagram

```
┌─────────────┐                ┌──────────────┐                ┌─────────────────┐
│   Cursor    │                │  mcp-remote  │                │   Atlassian     │
│    (IDE)    │                │   (Proxy)    │                │  MCP Server     │
└──────┬──────┘                └──────┬───────┘                └────────┬────────┘
       │                              │                                 │
       │  1. Start MCP (stdio)        │                                 │
       ├─────────────────────────────>│                                 │
       │                              │  2. Check tokens                │
       │                              ├────────┐                        │
       │                              │        │ ~/.mcp-auth/           │
       │                              │<───────┘                        │
       │                              │                                 │
       │                              │  3. No valid tokens             │
       │                              │     Open browser for OAuth      │
       │                              ├────────┐                        │
       │                              │        │                        │
       │  4. User authenticates       │<───────┘                        │
       │     in browser               │                                 │
       │                              │  5. OAuth callback              │
       │                              │<────────────────────────────────┤
       │                              │                                 │
       │                              │  6. Store tokens                │
       │                              ├────────┐                        │
       │                              │        │ ~/.mcp-auth/           │
       │                              │<───────┘                        │
       │                              │                                 │
       │                              │  7. Connect SSE                 │
       │                              ├────────────────────────────────>│
       │                              │                                 │
       │  8. MCP ready                │                                 │
       │<─────────────────────────────┤                                 │
       │                              │                                 │
       │  9. MCP requests (stdio)     │                                 │
       ├─────────────────────────────>│  10. Proxy to SSE              │
       │                              ├────────────────────────────────>│
       │                              │                                 │
       │                              │  11. SSE response               │
       │  12. MCP response (stdio)    │<────────────────────────────────┤
       │<─────────────────────────────┤                                 │
```

### Why Token Files Become Stale

**Problem:** `mcp-remote` maintains tokens in **memory** for performance:

1. **Initial load**: Reads tokens from disk on startup
2. **Runtime**: Keeps tokens in memory, refreshes as needed
3. **Persistence**: May not write back to disk immediately
4. **Process death**: Tokens lost if process crashes before persisting

**Result:** Token file on disk can be hours/days old while in-memory tokens are fresh.

### Why API Validation Fails

**MCP-Scoped Tokens** have limited OAuth scopes:
- ✅ `read:jira-work` - Read Jira issues
- ✅ `read:confluence-content.summary` - Read Confluence pages
- ❌ `read:me` - Read user profile (not included)

Standard Atlassian REST API endpoints like `/me` or `/oauth/token/accessible-resources` require broader scopes that MCP tokens don't have.

**This is by design** - MCP tokens are intentionally scoped narrowly for security.

## Related Issues

- [mcp-remote#200](https://github.com/modelcontextprotocol/mcp-remote/issues/200) - Token persistence across version upgrades
- Atlassian OAuth tokens are scoped differently than standard API tokens
- `mcp-remote` keeps tokens in memory and may not persist immediately
- Official Atlassian MCP Server: https://github.com/atlassian/atlassian-mcp-server
- MCP Protocol Specification: https://modelcontextprotocol.io/

## Future Improvements

### Short-term (mcp-health)
1. **MCP-Native Validation**: Use MCP protocol to validate tokens instead of REST API
2. **Automatic Process Detection**: Integrate process monitoring into validation flow
3. **Better Error Messages**: More specific guidance based on detected issues

### Medium-term (mcp-remote upstream)
1. **Better Token Persistence**: Ensure tokens are always persisted immediately after refresh
2. **Token Expiration Tracking**: Add `issued_at` timestamp to persisted tokens
3. **Health Check Endpoint**: Provide a way to validate tokens without full MCP connection
4. **File Watching**: Detect when token files are deleted and trigger re-auth

### Long-term (Cursor/IDE)
1. **Native MCP OAuth Support**: Eliminate need for `mcp-remote` proxy
2. **Built-in Token Management**: Handle OAuth flows directly in IDE
3. **Secure Token Storage**: Use OS keychain/credential manager
4. **Automatic Token Refresh**: Background refresh without user intervention

## Comparison with Other Clients

### Claude Code (Anthropic Desktop App)
✅ **Advantages:**
- Native OAuth support
- Seamless token management
- No external processes
- Automatic token refresh
- No file synchronization issues

❌ **Disadvantages:**
- Proprietary (not open source)
- Limited to Anthropic's ecosystem
- Cannot customize MCP configuration as easily

### VS Code with Native MCP
✅ **Advantages:**
- First-party MCP support
- Better integration than external processes
- Large extension ecosystem
- Active development

❌ **Disadvantages:**
- Still uses `mcp-remote` for Atlassian
- Token issues may persist
- Less AI-focused than Cursor

### Cursor with mcp-remote
✅ **Advantages:**
- AI-first IDE
- Flexible MCP configuration
- Can use any MCP server
- Active AI features development

❌ **Disadvantages:**
- External `mcp-remote` process required
- Token file synchronization issues
- No native OAuth support
- Manual re-auth via toggle needed

## Recommendations

### For Individual Users
1. **Primary workflow**: Use Claude Code for Atlassian-heavy tasks
2. **Fallback**: Use Cursor with `mcp-health` monitoring
3. **Re-auth method**: Toggle MCP in Cursor when tokens expire
4. **Monitoring**: Run `mcp-health check --watch` for continuous monitoring

### For Teams
1. **Document the limitations**: Share this guide with team members
2. **Standardize on Claude Code**: For teams heavily using Jira/Confluence
3. **Monitor token health**: Use `mcp-health` in CI/CD pipelines
4. **File upstream issues**: Report problems to `mcp-remote` and Cursor teams

### For Tool Developers
1. **Implement native OAuth**: Don't rely on external proxies
2. **Use OS credential storage**: Keychain on macOS, Credential Manager on Windows
3. **Provide health checks**: Built-in token validation endpoints
4. **Document architecture**: Clear explanation of OAuth flow and token storage

