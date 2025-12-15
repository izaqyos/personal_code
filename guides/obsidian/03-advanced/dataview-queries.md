# Dataview Queries for Dynamic Content

> SQL-like queries for your notes — turn your vault into a queryable database.

---

## 🗄️ What is Dataview?

**Dataview** is a plugin that treats your vault as a database:
- Query notes by metadata, tags, folders
- Create dynamic tables, lists, task views
- Auto-updating — changes reflect immediately

**Developer analogy:** It's like having SQL for your markdown files.

---

## 🚀 Getting Started

### Installation

```
Settings → Community plugins → Browse → "Dataview" → Install → Enable
```

### Enable JavaScript Queries (Optional)

```
Settings → Dataview → Enable JavaScript Queries
```

This unlocks `dataviewjs` for complex logic.

---

## 📝 Basic Query Types

### LIST — Simple Note Lists

```dataview
LIST
FROM "projects"
WHERE status = "active"
SORT file.mtime DESC
```

**Output:** Bulleted list of matching notes.

### TABLE — Structured Data

```dataview
TABLE 
    status as "Status",
    priority as "Priority",
    file.mtime as "Modified"
FROM "projects"
WHERE status != "archived"
SORT priority DESC
```

**Output:** Table with columns.

### TASK — Task Aggregation

```dataview
TASK
FROM "daily"
WHERE !completed
GROUP BY file.link
```

**Output:** All incomplete tasks, grouped by source note.

### CALENDAR — Date Visualization

```dataview
CALENDAR file.ctime
FROM "journal"
```

**Output:** Calendar with dots on dates that have notes.

---

## 🔍 Query Anatomy

```dataview
[QUERY TYPE]              -- LIST, TABLE, TASK, CALENDAR
[FIELDS]                  -- What columns to show (TABLE only)
FROM [SOURCE]             -- Where to look
WHERE [FILTER]            -- Conditions
SORT [FIELD] [ASC|DESC]   -- Ordering
GROUP BY [FIELD]          -- Grouping
LIMIT [NUMBER]            -- Max results
```

---

## 📂 Source Expressions (FROM)

### By Folder

```dataview
LIST FROM "projects"           -- Folder path
LIST FROM "projects/active"    -- Nested folder
```

### By Tag

```dataview
LIST FROM #project             -- Notes with tag
LIST FROM #project/active      -- Nested tag
```

### By Link

```dataview
LIST FROM [[Project Hub]]      -- Notes linking TO this note
LIST FROM outgoing([[My Note]])-- Notes this note links to
```

### Combine Sources

```dataview
LIST FROM "projects" OR #archived
LIST FROM "work" AND #priority
LIST FROM "notes" AND -"notes/archive"  -- Exclude subfolder
```

---

## 🎯 Developer Use Cases

### 1. Active Projects Dashboard

```dataview
TABLE 
    status as "Status",
    priority as "Priority",
    due as "Due Date",
    file.mtime as "Updated"
FROM "projects"
WHERE status = "active"
SORT priority DESC, due ASC
```

### 2. All TODOs Across Vault

```dataview
TASK
FROM ""
WHERE !completed AND !contains(text, "#someday")
GROUP BY file.link
SORT file.mtime DESC
LIMIT 50
```

### 3. Recently Modified Notes

```dataview
TABLE file.mtime as "Modified", file.size as "Size"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```

### 4. Team 1:1 Notes Index

```dataview
TABLE 
    date as "Date",
    mood as "Mood",
    length(file.tasks) as "Action Items"
FROM "1on1s"
SORT date DESC
```

### 5. ADR (Architecture Decision Records)

```dataview
TABLE
    status as "Status",
    date as "Date",
    deciders as "Deciders"
FROM "adr"
SORT date DESC
```

### 6. Learning Progress Tracker

```dataview
TABLE
    progress as "Progress",
    hours as "Hours",
    last_studied as "Last Studied"
FROM #learning
SORT last_studied DESC
```

### 7. Code Snippets Library

```dataview
TABLE
    language as "Language",
    tags as "Tags"
FROM "snippets"
WHERE language
SORT language ASC
```

---

## 📊 Working with Frontmatter

### Sample Note with Frontmatter

```yaml
---
type: project
status: active
priority: high
due: 2024-02-15
tags: [backend, api]
assignee: alice
---

# API Redesign Project

Project content here...
```

### Query Frontmatter Fields

```dataview
TABLE status, priority, due, assignee
FROM "projects"
WHERE type = "project"
```

### Date Comparisons

```dataview
TABLE due, status
FROM "projects"
WHERE due <= date(today) + dur(7 days)
AND status != "completed"
SORT due ASC
```

---

## ⚡ Inline Queries

Embed values directly in text:

```markdown
Total active projects: `= length(filter(pages("projects"), (p) => p.status = "active"))`

Last modified: `= this.file.mtime`

Days until deadline: `= (this.due - date(today)).days`
```

---

## 🔧 DataviewJS (Advanced)

For complex logic, use JavaScript:

### Basic DataviewJS

```dataviewjs
// List all projects with custom formatting
const projects = dv.pages('"projects"')
    .where(p => p.status === "active")
    .sort(p => p.priority, 'desc');

dv.table(
    ["Project", "Priority", "Due"],
    projects.map(p => [p.file.link, p.priority, p.due])
);
```

### Grouped Table

```dataviewjs
// Group tasks by status
const tasks = dv.pages('"projects"')
    .groupBy(p => p.status);

for (let group of tasks) {
    dv.header(3, group.key || "No Status");
    dv.table(
        ["Name", "Priority"],
        group.rows.map(p => [p.file.link, p.priority])
    );
}
```

### Custom Rendering

```dataviewjs
// Progress bars for projects
const projects = dv.pages('"projects"')
    .where(p => p.progress !== undefined);

for (let p of projects) {
    const bar = "█".repeat(p.progress / 10) + "░".repeat(10 - p.progress / 10);
    dv.paragraph(`${p.file.link}: ${bar} ${p.progress}%`);
}
```

### Aggregations

```dataviewjs
// Summary statistics
const projects = dv.pages('"projects"');

const stats = {
    total: projects.length,
    active: projects.where(p => p.status === "active").length,
    completed: projects.where(p => p.status === "completed").length,
    avgPriority: projects.values.map(p => p.priority || 0).reduce((a, b) => a + b, 0) / projects.length
};

dv.paragraph(`
📊 **Project Statistics**
- Total: ${stats.total}
- Active: ${stats.active}
- Completed: ${stats.completed}
- Avg Priority: ${stats.avgPriority.toFixed(1)}
`);
```

---

## 📋 Useful Functions

### String Functions

```dataview
WHERE contains(file.name, "project")
WHERE startswith(file.name, "2024")
WHERE regexmatch("^API", file.name)
```

### Date Functions

```dataview
WHERE file.ctime >= date(2024-01-01)
WHERE due < date(today)
WHERE date(today) - file.mtime <= dur(7 days)
```

### List Functions

```dataview
WHERE contains(tags, "important")
WHERE length(file.tasks) > 0
WHERE any(tags, (t) => startswith(t, "project"))
```

### Math Functions

```dataview
TABLE sum(hours) as "Total Hours"
FROM #learning
GROUP BY file.folder
```

---

## 🎯 Template: Weekly Review Query

Create a note for weekly reviews:

```markdown
# Weekly Review - {{date}}

## 📝 Notes Created This Week

```dataview
LIST
FROM ""
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
\```

## ✅ Tasks Completed

```dataview
TASK
FROM ""
WHERE completed
AND completion >= date(today) - dur(7 days)
\```

## 🔴 Overdue Tasks

```dataview
TASK
FROM ""
WHERE !completed
AND due < date(today)
SORT due ASC
\```

## 📊 Activity Summary

```dataviewjs
const week = dv.pages("")
    .where(p => p.file.ctime >= dv.date("today") - dv.duration("7 days"));

dv.paragraph(`
- Notes created: ${week.length}
- Total tasks: ${week.file.tasks.length}
`);
\```
```

---

## ⚠️ Performance Tips

| Tip | Why |
|-----|-----|
| Use specific folders in FROM | Limits scan scope |
| Avoid `FROM ""` in large vaults | Scans everything |
| Cache complex queries in notes | Reduce recalculation |
| Use LIMIT for large result sets | Faster rendering |
| Prefer LIST over TABLE when possible | Less overhead |

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Query shows nothing | Check folder path, field names |
| Dates not comparing | Ensure `date()` wrapper on YAML dates |
| Field not found | Check YAML spelling, use lowercase |
| Slow queries | Add FROM clause, use LIMIT |
| Inline query not rendering | Check backtick syntax |

---

## Summary

Dataview transforms your vault into a **queryable knowledge base**:

| Query Type | Use Case |
|------------|----------|
| LIST | Simple note indexes |
| TABLE | Structured dashboards |
| TASK | Cross-vault task views |
| CALENDAR | Date-based visualization |
| Inline | Embed values in text |
| DataviewJS | Complex logic & custom rendering |

**Start simple:** One TABLE query in your home note. Build from there.

---

## Next Steps
→ [[templater-automation]] — Automate note creation
→ [[git-integration]] — Version control your vault

