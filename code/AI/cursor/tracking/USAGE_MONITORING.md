# Cursor Usage Monitoring Guide

## Quick Check Methods

### 1. **In Cursor IDE** (Easiest)
- **Settings → Account**: Shows plan type and current usage
- **Status Bar** (bottom right): May show remaining requests
- **Command Palette** (`Cmd+Shift+P`): Search "Usage" or "Account"

### 2. **Online Dashboard**
Visit: https://cursor.sh/settings
- Login with your corporate account (yosii@checkpoint.com)
- View detailed usage breakdown
- Check plan status and limits

### 3. **Command Line Script**
```bash
python3 code/AI/cursor/usage_tracker.py
```

## Corporate Pro Plan Limits (Expected)

| Limit Type | Amount |
|------------|--------|
| **Fast Requests** | ~500/day |
| **Slow Requests** | ~2000/day |
| **Monthly** | Higher limits than free tier |

**Fast Requests**: Composer chat, code generation  
**Slow Requests**: Codebase search, large context operations

## Verify Your Plan Status

### Check Account Email
```bash
# In Cursor settings, verify you're logged in as:
yosii@checkpoint.com  # ✅ Corporate account
# NOT:
izaqyos@gmail.com     # ❌ Personal account
```

### Check Settings File
```bash
cat ~/Library/Application\ Support/Cursor/User/settings.json | grep -i cursor
```

Should see:
```json
"cursor.composer.usageSummaryDisplay": "always"
```

## What Counts Toward Limits

✅ **Counts:**
- Composer chat messages
- Code generation requests  
- Codebase searches (semantic search)
- File operations via Composer

❌ **Doesn't Count:**
- Regular typing/editing
- Git operations
- Terminal commands
- File saves (normal editing)

## Troubleshooting

### If Usage Seems Wrong

1. **Verify Account**: Settings → Account → Check email
2. **Check Plan**: Should show "Corporate Pro" or "Business"
3. **Contact IT**: If plan doesn't match, contact Checkpoint IT
4. **Check Billing**: Corporate admin may need to verify subscription

### If You Hit Limits

- **Wait**: Daily reset usually at midnight UTC
- **Use Slow Mode**: Fewer tokens per request
- **Batch Requests**: Combine multiple operations
- **Contact Admin**: Corporate plans can have limits adjusted

## Monitoring Script Usage

The `usage_tracker.py` script:
- Checks Cursor logs for activity patterns
- Attempts to read account info from storage
- Saves usage history to `~/.cursor_usage.json`

Run daily to track patterns:
```bash
# Add to cron or run manually
python3 code/AI/cursor/usage_tracker.py >> ~/.cursor_usage.log
```

## Notes

- Cursor doesn't expose a public API for usage stats
- Most reliable: Check in-app Settings → Account
- Corporate plans may have custom limits set by admin
- Usage resets daily (not monthly)

