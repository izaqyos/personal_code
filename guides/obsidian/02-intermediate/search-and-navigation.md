# Search & Navigation Mastery

> Find anything in seconds. Navigate like a Vim power user.

---

## ⚡ The Speed Hierarchy

From fastest to slowest:

```
1. Hotkey to specific note     →  Instant (if you set it up)
2. Quick Switcher (Cmd+O)      →  <1 second (fuzzy search)
3. Search (Cmd+Shift+F)        →  1-3 seconds (full text)
4. Graph View (Cmd+G)          →  Visual exploration
5. File Explorer sidebar       →  Manual browsing (slowest)
```

**Goal:** Stay in the top 3 for 95% of navigation.

---

## 🔍 Quick Switcher — Your New Best Friend

### Open It
`Cmd+O` (like VS Code's `Cmd+P`)

### What It Does
- Fuzzy searches **file names**
- Shows recent files first
- Creates new files if no match

### Pro Tips

```
Type              Result
─────────────────────────────────────
meeting           → All files with "meeting"
1on1 sarah        → Fuzzy match "1on1" AND "sarah"  
2024-01           → All January 2024 notes
#python           → Files tagged python (with plugin)
```

### Keyboard Navigation
| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate results |
| `Enter` | Open selected |
| `Cmd+Enter` | Open in new pane |
| `Esc` | Close |

---

## 🔎 Global Search — Full Text Power

### Open It
`Cmd+Shift+F`

### Basic Search
```
python                    # Find "python" anywhere
"list comprehension"      # Exact phrase
python OR rust            # Either term
python -beginner          # Python but NOT beginner
```

### Advanced Operators

```
# Search in specific locations
path:daily/               # Only in daily/ folder
file:meeting              # File name contains "meeting"
file:.md                  # Only markdown files

# Search by content type
tag:#type/meeting         # Has this tag
line:(TODO)               # Line contains TODO
section:(## Action)       # In a section starting with "## Action"

# Combine operators
tag:#type/meeting path:2024/ line:(TODO)
# Meetings from 2024 with TODO items
```

### Search & Replace
1. Search for term
2. Click "Replace" toggle
3. Enter replacement
4. Replace one or all

---

## 🧭 In-File Navigation

### Command Palette
`Cmd+P` — The universal launcher

```
Type                      Result
─────────────────────────────────────
>                         # Commands only (like VS Code)
#                         # Search tags
^                         # Search headings in current file
```

### Outline View
- **Toggle:** Click outline icon in right sidebar
- **Hotkey:** Set one in Settings → Hotkeys → "Outline: Show outline"
- Shows all headings as a clickable TOC

### Heading Navigation (Vim Users)
With Vim mode enabled:
```
]]    # Next heading
[[    # Previous heading
gd    # Go to definition (follow link)
Ctrl+o # Go back
Ctrl+i # Go forward
```

---

## ⌨️ Essential Navigation Hotkeys

### Set These Up (Settings → Hotkeys)

| Action | Suggested Hotkey | Why |
|--------|------------------|-----|
| Quick switcher | `Cmd+O` | Already default |
| Command palette | `Cmd+P` | Already default |
| Global search | `Cmd+Shift+F` | Already default |
| Search current file | `Cmd+F` | Already default |
| Daily note | `Cmd+D` | Quick journal access |
| Toggle left sidebar | `Cmd+\` | More screen space |
| Toggle right sidebar | `Cmd+Shift+\` | Backlinks/outline |
| Navigate back | `Cmd+Alt+←` | History navigation |
| Navigate forward | `Cmd+Alt+→` | History navigation |
| Open link | `Alt+Enter` | Follow link under cursor |
| Graph view | `Cmd+G` | Visual exploration |

### Split Panes
| Action | Hotkey |
|--------|--------|
| Split right | `Cmd+\` then drag, or right-click tab |
| Split down | Right-click tab → Split down |
| Close pane | `Cmd+W` |
| Focus next pane | `Cmd+Tab` (set custom) |

---

## 🕸️ Graph View — Visual Navigation

### Open It
`Cmd+G` or click graph icon

### What You See
- **Nodes** = Notes
- **Edges** = Links between notes
- **Clusters** = Related topics
- **Orphans** = Unlinked notes (consider linking!)

### Graph Controls
```
Filters:
├── Search (filter visible nodes)
├── Tags (show/hide by tag)
├── Attachments (show/hide images, PDFs)
├── Existing files only
└── Orphans (show unlinked)

Display:
├── Arrows (show link direction)
├── Node size (by link count)
└── Colors (by folder, tag, or custom)
```

### Local Graph
- Shows connections for **current note only**
- Toggle in right sidebar or `Cmd+P` → "Graph: Open local graph"
- Great for understanding context

### Navigation in Graph
- **Click node** → Open note
- **Hover** → Preview
- **Drag** → Rearrange (temporary)
- **Scroll** → Zoom
- **Drag background** → Pan

---

## 🔗 Backlinks Panel — Contextual Discovery

### Open It
Right sidebar → Backlinks tab

### What It Shows
```
Backlinks to [[Current Note]]
├── Linked mentions (explicit [[links]])
│   └── Note A
│       "I learned about [[Current Note]] today"
│   └── Note B  
│       "See [[Current Note]] for details"
│
└── Unlinked mentions (text matches, not linked)
    └── Note C
        "The current note approach is..."
        [Link] ← Click to convert to link!
```

### Pro Tip: Convert Unlinked to Linked
When you see an unlinked mention:
1. Click the "Link" button
2. Obsidian auto-converts the text to `[[link]]`
3. Strengthens your graph!

---

## 🏃 Speed Workflows

### Workflow 1: Morning Startup
```
1. Cmd+D           → Open today's daily note
2. Review template → Set priorities
3. Cmd+O           → Jump to first task/project
```

### Workflow 2: During a Meeting
```
1. Cmd+N           → New note
2. Cmd+T           → Insert meeting template
3. [[link]]        → Link people, projects as you type
4. Cmd+S           → Auto-saved anyway, but habit
```

### Workflow 3: Finding That Thing
```
1. Cmd+O           → Try quick switcher first
2. No luck? Cmd+Shift+F → Full text search
3. Still lost? Cmd+G → Browse graph visually
```

### Workflow 4: Research Deep Dive
```
1. Open topic note
2. Cmd+Click links → Open in new pane
3. Tile panes side-by-side
4. Local graph open → See connections
5. Create new links as you discover relationships
```

---

## 🎯 Exercise: Navigation Drill

Time yourself on these tasks:

### Task 1: Quick Switch (Target: <3 seconds)
1. Open any note
2. `Cmd+O` → Type first 3 letters of another note
3. `Enter` to open

### Task 2: Search & Navigate (Target: <10 seconds)
1. `Cmd+Shift+F`
2. Search for a word you know exists
3. Click result to jump there

### Task 3: Backlink Discovery (Target: <15 seconds)
1. Open a note that's linked from others
2. Open backlinks panel (right sidebar)
3. Click a backlink to navigate there
4. `Cmd+Alt+←` to go back

### Task 4: Split Pane Workflow (Target: <20 seconds)
1. Open a note
2. `Cmd+Click` a link to open in new pane
3. Arrange panes side-by-side
4. `Cmd+W` to close the extra pane

---

## 🔮 Level Up: Plugins for Navigation

These community plugins supercharge navigation (covered in plugins section):

| Plugin | What It Does |
|--------|--------------|
| **Quick Switcher++** | Search by tags, headings, symbols |
| **Omnisearch** | Better full-text search with ranking |
| **Another Quick Switcher** | More fuzzy matching options |
| **Hover Editor** | Edit linked notes in popover |
| **Strange New Worlds** | Enhanced backlinks with more context |

---

## Next
→ [[yaml-frontmatter-metadata]] — Structure your notes with metadata


