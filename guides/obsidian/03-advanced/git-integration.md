# Git Integration for Version Control

> Track every change, sync across devices, and never lose a note.

---

## 🔧 Why Git for Obsidian?

Your vault is just markdown files — perfect for Git:
- **Version history** — See what changed and when
- **Branching** — Experiment with vault reorganization
- **Backup** — Push to GitHub/GitLab for cloud safety
- **Sync** — Alternative to Obsidian Sync
- **Collaboration** — Shared team vaults

**Developer advantage:** You already know Git. Use those skills.

---

## 🚀 Manual Git Setup

### Initialize Repository

```bash
cd /path/to/your/vault
git init
```

### Create .gitignore

```bash
# .gitignore for Obsidian vault

# Obsidian workspace and cache
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/recent-files-obsidian/data.json
.obsidian/cache

# System files
.DS_Store
.trash/
*.tmp

# Optional: Ignore plugin data that changes frequently
# .obsidian/plugins/*/data.json

# Optional: Large binary files
# *.pdf
# *.png
# *.jpg
```

### Initial Commit

```bash
git add .
git commit -m "Initial vault commit"
```

### Connect to Remote

```bash
# GitHub
git remote add origin git@github.com:username/obsidian-vault.git
git branch -M main
git push -u origin main

# Or GitLab
git remote add origin git@gitlab.com:username/obsidian-vault.git
git push -u origin main
```

---

## 🔌 Obsidian Git Plugin

### Installation

```
Settings → Community plugins → Browse → "Obsidian Git" → Install → Enable
```

### Configuration

```
Settings → Obsidian Git
```

| Setting | Recommended |
|---------|-------------|
| Vault backup interval | 10-30 minutes |
| Auto pull on startup | ✅ Enable |
| Auto push after backup | ✅ Enable |
| Commit message format | `vault backup: {{date}}` |
| Date format | `YYYY-MM-DD HH:mm` |

### Key Commands

Access via Command Palette (`Cmd+P`):

| Command | Description |
|---------|-------------|
| Obsidian Git: Commit | Commit staged changes |
| Obsidian Git: Push | Push to remote |
| Obsidian Git: Pull | Pull from remote |
| Obsidian Git: Create backup | Commit and push |
| Obsidian Git: Open source control | View changed files |
| Obsidian Git: Open history | View git log |

### Recommended Hotkeys

```
Cmd+Shift+K → Obsidian Git: Create backup
Cmd+Shift+P → Obsidian Git: Pull
```

---

## 📱 Mobile Sync with Git

### Option 1: Working Copy (iOS)

1. **Working Copy app** (iOS Git client)
2. Clone your vault repository
3. Set up Obsidian to use Working Copy folder
4. Manual or scheduled sync

### Option 2: Termux (Android)

```bash
# Install Termux from F-Droid
pkg install git
cd /storage/emulated/0/
git clone git@github.com:username/obsidian-vault.git
```

### Option 3: iSH (iOS)

```bash
# Install iSH app
apk add git openssh
git clone git@github.com:username/obsidian-vault.git
```

**Note:** Mobile Git workflows are more manual than desktop.

---

## 🔄 Sync Workflow

### Daily Workflow

```
Morning:
1. Open Obsidian → Auto-pull on startup
2. Work on notes throughout day
3. Auto-backup every 10-30 minutes

Evening:
1. Cmd+Shift+K → Manual backup before closing
2. Changes pushed to remote
```

### Multi-Device Sync

```
Device A:                    Device B:
┌─────────────┐              ┌─────────────┐
│  Edit notes │              │  Edit notes │
│      ↓      │              │      ↓      │
│   Commit    │              │   Commit    │
│      ↓      │              │      ↓      │
│    Push     │──────────────│    Pull     │
└─────────────┘     ←        └─────────────┘
                    GitHub
                      ↓
              ┌─────────────┐
              │   Device C  │
              │    Pull     │
              └─────────────┘
```

---

## ⚠️ Handling Conflicts

### When Conflicts Happen

```
- Edited same file on two devices before syncing
- Auto-backup ran while you were mid-edit
- Network issues caused push/pull mismatch
```

### Resolution Steps

1. **Pull first** — Get remote changes
2. **Open conflicted files** — Git marks with `<<<<<<<`
3. **Resolve manually** — Choose correct content
4. **Commit resolution** — Complete the merge

### Conflict Markers

```markdown
<<<<<<< HEAD
Your local changes here
=======
Remote changes here
>>>>>>> origin/main
```

### Prevention Tips

| Tip | How |
|-----|-----|
| Pull before working | Auto-pull on startup |
| Push frequently | Short backup intervals |
| Avoid same-file edits | Coordinate with collaborators |
| Use atomic notes | Smaller files = fewer conflicts |

---

## 📊 Git Workflows for Different Use Cases

### Solo Personal Vault

```
main branch only
Auto-commit every 10 min
Auto-push on commit
Pull on startup
```

### Team Shared Vault

```
main: Production vault
feature/*: New content development
Pull request for major changes
Designated merge owner
```

### Work + Personal Split

```
Repo 1: work-vault (private)
Repo 2: personal-vault (private)
Separate Git identities if needed
```

---

## 🔧 Advanced Git Configuration

### Custom Commit Messages

```
Settings → Obsidian Git → Commit message format
```

Templates:
```
vault backup: {{date}}
auto: {{hostname}} {{date}}
{{numFiles}} files changed
```

### Exclude Specific Files

Add to `.gitignore`:
```gitignore
# Private notes
private/
journal/personal/

# Large attachments
attachments/*.mp4
attachments/*.zip
```

### Git Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Ensure no secrets are committed

if grep -rn "API_KEY\|PASSWORD\|SECRET" --include="*.md" .; then
    echo "Error: Potential secret found in commit"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 🔐 Security Considerations

### Private Vaults

```bash
# Ensure GitHub repo is private
gh repo edit --visibility private
```

### Sensitive Content

| Approach | Method |
|----------|--------|
| Exclude entirely | Add to `.gitignore` |
| Encrypt sensitive notes | git-crypt or transcrypt |
| Separate vault | Keep private content separate |
| Environment variables | For any API keys in scripts |

### SSH Keys

```bash
# Use SSH, not HTTPS for push
git remote set-url origin git@github.com:username/vault.git

# Generate key if needed
ssh-keygen -t ed25519 -C "your@email.com"
```

---

## 📋 Troubleshooting

| Issue | Solution |
|-------|----------|
| Push rejected | Pull first, resolve conflicts |
| Large file errors | Add to `.gitignore`, use Git LFS |
| Auth failures | Check SSH key, token expiration |
| Slow operations | Too many large files — consider LFS |
| Plugin not working | Check git is in PATH |

### Check Git Status

```bash
cd /path/to/vault
git status
git log --oneline -5
```

### Reset to Remote

```bash
# Nuclear option — reset local to match remote
git fetch origin
git reset --hard origin/main
```

---

## 🆚 Git vs Obsidian Sync

| Feature | Git | Obsidian Sync |
|---------|-----|---------------|
| Cost | Free (self-hosted) | $10/month |
| Setup | Manual | One-click |
| Version history | Full Git history | 1 year |
| Conflict resolution | Manual (Git-style) | Automatic |
| End-to-end encryption | Optional | ✅ Built-in |
| Mobile sync | Requires setup | ✅ Seamless |
| Selective sync | .gitignore | Excluded folders |
| Offline support | ✅ Full | ✅ Full |

**Recommendation:**
- Git: Developers comfortable with Git, need free solution
- Obsidian Sync: Less technical users, seamless mobile

---

## 🎯 My Git Workflow

```bash
# .obsidian/scripts/vault-backup.sh

#!/bin/bash
cd ~/vaults/main

# Stage all changes
git add -A

# Commit with timestamp
git commit -m "vault backup: $(date '+%Y-%m-%d %H:%M')"

# Push to remote
git push origin main

echo "Vault backed up successfully"
```

Hotkey: `Cmd+Shift+K` → Run this script via QuickAdd/Templater.

---

## Summary

Git integration provides:
- 📜 **Complete history** — Every change tracked
- 🔄 **Multi-device sync** — Via GitHub/GitLab
- 🔒 **Backup** — Remote copy of your vault
- 🤝 **Collaboration** — Shared team vaults
- 🆓 **Free** — No subscription needed

**Setup checklist:**
1. ✅ Initialize git in vault
2. ✅ Create `.gitignore`
3. ✅ Install Obsidian Git plugin
4. ✅ Configure auto-backup interval
5. ✅ Set up remote repository
6. ✅ Test push/pull workflow

---

## Next Steps
→ [[multi-vault-strategies]] — Organize multiple vaults
→ [[publishing-and-sharing]] — Share your notes publicly

