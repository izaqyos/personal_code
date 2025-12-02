# Top Community Plugins — The Power User's Arsenal

> Transform Obsidian from a note-taking app into a complete productivity system.

---

## 🔧 Installing Community Plugins

### First-Time Setup

1. **Enable Community Plugins**
   ```
   Settings → Community plugins → Turn on community plugins
   ```
   You'll see a security warning — this is expected. Community plugins run code, so only install trusted ones.

2. **Browse & Install**
   ```
   Settings → Community plugins → Browse → Search for plugin → Install → Enable
   ```

3. **Restart if Needed**
   Some plugins require an Obsidian restart (`Cmd/Ctrl + R` or quit and reopen).

### Plugin Management Tips

```
Settings → Community plugins → Installed plugins
```
- **Toggle** individual plugins on/off
- **Check for updates** regularly (or enable auto-update)
- **Uninstall** removes the plugin completely

---

## 🏆 The Essential 15

Here are the must-have plugins, organized by category:

| # | Plugin | Category | Why You Need It |
|---|--------|----------|-----------------|
| 1 | Dataview | Query | Query notes like a database |
| 2 | Templater | Automation | Advanced templating with logic |
| 3 | Tasks | Productivity | Powerful task management |
| 4 | Calendar | Navigation | Visual daily notes calendar |
| 5 | Kanban | Project Mgmt | Trello-style boards |
| 6 | Excalidraw | Visual | Hand-drawn diagrams |
| 7 | Advanced Tables | Editing | Better markdown tables |
| 8 | Periodic Notes | Organization | Weekly/monthly notes |
| 9 | QuickAdd | Capture | Fast note creation |
| 10 | Obsidian Git | Backup | Version control sync |
| 11 | Omnisearch | Search | Supercharged search |
| 12 | Linter | Formatting | Auto-format markdown |
| 13 | Commander | Customization | Custom buttons/menus |
| 14 | Natural Language Dates | Input | Type "tomorrow" → date |
| 15 | Paste URL into Selection | Links | Clean link pasting |

---

## 1. 📊 Dataview — Query Your Notes Like SQL

> **The most powerful plugin.** Turn your vault into a queryable database.

### Installation
```
Community plugins → Browse → "Dataview" → Install → Enable
```

### What It Does
Write queries to automatically generate lists, tables, and task views from your notes' metadata.

### Basic Usage

#### List All Notes with a Tag
````markdown
```dataview
LIST
FROM #status/active
```
````

#### Table of Team Members
````markdown
```dataview
TABLE role, team, last-1on1
FROM "people"
SORT last-1on1 DESC
```
````

Requires YAML frontmatter in your people notes:
```yaml
---
role: Senior Developer
team: Backend
last-1on1: 2024-01-15
---
```

#### All Tasks Due This Week
````markdown
```dataview
TASK
FROM "projects"
WHERE due >= date(today) AND due <= date(today) + dur(7 days)
SORT due ASC
```
````

### Developer-Oriented Examples

#### Project Dashboard
````markdown
```dataview
TABLE status, owner, deadline
FROM #type/project
WHERE status != "done"
SORT deadline ASC
```
````

#### Meeting Notes by Person
````markdown
```dataview
LIST
FROM [[Sarah Chen]]
WHERE contains(tags, "type/meeting")
SORT file.ctime DESC
LIMIT 10
```
````

#### Learning Progress Tracker
````markdown
```dataview
TABLE 
  choice(status = "done", "✅", choice(status = "in-progress", "🔄", "⏳")) as Progress,
  hours as "Hours Spent",
  last-session as "Last Session"
FROM #type/learning
SORT last-session DESC
```
````

### Settings to Configure
```
Settings → Dataview →
  ✓ Enable JavaScript Queries (for advanced use)
  ✓ Enable Inline Queries
  Date Format: yyyy-MM-dd
```

### Pro Tips
- Use `dv.pages()` in DataviewJS for complex logic
- Combine with Templater for dynamic dashboards
- Create a "Dataview Snippets" note for reusable queries

---

## 2. ⚡ Templater — Advanced Templating

> Beyond basic templates — add logic, prompts, and automation.

### Installation
```
Community plugins → Browse → "Templater" → Install → Enable
```

### What It Does
Create smart templates with variables, prompts, date math, and JavaScript execution.

### Basic Setup
```
Settings → Templater →
  Template folder location: templates
  ✓ Trigger Templater on new file creation
```

### Template Syntax Comparison

| Feature | Core Templates | Templater |
|---------|----------------|-----------|
| Current date | `{{date}}` | `<% tp.date.now() %>` |
| Date math | ❌ | `<% tp.date.now("YYYY-MM-DD", 7) %>` |
| Prompts | ❌ | `<% tp.system.prompt("Question?") %>` |
| Conditionals | ❌ | `<% if (condition) { %>...` |
| File operations | ❌ | `<% tp.file.rename() %>` |

### Example Templates

#### Daily Note Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
tags:
  - type/daily
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

## 🎯 Today's Focus
- [ ] 

## 📅 Meetings
<%* 
const day = tp.date.now("dddd");
if (day === "Monday") { 
%>
- [ ] Team standup (10am)
- [ ] Weekly planning
<%* } else if (day === "Friday") { %>
- [ ] Weekly review
- [ ] 1:1s
<%* } %>

## 📝 Notes


## ✅ Done Today
- 

## 🔗 Links
← [[<% tp.date.now("YYYY-MM-DD", -1) %>|Yesterday]]
→ [[<% tp.date.now("YYYY-MM-DD", 1) %>|Tomorrow]]
```

#### Meeting Note Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
attendees:
  - 
type: meeting
tags:
  - type/meeting
---

# <% tp.system.prompt("Meeting title?") %>

## Attendees
- <% tp.system.prompt("Who attended? (comma-separated)") %>

## Agenda
1. 

## Discussion


## Decisions
- 

## Action Items
- [ ] 

## Follow-up
- Next meeting: 
```

#### Person (Team Member) Template
```markdown
---
role: <% tp.system.prompt("Role?") %>
team: <% tp.system.suggester(["Frontend", "Backend", "Platform", "Design"], ["Frontend", "Backend", "Platform", "Design"]) %>
start-date: <% tp.system.prompt("Start date? (YYYY-MM-DD)") %>
last-1on1: 
tags:
  - type/person
---

# <% tp.file.title %>

## Overview
- **Role**: `= this.role`
- **Team**: `= this.team`
- **Started**: `= this.start-date`

## 1:1 Notes
```dataview
LIST
FROM [[<% tp.file.title %>]] AND #meeting/1on1
SORT file.ctime DESC
```

## Goals
- 

## Notes

```

### Hotkey Setup
```
Settings → Hotkeys → Search "Templater" →
  "Insert template" → Cmd/Ctrl + T
```

---

## 3. ✅ Tasks — Advanced Task Management

> Turn Obsidian into a proper task manager with due dates, priorities, and queries.

### Installation
```
Community plugins → Browse → "Tasks" → Install → Enable
```

### Task Syntax
```markdown
- [ ] Basic task
- [ ] Task with due date 📅 2024-01-20
- [ ] Task with priority ⏫ high
- [ ] Task with scheduled date ⏳ 2024-01-18
- [ ] Task with start date 🛫 2024-01-15
- [x] Completed task ✅ 2024-01-17
```

### Priority Levels
```markdown
- [ ] ⏫ Highest priority
- [ ] 🔼 High priority
- [ ] 🔽 Low priority
- [ ] ⏬ Lowest priority
```

### Query Examples

#### All Tasks Due Today
````markdown
```tasks
due today
not done
```
````

#### This Week's Tasks by Priority
````markdown
```tasks
due after yesterday
due before in 8 days
not done
sort by priority
sort by due
```
````

#### Tasks by Tag/Folder
````markdown
```tasks
path includes projects
tags include #priority/high
not done
```
````

#### My Action Items from Meetings
````markdown
```tasks
path includes meetings
description includes @me
not done
sort by due
```
````

### Settings
```
Settings → Tasks →
  Global task filter: (leave empty for all)
  ✓ Set done date on completion
  Date format: YYYY-MM-DD
```

### Tip: Combine with Dataview
Tasks queries are simpler but Dataview offers more flexibility. Use both!

---

## 4. 📅 Calendar — Visual Daily Notes

> See your daily notes in a calendar view. Click to create or navigate.

### Installation
```
Community plugins → Browse → "Calendar" → Install → Enable
```

### Setup
```
Settings → Calendar →
  ✓ Show week numbers
  Start week on: Monday
  Words per dot: 250 (activity indicator)
```

### Usage
- **Click a date** → Opens/creates daily note for that date
- **Dots** indicate notes with content
- **Right sidebar** → Calendar view always visible

### Integration with Daily Notes
Make sure your daily notes folder matches:
```
Settings → Daily notes → New file location: daily/
Settings → Calendar → (uses same location)
```

---

## 5. 📋 Kanban — Visual Project Boards

> Trello/GitHub Projects style boards in Obsidian.

### Installation
```
Community plugins → Browse → "Kanban" → Install → Enable
```

### Create a Board
1. Create new note
2. `Cmd/Ctrl + P` → "Kanban: Create new board"
3. Or add to frontmatter:
```yaml
---
kanban-plugin: basic
---
```

### Board Structure
```markdown
---
kanban-plugin: basic
---

## Backlog

- [ ] Task 1
- [ ] Task 2

## In Progress

- [ ] Current work @{2024-01-20}

## Review

- [ ] Waiting for feedback

## Done

- [x] Completed item
```

### Features
- **Drag and drop** cards between columns
- **Due dates** with `@{YYYY-MM-DD}`
- **Links** work inside cards: `[[Project Name]]`
- **Tags** for filtering

### Use Cases
- Sprint planning board
- Team workload view
- Personal project tracker
- Content pipeline

---

## 6. ✏️ Excalidraw — Hand-Drawn Diagrams

> Create beautiful hand-drawn style diagrams, flowcharts, and sketches.

### Installation
```
Community plugins → Browse → "Excalidraw" → Install → Enable
```

### Create a Drawing
```
Cmd/Ctrl + P → "Excalidraw: Create new drawing"
```

### Features
- Hand-drawn aesthetic
- Shapes, arrows, text
- Embed in notes with `![[drawing.excalidraw]]`
- Export to PNG/SVG

### Developer Use Cases
- Architecture diagrams
- System flowcharts
- Meeting whiteboard captures
- Concept mind maps

### Tip: Embed in Notes
```markdown
# System Architecture

![[architecture-diagram.excalidraw|800]]

The above diagram shows...
```

---

## 7. 📊 Advanced Tables — Better Markdown Tables

> Navigate, format, and manipulate tables with ease.

### Installation
```
Community plugins → Browse → "Advanced Tables" → Install → Enable
```

### Features
- **Tab** to move between cells
- **Auto-format** on save
- **Add rows/columns** with hotkeys
- **Sort columns** via command palette

### Hotkeys (while in table)
| Key | Action |
|-----|--------|
| Tab | Next cell |
| Shift+Tab | Previous cell |
| Enter | Next row |
| Cmd+Shift+D | Delete row |

### Creating Tables Fast
Type this and press Tab:
```markdown
| Name | Role | Team |
```
Auto-completes to:
```markdown
| Name | Role | Team |
| ---- | ---- | ---- |
|      |      |      |
```

---

## 8. 🗓️ Periodic Notes — Weekly & Monthly Reviews

> Extend daily notes with weekly, monthly, quarterly, and yearly notes.

### Installation
```
Community plugins → Browse → "Periodic Notes" → Install → Enable
```

### Setup
```
Settings → Periodic Notes →
  ✓ Enable weekly notes
    Format: YYYY-[W]ww
    Folder: periodic/weekly
    Template: templates/weekly.md
  ✓ Enable monthly notes
    Format: YYYY-MM
    Folder: periodic/monthly
    Template: templates/monthly.md
```

### Weekly Review Template
```markdown
---
week: <% tp.date.now("YYYY-[W]WW") %>
tags:
  - type/weekly-review
---

# Week <% tp.date.now("WW") %> Review

## 🎯 Goals This Week
- [ ] 
- [ ] 
- [ ] 

## ✅ Accomplishments
- 

## 📊 Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Deep work hours | 20 | |
| 1:1s completed | 4 | |
| PRs reviewed | 10 | |

## 🧠 Lessons Learned
- 

## 📅 Daily Notes
```dataview
LIST
FROM "daily"
WHERE file.day >= date(<% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "YYYY-[W]WW") %>) 
  AND file.day < date(<% tp.date.now("YYYY-MM-DD", 7, tp.file.title, "YYYY-[W]WW") %>)
```

## → Next Week
- 
```

---

## 9. ⚡ QuickAdd — Fast Capture

> Create notes, add to existing notes, or run macros with one keystroke.

### Installation
```
Community plugins → Browse → "QuickAdd" → Install → Enable
```

### Setup Examples

#### Quick Capture to Inbox
```
Settings → QuickAdd → Add Choice →
  Name: Quick Capture
  Type: Capture
  
  Capture settings:
    File: 00-inbox/{{DATE}}-inbox.md
    ✓ Create file if not exists
    Capture format: - {{VALUE}}
```

Hotkey: `Cmd/Ctrl + Shift + C`

#### New Meeting Note
```
Type: Template
Template path: templates/meeting.md
File name format: meetings/{{DATE}}-{{VALUE}}
```

#### Add Task to Today
```
Type: Capture
File: daily/{{DATE}}.md
Insert after: ## Tasks
Format: - [ ] {{VALUE}}
```

---

## 10. 🔄 Obsidian Git — Version Control

> Automatically backup your vault to GitHub/GitLab.

### Installation
```
Community plugins → Browse → "Obsidian Git" → Install → Enable
```

### First-Time Setup

1. **Initialize repo** (if not already):
   ```bash
   cd /path/to/vault
   git init
   git remote add origin git@github.com:username/vault.git
   ```

2. **Configure plugin**:
   ```
   Settings → Obsidian Git →
     Auto backup interval: 10 (minutes)
     Auto pull interval: 10
     Commit message: vault backup: {{date}}
     ✓ Push on backup
   ```

### Manual Commands
```
Cmd/Ctrl + P →
  "Obsidian Git: Commit all changes"
  "Obsidian Git: Push"
  "Obsidian Git: Pull"
```

### .gitignore Recommendations
```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
.DS_Store
```

---

## 11. 🔍 Omnisearch — Supercharged Search

> Faster, smarter search with fuzzy matching and better ranking.

### Installation
```
Community plugins → Browse → "Omnisearch" → Install → Enable
```

### Features
- **Fuzzy matching** — typos don't break search
- **Better ranking** — most relevant results first
- **Search in PDFs** — if you have them
- **Keyboard navigation** — arrow keys + enter

### Hotkey
Replace default search:
```
Settings → Hotkeys →
  "Omnisearch: Vault search" → Cmd/Ctrl + O
```

---

## 12. 🧹 Linter — Auto-Format Markdown

> Automatically format your notes for consistency.

### Installation
```
Community plugins → Browse → "Linter" → Install → Enable
```

### Recommended Settings
```
Settings → Linter →
  ✓ Lint on save
  
  YAML rules:
    ✓ Format YAML arrays (use multi-line)
    
  Heading rules:
    ✓ Heading blank lines (add space around headings)
    
  Content rules:
    ✓ Trailing spaces (remove)
    ✓ Consecutive blank lines (limit to 1)
    
  Spacing rules:
    ✓ Space after list markers
```

### Run Manually
```
Cmd/Ctrl + P → "Linter: Lint the current file"
```

---

## 13. 🎛️ Commander — Custom UI

> Add custom buttons to title bar, status bar, and ribbon.

### Installation
```
Community plugins → Browse → "Commander" → Install → Enable
```

### Use Cases
- **Quick access** to frequent commands
- **Visual triggers** for macros
- **Mobile-friendly** buttons for common actions

### Setup Example
```
Settings → Commander → Title bar →
  Add: "Daily notes: Open today's daily note" → 📅 icon
  Add: "QuickAdd: Quick Capture" → ➕ icon
```

---

## 14. 📆 Natural Language Dates — Smart Date Input

> Type "tomorrow" or "next friday" and get actual dates.

### Installation
```
Community plugins → Browse → "Natural Language Dates" → Install → Enable
```

### Usage
Type `@` followed by natural language:
```markdown
- [ ] Review PR @tomorrow
- [ ] Team offsite @next friday
- [ ] Quarterly review @in 2 weeks
```

Converts to:
```markdown
- [ ] Review PR 2024-01-16
- [ ] Team offsite 2024-01-19
- [ ] Quarterly review 2024-01-29
```

### Hotkey
```
Settings → Hotkeys → "Natural Language Dates: Insert date" → @
```

---

## 15. 🔗 Paste URL into Selection — Clean Links

> Select text, paste a URL, get a markdown link.

### Installation
```
Community plugins → Browse → "Paste URL into Selection" → Install → Enable
```

### How It Works

**Without plugin:**
1. Type `[link text]()`
2. Paste URL inside parentheses

**With plugin:**
1. Type "link text"
2. Select it
3. Paste URL
4. Get `[link text](https://url.com)`

Simple but saves tons of time when linking.

---

## 🚀 Quick Start: Install These First

For a developer & team manager, install in this order:

### Week 1 — Foundation
1. **Templater** — Set up daily note template
2. **Calendar** — Visual navigation
3. **Advanced Tables** — Better table editing
4. **Linter** — Consistent formatting

### Week 2 — Productivity
5. **Tasks** — Start tracking tasks with dates
6. **QuickAdd** — Fast capture workflow
7. **Natural Language Dates** — Easier date entry
8. **Paste URL into Selection** — Faster linking

### Week 3 — Power Features
9. **Dataview** — Build dashboards
10. **Periodic Notes** — Weekly reviews
11. **Kanban** — Visual project boards

### Week 4 — Polish
12. **Obsidian Git** — Backup everything
13. **Omnisearch** — Better search
14. **Commander** — Custom UI
15. **Excalidraw** — When you need diagrams

---

## 📋 Plugin Cheat Sheet

| Need | Plugin | Command/Hotkey |
|------|--------|----------------|
| Query notes | Dataview | Write query in note |
| Smart templates | Templater | `Cmd+T` |
| Task queries | Tasks | Write query in note |
| Calendar view | Calendar | Right sidebar |
| Project board | Kanban | Create `.kanban` note |
| Diagrams | Excalidraw | `Cmd+P` → new drawing |
| Format tables | Advanced Tables | Tab in table |
| Weekly notes | Periodic Notes | `Cmd+P` → open weekly |
| Quick capture | QuickAdd | Custom hotkey |
| Git backup | Obsidian Git | Auto or `Cmd+P` |
| Better search | Omnisearch | `Cmd+O` |
| Auto-format | Linter | Auto on save |
| Custom buttons | Commander | Settings |
| Natural dates | NL Dates | `@tomorrow` |
| Paste links | Paste URL | Select + paste |

---

## Next Steps

1. [[dataview-cookbook]] — Advanced Dataview recipes
2. [[templater-scripts]] — Custom Templater functions
3. [[workflow-automation]] — Combining plugins for workflows

---

## Resources

- [Obsidian Community Plugins](https://obsidian.md/plugins) — Official directory
- [Obsidian Hub](https://publish.obsidian.md/hub) — Community documentation
- [Plugin Developer Docs](https://docs.obsidian.md/) — If you want to build your own


