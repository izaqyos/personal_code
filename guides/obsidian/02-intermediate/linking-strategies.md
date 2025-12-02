# Linking Strategies — Tags vs Folders vs Links

> The architectural decision that shapes your entire PKM system.

---

## 🤔 The Big Question

When organizing notes, developers instinctively reach for folders (we love hierarchies). But Obsidian's power comes from **links**. So when do you use what?

```
Folders  →  Physical location (can only be in ONE place)
Tags     →  Metadata/categories (many-to-many)
Links    →  Relationships/connections (the graph)
```

---

## 📁 Folders — When to Use

### Good For
- **Broad domains** that rarely overlap (Work vs Personal)
- **Asset types** (Templates, Attachments, Archive)
- **Access control** (if sharing specific folders)
- **Muscle memory** navigation

### Developer Analogy
Folders = Monorepo packages or microservices. Clear boundaries, minimal cross-cutting.

### Recommended Structure
```
vault/
├── 00-inbox/           # Quick capture, unsorted
├── 01-projects/        # Active work
├── 02-areas/           # Ongoing responsibilities
├── 03-resources/       # Reference material
├── 04-archive/         # Completed/inactive
├── templates/          # Note templates
├── attachments/        # Images, PDFs
└── daily/              # Daily notes
```

This is the **PARA method** (Projects, Areas, Resources, Archive) — works great for managers.

### ⚠️ Folder Anti-Patterns
```
❌ vault/
   ├── programming/
   │   ├── python/
   │   │   ├── data-structures/
   │   │   │   ├── lists/
   │   │   │   │   └── list-comprehensions.md  # 5 levels deep!

✅ vault/
   ├── resources/
   │   └── python-list-comprehensions.md      # Flat with links
```

**Rule:** If you're nesting more than 2-3 levels, use links instead.

---

## 🏷️ Tags — When to Use

### Good For
- **Status tracking**: `#status/in-progress`, `#status/done`, `#status/blocked`
- **Content type**: `#type/meeting`, `#type/decision`, `#type/reference`
- **Cross-cutting concerns**: `#team/backend`, `#priority/high`
- **Queryable metadata** (with Dataview)

### Developer Analogy
Tags = Labels on GitHub issues/PRs. Multiple can apply, filterable, searchable.

### Tag Strategies

#### Flat Tags
```markdown
#python #learning #beginner
```
Simple but can get messy at scale.

#### Nested Tags (Recommended)
```markdown
#lang/python
#lang/rust
#status/learning
#status/mastered
#project/team-dashboard
#meeting/1on1
#meeting/standup
```

Nested tags create implicit hierarchies without folder constraints.

### Searching Tags
```
# In search or Dataview
tag:#status/in-progress
tag:#lang/python AND tag:#status/learning
```

### ⚠️ Tag Anti-Patterns
```
❌ #Python #python #PYTHON           # Inconsistent casing
❌ #my-very-long-and-specific-tag    # Too specific, use links
❌ #a #the #and                      # Meaningless tags

✅ #lang/python                      # Consistent, namespaced
✅ [[Python Basics]]                 # Specific concepts as links
```

---

## 🔗 Links — The Core of Obsidian

### Good For
- **Connecting ideas** (this note relates to that note)
- **Building context** (backlinks show usage)
- **Serendipitous discovery** (graph reveals clusters)
- **Atomic notes** (small, linkable concepts)

### Developer Analogy
Links = Import statements + dependency graph. Shows what depends on what.

### Link Types

#### Direct Links
```markdown
I learned about [[Python List Comprehensions]] today.
```

#### Aliased Links
```markdown
The [[Python List Comprehensions|list comp syntax]] is elegant.
```

#### Header Links
```markdown
See [[Python Basics#Data Types]] for more.
```

#### Block Links
```markdown
As mentioned in [[Meeting Notes 2024-01-15#^important-decision]]
```

### The Power of Backlinks

When you write:
```markdown
# Note: Python Learning
I'm studying [[Data Structures]] for interviews.
```

The "Data Structures" note automatically shows this as a backlink:
```
Backlinks (1)
└── Python Learning
    "I'm studying Data Structures for interviews."
```

**This is bidirectional linking** — you don't maintain "see also" sections manually.

---

## 🎯 Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                    WHAT ARE YOU ORGANIZING?                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   BROAD DOMAIN          METADATA              RELATIONSHIP
   "Where does           "What kind            "How does this
    this live?"           is this?"             connect?"
        │                     │                     │
        ▼                     ▼                     ▼
    📁 FOLDER             🏷️ TAG                🔗 LINK
        │                     │                     │
        ▼                     ▼                     ▼
   Work/Personal         #type/meeting         [[Related Note]]
   Projects/Archive      #status/done          [[Concept]]
   Templates/            #team/backend         [[Person]]
   Attachments           #priority/high        [[Project]]
```

---

## 🏗️ Recommended Hybrid System

### For a Developer & Team Manager

```markdown
# Folder Structure (PARA-inspired)
00-inbox/          # Dump everything here first
01-projects/       # Active work with deadlines
02-areas/          # Ongoing responsibilities (team, skills, health)
03-resources/      # Reference material
04-archive/        # Done/inactive
templates/
daily/
attachments/

# Tag Taxonomy
#type/meeting #type/decision #type/reference #type/idea
#status/active #status/done #status/blocked #status/someday
#team/frontend #team/backend #team/platform
#person/[[Name]]  # Or just use links for people
#project/dashboard #project/migration  # Or just use links

# Link Everything
[[Person Name]]       # Team members
[[Project Name]]      # Active projects  
[[Technology]]        # Python, Rust, etc.
[[Concept]]           # Data structures, algorithms
[[Meeting 2024-01-15]]# Specific meetings
```

### Example Note

```markdown
---
tags:
  - type/meeting
  - type/decision
  - status/done
---

# 1:1 with [[Sarah Chen]] - 2024-01-15

## Context
Discussing [[Project Dashboard]] progress and [[Q1 Goals]].

## Discussion
- [[Sarah Chen]] is blocked on [[API Integration]]
- Need input from [[Backend Team]]
- Decision: Prioritize [[Authentication]] first

## Action Items
- [ ] [[Sarah Chen]] to draft [[API Spec]] by Friday
- [ ] I'll sync with [[Backend Team]] tomorrow
- [x] Review [[Performance Metrics]] ✅

## Follow-up
→ Next 1:1: [[1:1 with Sarah Chen - 2024-01-22]]
← Previous: [[1:1 with Sarah Chen - 2024-01-08]]

#meeting/1on1
```

---

## 📊 Quick Reference

| Use Case | Folders | Tags | Links |
|----------|---------|------|-------|
| "This is a meeting note" | | ✅ `#type/meeting` | |
| "This relates to Python" | | | ✅ `[[Python]]` |
| "This is work stuff" | ✅ `work/` | | |
| "This is high priority" | | ✅ `#priority/high` | |
| "John mentioned this" | | | ✅ `[[John Smith]]` |
| "This is done" | | ✅ `#status/done` | |
| "Store my templates" | ✅ `templates/` | | |
| "Related to Project X" | | | ✅ `[[Project X]]` |
| "Archive old stuff" | ✅ `archive/` | | |

---

## 🚀 Exercise: Organize Your Learning

Create this structure for your learning tracks:

```markdown
# File: 02-areas/learning-hub.md

# Learning Hub

## Active Tracks
| Track | Status | Link |
|-------|--------|------|
| [[Python Practice]] | 🟢 Active | #status/active |
| [[LeetCode Prep]] | 🟢 Active | #status/active |
| [[Obsidian Mastery]] | 🟢 Active | #status/active |
| [[Rust Course]] | 🟡 In Progress | #status/in-progress |
| [[Prompt Engineering]] | 🟢 Active | #status/active |
| [[Networking Refresher]] | ⚪ Someday | #status/someday |

## Quick Links
- [[Daily Learning Log]]
- [[Weekly Review]]
- [[Skills Inventory]]
```

---

## Next
→ [[templates-and-daily-notes]] — Automate your workflow with templates


