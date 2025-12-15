# Embedding & Transclusion

> Include content from other notes without duplication — the DRY principle for your vault.

---

## 🔗 What is Transclusion?

**Transclusion** is embedding the content of one note inside another. Think of it like:
- `#include` in C/C++
- `import` in Python/JavaScript
- `{% include %}` in Jinja/Django templates

The embedded content stays **synced** — edit the source, and all embeds update automatically.

---

## 📝 Basic Embedding Syntax

### Embed Entire Note

```markdown
![[Note Name]]
```

This embeds the full content of `Note Name.md` into the current note.

### Embed Specific Heading

```markdown
![[Note Name#Heading]]
```

Only embeds content under that specific heading.

### Embed Specific Block

```markdown
![[Note Name#^block-id]]
```

Embeds a single paragraph or block (requires block ID).

### Embed with Alias

```markdown
![[Note Name|Custom Display Text]]
```

---

## 🎯 Creating Block References

### Auto-generated Block IDs

1. Link to any paragraph: type `![[Note Name#^`
2. Obsidian shows matching blocks
3. Select one — Obsidian auto-adds a block ID like `^a1b2c3`

### Manual Block IDs

Add `^my-custom-id` at the end of any paragraph:

```markdown
This is an important definition. ^definition-api

The API accepts JSON payloads with authentication headers. ^api-usage
```

Then embed with:
```markdown
![[API Design#^definition-api]]
```

**Developer tip:** Use semantic block IDs like `^decision-rationale`, `^key-takeaway`, `^code-example`.

---

## 🖼️ Embedding Other Content

### Images

```markdown
![[image.png]]
![[diagram.svg]]
```

### With Size Control

```markdown
![[image.png|400]]        <!-- Width: 400px -->
![[image.png|400x300]]    <!-- Width x Height -->
```

### PDFs

```markdown
![[document.pdf]]
![[document.pdf#page=5]]  <!-- Specific page -->
```

### Audio/Video

```markdown
![[recording.mp3]]
![[demo.mp4]]
```

### Canvas

```markdown
![[project-architecture.canvas]]
```

---

## 💡 Use Cases for Developers & Managers

### 1. Reusable Code Snippets

**Source note:** `snippets/python-logging.md`
```markdown
## Python Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
``` ^python-logging-setup
```

**In project notes:**
```markdown
## Logging Configuration

We use standard Python logging:

![[python-logging.md#^python-logging-setup]]

Customizations for this project:
- Log level: DEBUG in dev, WARNING in prod
```

### 2. Shared Team Context

**Source:** `team/engineering-principles.md`
```markdown
## Our Core Principles

1. **Ship incrementally** — Small PRs, fast feedback
2. **Automate everything** — CI/CD, testing, deployments
3. **Document decisions** — ADRs for major choices
4. **Own your code** — Monitor, debug, improve
^core-principles
```

**In onboarding doc:**
```markdown
# New Developer Onboarding

## Team Values

![[engineering-principles#^core-principles]]

Learn more: [[Engineering Principles]]
```

### 3. Meeting Templates with Embedded Agendas

**Standing agenda:** `templates/1on1-agenda.md`
```markdown
## Standard 1:1 Agenda

1. **Check-in** — How are you doing?
2. **Updates** — What's on your mind?
3. **Blockers** — Anything I can help with?
4. **Growth** — Career development topics
5. **Action items** — What are we committing to?
^standard-agenda
```

**In each 1:1 note:**
```markdown
# 1:1 with Alice - 2024-01-15

![[1on1-agenda#^standard-agenda]]

### Notes
- ...
```

### 4. Architecture Decision Records (ADRs)

**ADR template pattern:**
```markdown
# ADR-005: Use PostgreSQL for Primary Database

## Context
![[project-requirements#^database-requirements]]

## Decision
PostgreSQL with read replicas.

## Consequences
![[postgresql-tradeoffs#^scaling-limitations]]
```

### 5. Daily Notes with Embedded Goals

**Weekly goals:** `planning/2024-W03-goals.md`
```markdown
## Week 3 Goals

- [ ] Complete API v2 design review
- [ ] Finish performance testing
- [ ] Write Q1 roadmap draft
^weekly-goals
```

**Daily note:**
```markdown
# 2024-01-15

## This Week's Goals
![[2024-W03-goals#^weekly-goals]]

## Today's Focus
- API v2 design review meeting at 2pm
```

---

## ⌨️ Keyboard Shortcuts

| Action | Method |
|--------|--------|
| Insert embed | Type `![[` and search |
| Embed heading | `![[Note#` then select |
| Embed block | `![[Note#^` then select |
| Toggle preview | `Cmd+E` |
| Follow embed to source | `Cmd+Click` on embed |

---

## 🎨 Styling Embeds with CSS

Embeds can be styled with CSS snippets. Create `.obsidian/snippets/embeds.css`:

```css
/* Add border to embedded content */
.markdown-embed {
    border-left: 3px solid var(--interactive-accent);
    padding-left: 1em;
    margin: 1em 0;
}

/* Subtle background for embeds */
.markdown-embed-content {
    background: var(--background-secondary);
    padding: 0.5em;
    border-radius: 4px;
}

/* Hide embed title */
.markdown-embed-title {
    display: none;
}
```

---

## 🎯 Best Practices

### Do's ✅

- **Embed reusable content** — Definitions, principles, templates
- **Use meaningful block IDs** — `^api-response-format` not `^abc123`
- **Embed headings** for context — Often better than blocks
- **Keep source notes focused** — Single-responsibility principle
- **Document your embeds** — Add context around embedded content

### Don'ts ❌

- Don't over-embed — If you're embedding 90%, just link instead
- Don't create circular embeds — A embeds B embeds A
- Don't embed large notes — Performance impact
- Don't rely on embeds for structure — Your notes should stand alone
- Don't forget to check broken embeds — Renamed/deleted notes break them

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Embed not rendering | Check preview mode (`Cmd+E`) |
| Block not found | Verify block ID exists in source |
| Missing content after rename | Update embed links or use alias |
| Embed shows raw syntax | Missing `!` before `[[` |
| Performance issues | Reduce number of embeds per note |

---

## 🔮 Advanced: Dataview + Embeds

Combine with Dataview for dynamic embeds:

```dataview
TABLE WITHOUT ID embed(link(file.link)) as "Team Member Notes"
FROM "team/members"
WHERE contains(tags, "active")
```

This dynamically embeds content from multiple notes!

---

## Summary

Transclusion enables **DRY note-taking**:

| Embed Type | Syntax | Use Case |
|------------|--------|----------|
| Full note | `![[Note]]` | Include entire document |
| Heading | `![[Note#Heading]]` | Section of a document |
| Block | `![[Note#^block-id]]` | Single paragraph/list |
| Image | `![[image.png\|400]]` | Sized images |
| PDF | `![[doc.pdf#page=5]]` | Specific pages |

**Key benefits:**
- 🔄 **Single source of truth** — Update once, sync everywhere
- 📦 **Modular notes** — Compose complex docs from simple parts
- 🔍 **Better search** — Content lives in searchable source notes
- 🧹 **Easier maintenance** — Fix in one place

---

## Next Steps
→ [[yaml-frontmatter-metadata]] — Structured metadata for your notes
→ [[zettelkasten-para-systems]] — Organizational frameworks for your vault

