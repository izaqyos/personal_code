# Obsidian 101 — Foundations

> Everything you need to get started with Obsidian as a developer.

---

## 📥 1. Installation

### macOS (your setup)
```bash
# Option 1: Homebrew (recommended for devs)
brew install --cask obsidian

# Option 2: Direct download
# https://obsidian.md/download
```

### Verify Installation
After installing, Obsidian will prompt you to create or open a **vault**.

---

## 🗃️ 2. Understanding the Vault

A **vault** is simply a folder on your filesystem. That's it. No proprietary format, no database — just a directory of `.md` files.

### Why This Matters for Developers
```
your-vault/
├── .obsidian/          # Settings, plugins, themes (gitignore or track)
├── notes/
│   ├── daily/
│   └── projects/
├── templates/
└── attachments/
```

- **Plain text** → Version control with Git ✅
- **Portable** → Move between machines, editors, apps
- **Future-proof** → Your notes outlive any app
- **Editable anywhere** → NeoVIM, VS Code, Cursor, even `cat`

### Creating Your First Vault

1. Launch Obsidian
2. Click **"Create new vault"**
3. Choose a location (I recommend inside a Git repo)
4. Name it (e.g., `knowledge-base`, `second-brain`, `pkm`)

**Pro tip:** Create the vault inside an existing Git repo for instant backup:
```bash
mkdir -p ~/work/git/personal_code/notes/obsidian-vault
cd ~/work/git/personal_code/notes/obsidian-vault
git init
```

---

## 🔗 3. Core Concepts

### Notes
- Every note is a `.md` (Markdown) file
- File name = Note title
- No hierarchy required — flat is fine, structure with links

### Links — The Heart of Obsidian

```markdown
# Wiki-style links (Obsidian default)
[[note-name]]
[[note-name|display text]]
[[note-name#heading]]

# Standard Markdown links (also work)
[display text](note-name.md)
```

**Why links matter:**
- Create connections between ideas
- Build a knowledge graph organically
- Enable serendipitous rediscovery

### Backlinks
When you link `[[Note A]]` from Note B, Note A automatically shows Note B in its **backlinks panel**.

```
Note A ←── linked from ←── Note B
          (backlink)
```

This is bi-directional linking. You don't need to manually maintain "see also" sections.

### Graph View
Press `Cmd+G` (or click the graph icon) to visualize all your notes and their connections.

- Nodes = Notes
- Edges = Links
- Clusters = Related concepts

**Developer analogy:** Think of it as a dependency graph for your knowledge.

---

## ✍️ 4. Markdown in Obsidian

Obsidian uses standard Markdown with some extensions:

### Standard Markdown
```markdown
# Heading 1
## Heading 2
### Heading 3

**bold** and *italic* and ~~strikethrough~~

- Bullet list
- Another item
  - Nested item

1. Numbered list
2. Second item

> Blockquote

`inline code`

​```python
def code_block():
    return "syntax highlighted"
​```

[Link text](https://url.com)
![Image alt](path/to/image.png)

| Table | Header |
|-------|--------|
| Cell  | Cell   |
```

### Obsidian Extensions
```markdown
# Internal links
[[Another Note]]
[[Note#Specific Heading]]

# Embeds (transclusion)
![[embedded-note]]
![[note#section]]
![[image.png]]

# Tags
#tag #nested/tag

# Callouts (admonitions)
> [!note]
> This is a note callout

> [!warning]
> This is a warning

> [!tip]
> Pro tip here

# Task lists
- [ ] Unchecked task
- [x] Completed task

# Footnotes
Here's a statement[^1]
[^1]: This is the footnote

# Comments (won't render)
%%This is a hidden comment%%

# Math (LaTeX)
Inline: $E = mc^2$
Block:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

---

## ⌨️ 5. Essential Keyboard Shortcuts

As a Vim user, you'll appreciate these. Obsidian also has a **Vim mode** (Settings → Editor → Vim key bindings).

### Navigation
| Action | Shortcut |
|--------|----------|
| Quick switcher (fuzzy find files) | `Cmd+O` |
| Command palette | `Cmd+P` |
| Search in all files | `Cmd+Shift+F` |
| Search in current file | `Cmd+F` |
| Toggle left sidebar | `Cmd+\` |
| Toggle right sidebar | `Cmd+Shift+\` |
| Graph view | `Cmd+G` |
| Back (navigate history) | `Cmd+Alt+←` |
| Forward | `Cmd+Alt+→` |

### Editing
| Action | Shortcut |
|--------|----------|
| New note | `Cmd+N` |
| Create link | `Cmd+K` (on selection) |
| Toggle checkbox | `Cmd+Enter` |
| Toggle bold | `Cmd+B` |
| Toggle italic | `Cmd+I` |
| Toggle code | `Cmd+`` ` |
| Indent | `Tab` |
| Outdent | `Shift+Tab` |

### Pro Tips
| Action | Shortcut |
|--------|----------|
| Open link under cursor | `Cmd+Click` or `Alt+Enter` |
| Open in new pane | `Cmd+Shift+Click` |
| Follow link (Vim mode) | `gd` |
| Close current pane | `Cmd+W` |

---

## ⚙️ 6. Essential Settings

Open Settings: `Cmd+,`

### Editor Settings
- **Vim key bindings** → ON (you'll love this)
- **Spell check** → Your preference
- **Auto pair brackets** → ON
- **Default view mode** → Source mode (if you prefer raw markdown)

### Files & Links
- **Default location for new notes** → Same folder as current file, or specific folder
- **New link format** → Relative path (better for Git portability)
- **Use [[Wikilinks]]** → ON (cleaner syntax)

### Appearance
- **Theme** → Browse community themes (developer favorites: Minimal, Things, Prism)
- **Font** → Monospace fonts work great (JetBrains Mono, Fira Code)

### Core Plugins to Enable
These are built-in, just toggle them on:
- ✅ **Backlinks**
- ✅ **Graph view**
- ✅ **Quick switcher**
- ✅ **Command palette**
- ✅ **Templates**
- ✅ **Daily notes**
- ✅ **Outline** (table of contents)
- ✅ **Page preview** (hover to preview links)
- ✅ **Slash commands**

---

## 📱 7. Mobile & Sync Options

### Free Options
| Method | Pros | Cons |
|--------|------|------|
| **iCloud** (macOS/iOS) | Free, automatic | iOS only, occasional conflicts |
| **Git** (manual/automated) | Version history, free | Requires setup, not real-time |
| **Syncthing** | Free, P2P, cross-platform | DIY setup |

### Paid Options
| Method | Cost | Pros |
|--------|------|------|
| **Obsidian Sync** | $4/mo | Official, reliable, E2E encrypted, version history |
| **Obsidian Publish** | $8/mo | Public/private website from your vault |

### Git Sync Setup (Developer's Choice)
```bash
# In your vault directory
git init
echo ".obsidian/workspace.json" >> .gitignore
echo ".obsidian/workspace-mobile.json" >> .gitignore

# Initial commit
git add .
git commit -m "Initial vault setup"

# Add remote
git remote add origin git@github.com:username/vault.git
git push -u origin main
```

The **Obsidian Git** plugin can automate commits and pushes.

---

## 🚀 Quick Start Workflow

1. **Create a new note**: `Cmd+N`
2. **Name it** something meaningful
3. **Write** in Markdown
4. **Link** to related concepts with `[[double brackets]]`
5. **Use the graph** (`Cmd+G`) to see connections grow
6. **Search** (`Cmd+O`) to jump between notes instantly

---

## 🎯 Your First Exercise

Create these 3 notes and link them together:

### Note 1: `python-learning.md`
```markdown
# Python Learning

My Python practice project: `/Users/yosii/work/git/personal_code/code/practice/python`

## Topics to Cover
- [[data-structures]]
- [[algorithms]]
- OOP concepts
- Async programming

## Resources
- [[leetcode-prep]]
```

### Note 2: `leetcode-prep.md`
```markdown
# LeetCode Prep

Project location: `/Users/yosii/work/git/personal_code/code/interviewQs/full_leetcode_export`

## Strategy
- Start with [[easy-problems]]
- Focus on [[data-structures]]
- Time-boxed practice sessions

## Patterns to Master
- Two pointers
- Sliding window
- BFS/DFS
- Dynamic programming
```

### Note 3: `learning-dashboard.md`
```markdown
# Learning Dashboard

## Active Learning Tracks
1. [[python-learning]] - Practice project
2. [[leetcode-prep]] - Interview preparation
3. [[obsidian-guide]] - PKM mastery
4. Networking refresher (CCNA) - *Coming soon*

## Weekly Review
- [ ] Python practice session
- [ ] Solve 3 LeetCode problems
- [ ] Obsidian workflow refinement
```

Now open the **Graph View** (`Cmd+G`) and watch your knowledge network form! 🎉

---

## Next Steps

Once you're comfortable with these basics:
- → [[02-intermediate/linking-strategies]] - When to use tags vs folders vs links
- → [[02-intermediate/templates]] - Automate note creation
- → [[04-plugins/top-20-plugins]] - Supercharge your workflow

---

*Foundations complete. You're ready to build your second brain.* 🧠

