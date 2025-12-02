# Templates & Daily Notes Workflow

> Automate repetitive note creation and build consistent habits.

---

## 🎯 Why Templates Matter

As a developer, you know the value of:
- **DRY** (Don't Repeat Yourself)
- **Scaffolding** (project generators, boilerplate)
- **Consistency** (code style, conventions)

Templates bring these principles to note-taking.

---

## ⚙️ Setting Up Core Templates Plugin

1. **Settings** → **Core plugins** → Enable **Templates**
2. **Settings** → **Templates** → Set template folder: `templates`
3. Create your `templates/` folder in the vault

### Basic Template Variables

```markdown
{{title}}    → Note title
{{date}}     → Current date (YYYY-MM-DD)
{{time}}     → Current time (HH:mm)
```

---

## 📝 Essential Templates for Developers & Managers

### 1. Daily Note Template

```markdown
# {{date}} — Daily Note

## 🎯 Top 3 Priorities
1. 
2. 
3. 

## 📅 Schedule
- [ ] 09:00 — 
- [ ] 10:00 — 
- [ ] 14:00 — 

## 📝 Notes & Captures


## ✅ Completed
- 

## 🔗 Links Created Today
- 

## 🌙 End of Day Review
**Energy:** ⚡⚡⚡⚡⚡ (1-5)
**Focus:** 🎯🎯🎯🎯🎯 (1-5)

### What went well?


### What could improve?


---
← [[{{date:YYYY-MM-DD|-1d}}]] | [[{{date:YYYY-MM-DD|+1d}}]] →
```

### 2. Meeting Note Template

```markdown
---
tags:
  - type/meeting
  - status/active
date: {{date}}
attendees: 
---

# Meeting: {{title}}

## 📋 Agenda
1. 
2. 
3. 

## 👥 Attendees
- 

## 📝 Notes


## ✅ Decisions Made


## 🎯 Action Items
- [ ] @person — Task — Due: 
- [ ] @me — Task — Due: 

## 🔗 Related
- 

---
*Created: {{date}} {{time}}*
```

### 3. 1:1 Meeting Template

```markdown
---
tags:
  - type/meeting
  - meeting/1on1
date: {{date}}
with: "[[]]"
---

# 1:1 with [[]] — {{date}}

## 🔄 Since Last Time
- Previous action items:
  - [ ] 
- Updates:

## 💬 Their Topics
- 

## 💬 My Topics
- 

## 🎯 Career & Growth
- Goals progress:
- Feedback:
- Development areas:

## 😊 Wellbeing Check
- Energy/workload:
- Blockers:
- Support needed:

## ✅ Action Items
- [ ] @them — 
- [ ] @me — 

## 🔗 Links
← Previous: [[]]
→ Next: [[]]
```

### 4. Project Note Template

```markdown
---
tags:
  - type/project
  - status/active
created: {{date}}
deadline: 
owner: 
---

# Project: {{title}}

## 📋 Overview
**Goal:** 
**Why it matters:** 
**Success criteria:** 

## 👥 Stakeholders
| Role | Person | Notes |
|------|--------|-------|
| Owner | [[]] | |
| Sponsor | [[]] | |
| Team | [[]] | |

## 🗺️ Milestones
- [ ] Milestone 1 — Due: 
- [ ] Milestone 2 — Due: 
- [ ] Milestone 3 — Due: 

## 📊 Status Updates
### {{date}}
- 

## 🔗 Related
- Docs: 
- Repo: 
- Meetings: 

## 📁 Resources
- 

---
*Created: {{date}}*
```

### 5. Person (Team Member) Template

```markdown
---
tags:
  - type/person
  - team/
role: 
started: 
---

# [[{{title}}]]

## 📋 Role & Responsibilities
- **Title:** 
- **Team:** 
- **Reports to:** [[]]
- **Started:** 

## 🎯 Current Focus
- 

## 💪 Strengths
- 

## 🌱 Growth Areas
- 

## 📝 Notes & Observations


## 🔗 1:1 History
```dataview
LIST FROM #meeting/1on1 
WHERE contains(file.name, "{{title}}")
SORT date DESC
LIMIT 10
```

## 🎯 Goals
### Q1 2024
- [ ] Goal 1
- [ ] Goal 2

---
*Profile created: {{date}}*
```

### 6. Learning Topic Template

```markdown
---
tags:
  - type/learning
  - status/in-progress
  - lang/
created: {{date}}
---

# {{title}}

## 🎯 Learning Goal
**What:** 
**Why:** 
**By when:** 

## 📚 Resources
- [ ] Course/Book: 
- [ ] Documentation: 
- [ ] Practice project: 

## 📝 Notes


## 💡 Key Concepts
1. 
2. 
3. 

## 🧪 Practice
```code

```

## ❓ Questions / Gaps


## 🔗 Related
- [[]]

---
*Started: {{date}}*
```

### 7. Decision Record (ADR-style)

```markdown
---
tags:
  - type/decision
  - status/accepted
date: {{date}}
deciders: 
---

# Decision: {{title}}

## 📋 Context
What is the issue that we're seeing that is motivating this decision?

## 🎯 Decision
What is the change that we're proposing and/or doing?

## 🤔 Options Considered

### Option 1: 
- ✅ Pros:
- ❌ Cons:

### Option 2:
- ✅ Pros:
- ❌ Cons:

### Option 3:
- ✅ Pros:
- ❌ Cons:

## ✅ Chosen Option
**Option X** because...

## 📊 Consequences
- Good:
- Bad:
- Risks:

## 🔗 Related
- [[]]

---
*Decided: {{date}}*
*Status: Accepted/Proposed/Deprecated*
```

---

## 📅 Daily Notes Setup

### Enable Daily Notes
1. **Settings** → **Core plugins** → Enable **Daily notes**
2. Configure:
   - **Date format:** `YYYY-MM-DD` (sortable, standard)
   - **New file location:** `daily/`
   - **Template file:** `templates/daily-note`
   - **Open daily note on startup:** Your choice

### Keyboard Shortcut
- **Open today's daily note:** `Cmd+D` (set in Hotkeys)
- Or use Command Palette: `Cmd+P` → "Daily notes: Open today"

---

## 🚀 Using Templates

### Method 1: Command Palette
1. Create new note (`Cmd+N`)
2. `Cmd+P` → "Templates: Insert template"
3. Select template

### Method 2: Hotkey (Recommended)
1. **Settings** → **Hotkeys**
2. Search "Templates: Insert template"
3. Assign: `Cmd+T` or `Alt+T`

### Method 3: Quick Add Plugin (Advanced)
For power users — we'll cover this in the plugins section.

---

## 🔧 Pro Tips

### Tip 1: Template Folder Organization
```
templates/
├── daily-note.md
├── meeting.md
├── 1on1.md
├── project.md
├── person.md
├── learning.md
├── decision.md
└── quick-capture.md
```

### Tip 2: Frontmatter Defaults
Always include YAML frontmatter for Dataview queries:
```yaml
---
tags:
  - type/meeting
date: {{date}}
---
```

### Tip 3: Link Placeholders
Leave `[[]]` empty as prompts to fill in:
```markdown
## Attendees
- [[]]
- [[]]
```

### Tip 4: Use Callouts for Visual Structure
```markdown
> [!info] Context
> Background information here

> [!warning] Blocker
> Something blocking progress

> [!success] Decision
> What was decided
```

---

## 🎯 Exercise: Set Up Your Core Templates

1. **Create** `templates/` folder in your vault
2. **Copy** these templates (start with daily-note and meeting)
3. **Enable** Daily Notes core plugin
4. **Set** hotkey for inserting templates (`Cmd+T`)
5. **Create** your first daily note for today

### Test Your Setup
1. Press your daily note hotkey
2. A new note should appear with your template filled in
3. Create a meeting note using `Cmd+N` → `Cmd+T` → select meeting

---

## 🔮 Templater Plugin — Advanced Templating

The core Templates plugin is good, but **Templater** (community plugin) is *much* more powerful:

- Date math (`tomorrow`, `next week`, `-1 day`)
- User prompts and dropdown selectors
- Conditionals and logic
- File operations (rename, move, create)
- JavaScript execution

---

### Installing Templater

1. **Settings** → **Community plugins** → **Turn on community plugins**
2. Click **Browse** → Search "Templater"
3. Click **Install** → **Enable**

### Configuring Templater

```
Settings → Templater →
  Template folder location: templates
  ✓ Trigger Templater on new file creation
  ✓ Enable folder templates (optional)
```

---

### Core Templates vs Templater Syntax

| Feature | Core Templates | Templater |
|---------|----------------|-----------|
| Today's date | `{{date}}` | `<% tp.date.now() %>` |
| Custom format | `{{date:YYYY-MM-DD}}` | `<% tp.date.now("YYYY-MM-DD") %>` |
| Tomorrow | ❌ | `<% tp.date.now("YYYY-MM-DD", 1) %>` |
| Yesterday | ❌ | `<% tp.date.now("YYYY-MM-DD", -1) %>` |
| Next week | ❌ | `<% tp.date.now("YYYY-MM-DD", 7) %>` |
| Note title | `{{title}}` | `<% tp.file.title %>` |
| Time | `{{time}}` | `<% tp.date.now("HH:mm") %>` |
| User prompt | ❌ | `<% tp.system.prompt("Question?") %>` |
| Dropdown | ❌ | `<% tp.system.suggester([...]) %>` |
| Conditionals | ❌ | `<%* if (condition) { %> ... <%* } %>` |

---

### Templater Variables Cheat Sheet

#### Date & Time
```markdown
<% tp.date.now("YYYY-MM-DD") %>           → 2024-01-15
<% tp.date.now("dddd") %>                 → Monday
<% tp.date.now("dddd, MMMM Do YYYY") %>   → Monday, January 15th 2024
<% tp.date.now("YYYY-MM-DD", 1) %>        → Tomorrow
<% tp.date.now("YYYY-MM-DD", -1) %>       → Yesterday
<% tp.date.now("YYYY-MM-DD", 7) %>        → Next week
<% tp.date.now("HH:mm") %>                → 14:30
```

#### File Operations
```markdown
<% tp.file.title %>                       → Current note title
<% tp.file.folder() %>                    → Current folder path
<% tp.file.creation_date() %>             → When file was created
<% tp.file.path() %>                      → Full file path
```

#### User Input
```markdown
<% tp.system.prompt("What's the title?") %>
<% tp.system.prompt("Meeting with?", "Team") %>  → Default value
<% tp.system.suggester(["Option A", "Option B"], ["a", "b"]) %>
```

#### Cursor Placement
```markdown
<% tp.file.cursor() %>                    → Place cursor here after insert
<% tp.file.cursor(1) %>                   → Multiple cursors (numbered)
```

---

### Templater Daily Note Template

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
tags:
  - type/daily
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

## 🎯 Top 3 Priorities
1. <% tp.file.cursor(1) %>
2. 
3. 

## 📅 Schedule
<%* 
const day = tp.date.now("dddd");
if (day === "Monday") { 
%>
- [ ] 10:00 — Team standup
- [ ] 14:00 — Weekly planning
<%* } else if (day === "Friday") { %>
- [ ] 10:00 — Team standup  
- [ ] 15:00 — Weekly review
<%* } else { %>
- [ ] 10:00 — Team standup
<%* } %>

## 📝 Notes


## ✅ Completed
- 

## 🌙 End of Day
**Energy:** /5
**Focus:** /5

---
← [[<% tp.date.now("YYYY-MM-DD", -1) %>|Yesterday]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>|Tomorrow]] →
```

---

### Templater Meeting Template with Prompts

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
type: meeting
tags:
  - type/meeting
---

# <% tp.system.prompt("Meeting title?") %>

## 👥 Attendees
- <% tp.system.prompt("Who attended? (comma-separated)") %>

## 📋 Agenda
1. <% tp.file.cursor() %>

## 📝 Notes


## ✅ Decisions


## 🎯 Action Items
- [ ] 

---
*Created: <% tp.date.now("YYYY-MM-DD HH:mm") %>*
```

---

### Templater 1:1 Template with Dropdown

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
with: "[[<% tp.system.prompt("Team member name?") %>]]"
tags:
  - type/meeting
  - meeting/1on1
---

# 1:1 with [[<% tp.system.prompt("Team member name?") %>]] — <% tp.date.now("YYYY-MM-DD") %>

## 🔄 Since Last Time
- Previous action items:
  - [ ] 

## 💬 Their Topics
- <% tp.file.cursor() %>

## 💬 My Topics
- 

## 😊 Wellbeing Check
- **Energy:** <% tp.system.suggester(["🔴 Low", "🟡 Medium", "🟢 High"], ["Low", "Medium", "High"]) %>
- **Blockers:** 

## ✅ Action Items
- [ ] @them — 
- [ ] @me — 

---
← Previous: [[]]
→ Next scheduled: <% tp.date.now("YYYY-MM-DD", 14) %>
```

---

### Using Templater

> ⚠️ **Important:** The command is named differently than Core Templates!

| Action | Command |
|--------|---------|
| Insert Templater template | `Cmd+P` → **"Templater: Open insert template modal"** |
| Insert Core template | `Cmd+P` → "Templates: Insert template" |
| Create new from template | `Cmd+P` → "Templater: Create new note from template" |

### Set a Hotkey

1. **Settings** → **Hotkeys**
2. Search: `Templater: Open insert template modal`
3. Assign: `Cmd + T` (or your preference)

---

### Pro Tips for Templater

#### Tip 1: Use `cursor()` for Fast Editing
```markdown
## Notes
<% tp.file.cursor() %>
```
After inserting, cursor jumps right here!

#### Tip 2: Combine Prompts with Links
```markdown
Related to: [[<% tp.system.prompt("Related project?") %>]]
```
Creates a link from user input.

#### Tip 3: Conditional Content by Day
```markdown
<%* if (tp.date.now("dddd") === "Monday") { %>
## 📋 Weekly Planning
- [ ] Review last week
- [ ] Set this week's goals
<%* } %>
```
Only shows on Mondays!

#### Tip 4: Auto-Rename File from Prompt
```markdown
<%*
const title = await tp.system.prompt("Meeting title?");
await tp.file.rename(tp.date.now("YYYY-MM-DD") + " - " + title);
%>
# <%= title %>
```
Creates file like `2024-01-15 - Sprint Planning.md`

---

## Next
→ [[search-and-navigation]] — Master finding anything instantly


