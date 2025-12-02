# YAML Frontmatter & Metadata

> Structure your notes for powerful queries and automation.

---

## 🤔 What is Frontmatter?

YAML metadata at the **top** of a note, wrapped in `---`:

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - type/meeting
  - status/active
author: yosii
---

# Rest of your note starts here
```

**Developer analogy:** It's like a file's metadata/headers, or a JSON config at the top of each note.

---

## 📋 Why Use Frontmatter?

1. **Queryable** — Dataview can query any field
2. **Consistent** — Enforce structure across notes
3. **Sortable** — Sort notes by date, priority, etc.
4. **Filterable** — Find notes by any property
5. **Automatable** — Templater can populate fields

---

## ✏️ Syntax Basics

### Scalar Values
```yaml
---
title: Meeting Notes
date: 2024-01-15
priority: high
completed: true
rating: 4.5
---
```

### Lists
```yaml
---
tags:
  - meeting
  - project-x
  - important

# Or inline
tags: [meeting, project-x, important]
---
```

### Nested Objects
```yaml
---
project:
  name: Dashboard
  status: active
  deadline: 2024-03-01
---
```

### Links in Frontmatter
```yaml
---
related:
  - "[[Project Dashboard]]"
  - "[[Team Meeting]]"
author: "[[John Smith]]"
---
```

**Note:** Links in frontmatter need quotes to work properly.

---

## 🏷️ Tags: Frontmatter vs Inline

### Option 1: Frontmatter Tags (Recommended)
```yaml
---
tags:
  - type/meeting
  - status/active
  - team/backend
---
```

**Pros:**
- Clean, organized
- Easy to query with Dataview
- Consistent location

### Option 2: Inline Tags
```markdown
#type/meeting #status/active #team/backend
```

**Pros:**
- Quick to add while writing
- Visible in content

### Best Practice: Both
```yaml
---
tags:
  - type/meeting
  - status/active
---

# Meeting Notes #team/backend

Content here with occasional #inline-tags for context.
```

---

## 📊 Common Frontmatter Schemas

### For Meetings
```yaml
---
type: meeting
date: 2024-01-15
attendees:
  - "[[Alice]]"
  - "[[Bob]]"
project: "[[Project X]]"
status: completed
tags:
  - type/meeting
  - meeting/standup
---
```

### For Projects
```yaml
---
type: project
status: active  # active, on-hold, completed, cancelled
priority: high  # high, medium, low
start_date: 2024-01-01
deadline: 2024-03-31
owner: "[[Me]]"
team:
  - "[[Alice]]"
  - "[[Bob]]"
tags:
  - type/project
  - status/active
---
```

### For People (Team Members)
```yaml
---
type: person
role: Senior Engineer
team: Backend
reports_to: "[[Manager Name]]"
started: 2023-06-15
location: Tel Aviv
tags:
  - type/person
  - team/backend
---
```

### For Learning Notes
```yaml
---
type: learning
topic: Python
subtopic: Data Structures
difficulty: intermediate
source: "[[Udemy Course]]"
status: in-progress  # not-started, in-progress, completed
created: 2024-01-15
tags:
  - type/learning
  - lang/python
  - status/in-progress
---
```

### For Daily Notes
```yaml
---
date: 2024-01-15
day: Monday
week: 3
mood: 😊
energy: 4
tags:
  - type/daily
---
```

### For Decision Records
```yaml
---
type: decision
status: accepted  # proposed, accepted, deprecated, superseded
date: 2024-01-15
deciders:
  - "[[Alice]]"
  - "[[Bob]]"
supersedes: "[[ADR-001]]"
superseded_by: 
tags:
  - type/decision
  - status/accepted
---
```

---

## 🔍 Querying Frontmatter with Dataview

Once you have consistent frontmatter, Dataview becomes incredibly powerful:

### List all active projects
```dataview
LIST
FROM #type/project
WHERE status = "active"
SORT priority DESC
```

### Table of team members
```dataview
TABLE role, team, started
FROM #type/person
SORT started ASC
```

### Tasks due this week
```dataview
TASK
FROM #type/project
WHERE deadline <= date(today) + dur(7 days)
```

### Recent meetings with a person
```dataview
LIST
FROM #type/meeting
WHERE contains(attendees, [[Alice]])
SORT date DESC
LIMIT 5
```

*(We'll cover Dataview in depth in the Advanced section)*

---

## ⚙️ Obsidian Properties (v1.4+)

Obsidian now has built-in **Properties** view for frontmatter:

### Enable Properties View
- Click the properties icon (≡) at the top of a note
- Or: Settings → Editor → Show properties

### Property Types
Obsidian auto-detects types, or you can set them:
- **Text** — String values
- **List** — Arrays
- **Number** — Numeric values
- **Checkbox** — Boolean (true/false)
- **Date** — Date picker
- **DateTime** — Date and time

### Benefits
- Visual editor for frontmatter
- Type validation
- Autocomplete for existing values
- No YAML syntax errors

---

## 🛡️ Validation Tips

### Common YAML Gotchas

```yaml
# ❌ Bad: Unquoted special characters
title: Meeting: Planning Session  # Colon breaks parsing

# ✅ Good: Quote strings with special chars
title: "Meeting: Planning Session"

# ❌ Bad: Unquoted link
related: [[Other Note]]

# ✅ Good: Quote links
related: "[[Other Note]]"

# ❌ Bad: Tab indentation
tags:
	- one    # Tab character

# ✅ Good: Space indentation (2 spaces)
tags:
  - one
  - two
```

### Validate Your YAML
If a note isn't parsing correctly:
1. Check for tabs (use spaces)
2. Check for unquoted colons
3. Check for unquoted brackets
4. Use an online YAML validator

---

## 🎯 Exercise: Standardize Your Frontmatter

### Step 1: Define Your Schema
Create a reference note:

```markdown
# Frontmatter Schema Reference

## Required Fields by Type

### All Notes
- `type`: meeting | project | person | learning | daily | decision
- `tags`: array of tags
- `date` or `created`: when created

### Meetings
- `attendees`: array of person links
- `status`: scheduled | completed | cancelled

### Projects  
- `status`: active | on-hold | completed | cancelled
- `priority`: high | medium | low
- `deadline`: date
- `owner`: person link

### People
- `role`: job title
- `team`: team name
- `reports_to`: person link

### Learning
- `topic`: main subject
- `source`: where you're learning from
- `status`: not-started | in-progress | completed
```

### Step 2: Update Your Templates
Add frontmatter to all your templates (we created these earlier).

### Step 3: Retrofit Existing Notes
Add frontmatter to your existing notes, starting with the most important ones.

---

## 🔮 Advanced: Aliases

Aliases let a note be found by multiple names:

```yaml
---
aliases:
  - PKM
  - Personal Knowledge Management
  - Second Brain
---

# Personal Knowledge Management System
```

Now searching for "PKM" or "Second Brain" will find this note!

Great for:
- Acronyms
- Alternative names
- Common misspellings

---

## Next
→ [[canvas-and-visual-thinking]] — Visual note-taking and mind mapping


