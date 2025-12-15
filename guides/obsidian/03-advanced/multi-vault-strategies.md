# Multi-Vault Strategies

> When one vault isn't enough — organize, separate, and scale your knowledge.

---

## 🤔 Why Multiple Vaults?

### Reasons to Split

| Reason | Example |
|--------|---------|
| **Privacy** | Work vs personal (different employers) |
| **Context** | Projects with different stakeholders |
| **Performance** | Massive vaults slow down |
| **Sync** | Different sync strategies per vault |
| **Collaboration** | Team vault vs individual |
| **Portability** | Share subset without exposing all |

### Reasons to Keep One Vault

| Reason | Explanation |
|--------|-------------|
| **Linking** | Cross-domain connections |
| **Search** | One place to find everything |
| **Simplicity** | Less cognitive overhead |
| **Plugins** | Configure once |
| **Backups** | Single backup strategy |

---

## 📊 Common Multi-Vault Patterns

### Pattern 1: Work + Personal

```
~/vaults/
├── work/           # Company knowledge
│   ├── projects/
│   ├── meetings/
│   ├── 1on1s/
│   └── team/
│
└── personal/       # Life & hobbies
    ├── journal/
    ├── learning/
    ├── health/
    └── finance/
```

**Benefits:**
- Clear separation for employer policies
- Different backup/sync strategies
- No risk of sharing personal with work

### Pattern 2: Project-Based

```
~/vaults/
├── main/           # Daily notes, general knowledge
├── project-alpha/  # Specific project
├── project-beta/   # Another project
└── archive/        # Completed projects
```

**Benefits:**
- Share project vaults with collaborators
- Archive entire projects easily
- Project-specific plugins/settings

### Pattern 3: Public + Private

```
~/vaults/
├── public/         # Publishable content
│   ├── blog/
│   ├── tutorials/
│   └── resources/
│
└── private/        # Personal notes
    ├── journal/
    ├── ideas/
    └── drafts/
```

**Benefits:**
- Publish directly from public vault
- No risk of leaking private content
- Different CSS/themes per vault

### Pattern 4: Hub + Satellite

```
~/vaults/
├── hub/            # Central index, MOCs
│   └── indexes/    # Links to all other vaults
│
├── work/           # Satellite vault
├── learning/       # Satellite vault
└── projects/       # Satellite vault
```

**Benefits:**
- Central navigation point
- Vaults remain independent
- Easy to add/remove satellites

---

## 🔧 Setting Up Multiple Vaults

### Create New Vault

1. **Obsidian:**
   ```
   Open another vault (bottom left) → Create new vault
   ```

2. **Manual:**
   ```bash
   mkdir -p ~/vaults/new-vault
   # Open folder as vault in Obsidian
   ```

### Vault Switcher

```
Obsidian → Open another vault → Choose vault
```

**Hotkey (custom):** `Cmd+Shift+V`

### Quick Access Tips

| Method | How |
|--------|-----|
| Alias | `alias work="open -a Obsidian ~/vaults/work"` |
| macOS Shortcuts | Create Shortcuts app automation |
| Alfred/Raycast | Create workflow to open specific vault |

---

## ⚙️ Per-Vault Configuration

Each vault has its own `.obsidian/` folder:

```
vault/
├── .obsidian/
│   ├── app.json           # App settings
│   ├── appearance.json    # Theme, fonts
│   ├── hotkeys.json       # Custom hotkeys
│   ├── plugins/           # Installed plugins
│   │   ├── dataview/
│   │   ├── templater/
│   │   └── obsidian-git/
│   ├── snippets/          # CSS snippets
│   └── templates/         # Only if using core templates
└── ... notes ...
```

### Sync Settings Between Vaults

**Option 1: Manual Copy**
```bash
cp -r ~/vaults/main/.obsidian/plugins ~/vaults/work/.obsidian/
```

**Option 2: Symbolic Links**
```bash
# Share plugins between vaults
ln -s ~/vaults/main/.obsidian/plugins ~/vaults/work/.obsidian/plugins

# Share snippets
ln -s ~/vaults/main/.obsidian/snippets ~/vaults/work/.obsidian/snippets
```

**Option 3: Git Submodules**
```bash
# In each vault's .obsidian/
git submodule add git@github.com:user/obsidian-plugins plugins
```

---

## 🔗 Cross-Vault Linking

### The Challenge

Obsidian links are vault-relative — can't directly link between vaults.

### Solution 1: URI Scheme

```markdown
[Link to work note](obsidian://open?vault=work&file=projects/alpha)
```

Format:
```
obsidian://open?vault=VAULT_NAME&file=PATH/TO/FILE
```

### Solution 2: File URLs

```markdown
[Local file link](file:///Users/me/vaults/other/note.md)
```

⚠️ Won't render in Obsidian, but works in some contexts.

### Solution 3: Hub Note

Create index notes that use URI links:

```markdown
# 🏠 Vault Hub

## My Vaults
- [Work Vault](obsidian://open?vault=work)
- [Personal Vault](obsidian://open?vault=personal)
- [Learning Vault](obsidian://open?vault=learning)

## Quick Links
- [Current Project](obsidian://open?vault=work&file=projects/current)
- [Today's Journal](obsidian://open?vault=personal&file=journal/2024-01-15)
```

---

## 📁 Folder-Based Alternative

Instead of multiple vaults, use strict folder separation:

```
vault/
├── _WORK/              # Prefix for sorting
│   ├── projects/
│   ├── meetings/
│   └── team/
│
├── _PERSONAL/
│   ├── journal/
│   └── health/
│
├── _LEARNING/
│   └── courses/
│
└── _SYSTEM/
    ├── templates/
    └── daily/
```

### Benefits

- Single search across everything
- Links work naturally
- One backup strategy

### Isolation with Dataview

```dataview
TABLE file.mtime as "Modified"
FROM "_WORK"
WHERE status = "active"
```

---

## 🔄 Vault-Specific Sync Strategies

| Vault | Sync Method | Reason |
|-------|-------------|--------|
| Work | Company GitHub | Policy compliance |
| Personal | Obsidian Sync | Seamless mobile |
| Archive | Local only | Rarely accessed |
| Public | GitHub Pages | Publishing |

### Git Configuration Per Vault

```bash
# Work vault — company identity
cd ~/vaults/work
git config user.email "you@company.com"
git remote add origin git@github.com:company/team-notes.git

# Personal vault — personal identity
cd ~/vaults/personal
git config user.email "you@personal.com"
git remote add origin git@github.com:you/personal-vault.git
```

---

## 📱 Mobile Considerations

### Multi-Vault on Mobile

| Platform | Support |
|----------|---------|
| iOS | Vault switcher, iCloud-synced vaults |
| Android | Vault switcher, local vaults |

### Recommended Mobile Strategy

```
Primary vault (synced):  personal/
Secondary vault:         work/ (if needed)
```

**Tip:** Keep mobile to 1-2 vaults for simplicity.

---

## 🎯 Migration Between Vaults

### Move Notes

```bash
# Move folder to another vault
mv ~/vaults/main/projects/completed ~/vaults/archive/2023/

# Update links (manual or with plugin)
```

### Obsidian Tools

1. **Move file** (built-in): Right-click → Move file to...
2. **Note Refactor** plugin: Bulk operations
3. **Shell script**: For large migrations

### Link Fixer Script

```bash
#!/bin/bash
# Fix broken links after moving notes

OLD_PATH="projects/alpha"
NEW_PATH="archive/2023/alpha"

find ~/vaults/main -name "*.md" -exec \
    sed -i '' "s|\[\[$OLD_PATH|\[\[$NEW_PATH|g" {} \;
```

---

## 📊 Decision Framework

### Should You Split?

| Question | Yes → Split | No → Keep |
|----------|-------------|-----------|
| Different access control? | ✅ | |
| Different collaborators? | ✅ | |
| Performance issues? | ✅ | |
| Rarely need cross-links? | ✅ | |
| Same sync everywhere? | | ✅ |
| Heavy cross-linking? | | ✅ |
| Single search needed? | | ✅ |

### Recommended Starting Point

```
Start: Single vault with folders
Split when: Clear need emerges
Strategy: Work vs Personal first
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong vault opens | Check default vault setting |
| Plugins missing | Install per-vault or use symlinks |
| URI links broken | Encode spaces as `%20` |
| Sync conflicts | Ensure only one device edits at a time |
| Settings not syncing | .obsidian is vault-specific |

---

## Summary

Multi-vault strategies:

| Pattern | Use Case |
|---------|----------|
| **Work + Personal** | Employment separation |
| **Project-based** | Collaboration, archiving |
| **Public + Private** | Publishing |
| **Hub + Satellite** | Central navigation |
| **Single with folders** | Simplicity, cross-linking |

**Key principle:** Start with one vault. Split only when you have a clear reason.

---

## Next Steps
→ [[publishing-and-sharing]] — Share your notes publicly
→ [[git-integration]] — Version control each vault

