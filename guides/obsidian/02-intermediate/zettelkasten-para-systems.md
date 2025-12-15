# Zettelkasten & PARA Systems

> Two proven organizational frameworks for your vault — choose what fits your brain.

---

## 🧠 Why Use a System?

Without structure, your vault becomes a **graveyard of notes**:
- Hard to find anything
- No connections between ideas
- Notes written but never revisited

A good system provides:
- **Consistent organization** — Know where to put new notes
- **Discoverability** — Find notes when you need them
- **Emergence** — Ideas connect and build on each other

**Developer analogy:** It's like choosing between monorepo vs. multi-repo, REST vs. GraphQL — pick one and commit.

---

## 📦 PARA Method

### What is PARA?

Created by **Tiago Forte**, PARA organizes by **actionability**, not topic.

| Folder | What Goes Here | Timeframe |
|--------|---------------|-----------|
| **P**rojects | Active work with deadlines | Days-Weeks |
| **A**reas | Ongoing responsibilities | Ongoing |
| **R**esources | Reference material | Forever |
| **A**rchive | Completed/inactive items | Historical |

### PARA for Developers & Managers

```
vault/
├── 1-Projects/
│   ├── api-v2-redesign/
│   ├── q1-performance-review/
│   ├── onboarding-alice/
│   └── kubernetes-migration/
│
├── 2-Areas/
│   ├── team-management/
│   │   ├── 1on1-notes/
│   │   ├── hiring/
│   │   └── team-goals.md
│   ├── engineering/
│   │   ├── architecture-decisions/
│   │   ├── code-standards.md
│   │   └── tech-debt.md
│   └── personal-development/
│       ├── learning-roadmap.md
│       └── career-goals.md
│
├── 3-Resources/
│   ├── programming/
│   │   ├── python/
│   │   ├── rust/
│   │   └── algorithms/
│   ├── management/
│   │   ├── feedback-frameworks.md
│   │   └── meeting-templates/
│   └── tools/
│       ├── git-cheatsheet.md
│       ├── vim-config.md
│       └── obsidian-workflows.md
│
└── 4-Archive/
    ├── 2023-projects/
    ├── completed-hiring/
    └── old-team-notes/
```

### PARA Workflow

1. **New task/project?** → `1-Projects/project-name/`
2. **Ongoing responsibility?** → `2-Areas/relevant-area/`
3. **Learning something new?** → `3-Resources/topic/`
4. **Project done?** → Move folder to `4-Archive/`

### PARA Decision Tree

```
Is this actionable?
├── YES → Does it have a deadline?
│         ├── YES → 1-Projects
│         └── NO  → 2-Areas (ongoing responsibility)
└── NO  → Is it useful reference material?
          ├── YES → 3-Resources
          └── NO  → Delete or 4-Archive
```

---

## 📝 Zettelkasten Method

### What is Zettelkasten?

German for "slip box" — developed by **Niklas Luhmann** (70+ books, 500+ papers).

**Core principle:** Notes are **atomic** (one idea each) and heavily **linked**.

### Zettelkasten Principles

| Principle | Description | Developer Analogy |
|-----------|-------------|-------------------|
| **Atomic** | One idea per note | Single responsibility |
| **Linked** | Connected to related notes | Microservices architecture |
| **In your own words** | Rewrite, don't copy | Code review understanding |
| **Permanent** | Polished, not scratch | Production code |

### Zettelkasten Note Types

#### 1. Fleeting Notes (Inbox)
Quick captures, unprocessed thoughts.

```markdown
# Inbox/2024-01-15-random

- Heard about "event sourcing" in meeting — look into this
- Idea: use Dataview for weekly reviews
- Book rec from Alice: "Staff Engineer"
```

**Lifespan:** Process within 24-48 hours.

#### 2. Literature Notes
Summaries of external sources (books, articles, videos).

```markdown
---
type: literature
source: "Designing Data-Intensive Applications"
author: Martin Kleppmann
chapter: 5
---

# DDIA Ch5 - Replication

## Key Ideas
- Replication strategies: single-leader, multi-leader, leaderless
- Trade-off: consistency vs. availability

## My Takeaways
- [[Eventual consistency]] is often acceptable for our use case
- Leader election is the hard part → links to [[Distributed consensus]]
```

#### 3. Permanent Notes (Zettels)
Your processed, original thoughts — the heart of Zettelkasten.

```markdown
---
id: 202401151430
type: permanent
tags: [distributed-systems, architecture]
---

# Eventual Consistency Trade-offs

Eventual consistency trades **immediate correctness** for **availability**.

Acceptable when:
- Reads vastly outnumber writes
- Temporary staleness is tolerable
- User actions aren't safety-critical

Not acceptable when:
- Financial transactions (use [[Strong consistency]])
- Inventory counts (overselling risk)
- Access control changes

Related:
- [[CAP Theorem]] — fundamental trade-off
- [[DDIA Ch5 - Replication]] — source material
- [[Our API Design Decisions]] — how we applied this
```

### Zettelkasten Vault Structure

```
vault/
├── inbox/                    # Fleeting notes
│   └── 2024-01-15.md
├── literature/               # Source summaries
│   ├── books/
│   ├── articles/
│   └── talks/
├── permanent/                # Your processed ideas
│   ├── programming/
│   ├── management/
│   └── systems/
└── maps/                     # MOCs (Maps of Content)
    ├── distributed-systems.md
    ├── team-management.md
    └── learning-roadmap.md
```

### Maps of Content (MOCs)

MOCs are **index notes** that link related permanent notes:

```markdown
# MOC: Distributed Systems

## Core Concepts
- [[CAP Theorem]]
- [[Eventual Consistency Trade-offs]]
- [[Distributed consensus]]

## Patterns
- [[Event Sourcing]]
- [[CQRS Pattern]]
- [[Saga Pattern]]

## Our Implementations
- [[Our API Design Decisions]]
- [[ADR-005 Database Replication]]

## Learning Resources
- [[DDIA Ch5 - Replication]]
- [[MIT 6.824 Notes]]
```

---

## 🔀 Hybrid Approach: PARA + Zettelkasten

Many people combine both systems:

```
vault/
├── 1-Projects/           # PARA: Active work
├── 2-Areas/              # PARA: Responsibilities
├── 3-Resources/          # Zettelkasten permanent notes!
│   ├── _inbox/           # Fleeting notes
│   ├── _literature/      # Source notes
│   └── ...topics.../     # Permanent notes by topic
├── 4-Archive/            # PARA: Completed
└── _maps/                # MOCs
```

**How it works:**
- **PARA** handles **actionable** work (projects, areas)
- **Zettelkasten** handles **knowledge** (resources become your slip box)

---

## ⚡ Quick Comparison

| Aspect | PARA | Zettelkasten |
|--------|------|--------------|
| **Organizes by** | Actionability | Ideas/concepts |
| **Folder structure** | 4 top-level folders | Note types |
| **Links** | Optional | Essential |
| **Note size** | Any length | Atomic (small) |
| **Best for** | Task/project management | Building knowledge |
| **Maintenance** | Regular archiving | Processing inbox |
| **Learning curve** | Low | Medium-High |

---

## 🎯 Which Should You Choose?

### Choose PARA if:
- You manage many active projects
- You need clear "where does this go?" answers
- You're new to PKM systems
- Your work is primarily project-based
- You like folder organization

### Choose Zettelkasten if:
- You're building long-term knowledge
- You write to think and learn
- You want ideas to compound over time
- You're comfortable with heavy linking
- You read/research extensively

### Choose Hybrid if:
- You do both project work AND knowledge building
- You're a manager who also does technical deep-dives
- You want the best of both worlds

---

## 🚀 Getting Started

### PARA Quick Start

1. Create four folders: `1-Projects`, `2-Areas`, `3-Resources`, `4-Archive`
2. Move existing notes into appropriate folders
3. For each new note, ask: "Is this a project, area, resource, or archive?"
4. Weekly: Archive completed projects

### Zettelkasten Quick Start

1. Create `inbox/` folder for quick captures
2. Create `permanent/` folder for processed notes
3. Daily: Write fleeting notes in inbox
4. Weekly: Process inbox → create permanent notes with links
5. Create MOCs as topics grow

---

## 💡 Implementation Tips

### For Developers

```markdown
# Zettel: Error Handling Philosophy

Write code assuming things will fail.

Defensive patterns:
- Validate all inputs at boundaries
- Use Result types over exceptions when possible
- Fail fast, fail loud

Links:
- [[Rust Error Handling]] — Result<T, E> pattern
- [[Python Exception Hierarchy]]
- [[Our API Error Standards]]
```

### For Managers

```markdown
# Area: Team Management

## Ongoing Responsibilities
- [[1on1 Notes Index]] — All 1:1 documentation
- [[Team Goals 2024]] — Current objectives
- [[Hiring Pipeline]] — Open roles and candidates

## Processes
- [[Performance Review Template]]
- [[New Hire Onboarding Checklist]]
- [[Offboarding Checklist]]
```

---

## 📊 Maintenance Routines

### Weekly Review (30 min)

**PARA:**
- Review active projects — still active?
- Archive anything completed
- Check areas — anything slipping?

**Zettelkasten:**
- Process inbox notes
- Create new permanent notes
- Add links to existing notes

### Monthly Review (1 hour)

- Review project list — reprioritize
- Update MOCs with new connections
- Archive old areas
- Check for orphan notes (no links)

### Quarterly Review (2 hours)

- Major archiving sweep
- Reorganize resources if needed
- Update main MOCs/index notes
- Reflect on system effectiveness

---

## Summary

| System | Core Idea | Best For |
|--------|-----------|----------|
| **PARA** | Organize by actionability | Project & responsibility management |
| **Zettelkasten** | Atomic linked notes | Knowledge building & learning |
| **Hybrid** | Projects in PARA, knowledge in Zettel | Developer-managers |

**The best system is the one you'll actually use.** Start simple, evolve as needed.

---

## Next Steps
→ [[yaml-frontmatter-metadata]] — Add structure with frontmatter
→ [[templates-and-daily-notes]] — Automate note creation
→ [[../03-plugins/dataview-queries]] — Query your notes dynamically

