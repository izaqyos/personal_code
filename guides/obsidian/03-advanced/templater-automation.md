# Templater for Advanced Automation

> Go beyond basic templates with JavaScript-powered automation.

---

## 🔧 What is Templater?

**Templater** is a community plugin that supercharges Obsidian's templates:
- Dynamic content insertion (dates, prompts, calculations)
- JavaScript execution within templates
- File manipulation (create, move, rename)
- System commands and external scripts

**Developer analogy:** It's like having a template engine (Jinja/Handlebars) with full JS access.

---

## 🚀 Getting Started

### Installation

```
Settings → Community plugins → Browse → "Templater" → Install → Enable
```

### Configuration

```
Settings → Templater → Template folder location → templates/
```

### Key Settings

| Setting | Recommended |
|---------|-------------|
| Template folder | `templates/` |
| Trigger on new file | ✅ Enable |
| Enable system commands | ⚠️ Only if needed |
| Enable JS execution | ✅ Enable (for power features) |

---

## 📝 Templater Syntax

### Basic Commands

```markdown
<% tp.date.now() %>                    <!-- Current date -->
<% tp.date.now("YYYY-MM-DD") %>        <!-- Formatted date -->
<% tp.file.title %>                    <!-- Current file name -->
<% tp.file.folder() %>                 <!-- Current folder -->
```

### Execution vs Output

```markdown
<%* /* Code that runs but outputs nothing */ %>
<% /* Code that outputs result */ %>
```

### User Input

```markdown
<% tp.system.prompt("Enter project name") %>
<% tp.system.suggester(["High", "Medium", "Low"], ["high", "medium", "low"]) %>
```

---

## 🎯 Developer Templates

### 1. Daily Note Template

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
week: <% tp.date.now("YYYY-[W]ww") %>
type: daily
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

## 🎯 Today's Focus
- 

## 📋 Tasks
- [ ] 

## 📝 Notes


## 🔗 Links
- Previous: [[<% tp.date.now("YYYY-MM-DD", -1) %>]]
- Next: [[<% tp.date.now("YYYY-MM-DD", 1) %>]]
- Weekly: [[<% tp.date.now("YYYY-[W]ww") %>]]

## 📊 End of Day
### What went well?

### What could improve?

```

### 2. Meeting Notes Template

```markdown
<%*
const meetingType = await tp.system.suggester(
    ["1:1", "Team Sync", "Project", "Interview", "Other"],
    ["1on1", "sync", "project", "interview", "other"]
);
const attendees = await tp.system.prompt("Attendees (comma-separated)");
-%>
---
date: <% tp.date.now("YYYY-MM-DD") %>
time: <% tp.date.now("HH:mm") %>
type: meeting/<% meetingType %>
attendees: [<% attendees.split(",").map(a => a.trim()).join(", ") %>]
status: active
---

# <% meetingType.toUpperCase() %> - <% tp.date.now("YYYY-MM-DD") %>

## 👥 Attendees
<% attendees.split(",").map(a => `- ${a.trim()}`).join("\n") %>

## 📋 Agenda
1. 

## 📝 Notes


## ✅ Action Items
- [ ] 

## 🔗 Follow-ups

```

### 3. Project Template

```markdown
<%*
const projectName = await tp.system.prompt("Project name");
const priority = await tp.system.suggester(
    ["🔴 High", "🟡 Medium", "🟢 Low"],
    ["high", "medium", "low"]
);
const dueDate = await tp.system.prompt("Due date (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD", 30));
await tp.file.rename(projectName.toLowerCase().replace(/\s+/g, '-'));
-%>
---
type: project
status: active
priority: <% priority %>
created: <% tp.date.now("YYYY-MM-DD") %>
due: <% dueDate %>
tags: [project]
---

# <% projectName %>

## 📋 Overview


## 🎯 Goals
1. 

## 📊 Status
- [ ] Planning
- [ ] In Progress
- [ ] Review
- [ ] Complete

## 📝 Notes


## ✅ Tasks
- [ ] 

## 🔗 Related
- 

```

### 4. 1:1 Template

```markdown
<%*
const person = await tp.system.suggester(
    ["Alice", "Bob", "Carol", "David"],
    ["alice", "bob", "carol", "david"]
);
const fileName = `${tp.date.now("YYYY-MM-DD")}-${person}`;
await tp.file.rename(fileName);
-%>
---
date: <% tp.date.now("YYYY-MM-DD") %>
person: <% person %>
type: 1on1
---

# 1:1 with <% person.charAt(0).toUpperCase() + person.slice(1) %> - <% tp.date.now("MMMM D, YYYY") %>

## 🌡️ Check-in
How are you feeling? (1-5): 

## 📋 Their Updates
- 

## 💬 Discussion Points
### From Them
- 

### From Me
- 

## 🚧 Blockers / Challenges
- 

## 🌱 Growth & Development
- 

## ✅ Action Items
### For Them
- [ ] 

### For Me
- [ ] 

## 📝 Private Notes
<!-- Not to be shared -->


---
Previous: [[<% tp.date.now("YYYY-MM-DD", -14) %>-<% person %>|Last 1:1]]

```

### 5. Bug Report Template

```markdown
<%*
const severity = await tp.system.suggester(
    ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
    ["critical", "high", "medium", "low"]
);
const component = await tp.system.prompt("Component/Service");
-%>
---
type: bug
severity: <% severity %>
component: <% component %>
reported: <% tp.date.now("YYYY-MM-DD") %>
status: open
assignee: 
---

# Bug: <% tp.file.title %>

## 📋 Summary


## 🔄 Steps to Reproduce
1. 
2. 
3. 

## ✅ Expected Behavior


## ❌ Actual Behavior


## 📸 Screenshots/Logs

```
<!-- Paste logs here -->
```

## 🔍 Investigation Notes


## 💡 Potential Solutions
1. 

## ✅ Resolution


```

### 6. ADR (Architecture Decision Record)

```markdown
<%*
const adrNumber = await tp.system.prompt("ADR Number", "001");
const title = await tp.system.prompt("Decision Title");
const status = await tp.system.suggester(
    ["Proposed", "Accepted", "Deprecated", "Superseded"],
    ["proposed", "accepted", "deprecated", "superseded"]
);
await tp.file.rename(`ADR-${adrNumber}-${title.toLowerCase().replace(/\s+/g, '-')}`);
-%>
---
type: adr
number: <% adrNumber %>
title: <% title %>
status: <% status %>
date: <% tp.date.now("YYYY-MM-DD") %>
deciders: []
---

# ADR-<% adrNumber %>: <% title %>

## Status
**<% status.toUpperCase() %>** — <% tp.date.now("YYYY-MM-DD") %>

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive
- 

### Negative
- 

### Risks
- 

## Alternatives Considered

### Option 1: [Name]
**Pros:**
- 

**Cons:**
- 

### Option 2: [Name]
**Pros:**
- 

**Cons:**
- 

## References
- 

```

---

## ⚡ Advanced Templater Functions

### File Operations

```markdown
<%* 
// Rename file based on content
await tp.file.rename("new-name");

// Move file to folder
await tp.file.move("/projects/" + tp.file.title);

// Create file from template
await tp.file.create_new(tp.file.find_tfile("templates/project"), "new-project");

// Get file content
const content = await tp.file.content;
-%>
```

### Date Manipulation

```markdown
<% tp.date.now("YYYY-MM-DD") %>           <!-- Today -->
<% tp.date.now("YYYY-MM-DD", 7) %>        <!-- 7 days from now -->
<% tp.date.now("YYYY-MM-DD", -1) %>       <!-- Yesterday -->
<% tp.date.now("YYYY-[W]ww") %>           <!-- Week number -->
<% tp.date.weekday("YYYY-MM-DD", 1) %>    <!-- Next Monday -->
```

### Cursor Placement

```markdown
## Notes
<% tp.file.cursor() %>
<!-- Cursor will be placed here after template insertion -->
```

### Multiple Cursors

```markdown
## Field 1
<% tp.file.cursor(1) %>

## Field 2  
<% tp.file.cursor(2) %>
```

### Web Requests (with system commands)

```markdown
<%*
// Requires enabling system commands
const response = await tp.system.fetch("https://api.example.com/data");
const data = JSON.parse(response);
-%>
API Response: <% data.title %>
```

---

## 🔄 Automation Workflows

### Auto-Create Daily Note on Startup

```
Settings → Templater → Trigger Templater on new file creation → Enable
Settings → Daily notes → Open daily note on startup → Enable
```

### Folder-Specific Templates

```
Settings → Templater → Folder Templates
Add: projects/ → templates/project.md
Add: meetings/ → templates/meeting.md
Add: 1on1s/ → templates/1on1.md
```

Now any file created in these folders auto-applies the template!

### QuickAdd Integration

Combine Templater with QuickAdd for rapid note creation:
1. Install QuickAdd plugin
2. Create macro that runs Templater template
3. Assign hotkey

---

## 📋 My Template Collection

```
templates/
├── daily-note.md
├── weekly-review.md
├── meeting/
│   ├── 1on1.md
│   ├── team-sync.md
│   └── project.md
├── work/
│   ├── project.md
│   ├── adr.md
│   └── bug-report.md
├── learning/
│   ├── book-notes.md
│   └── course-notes.md
└── snippets/
    ├── code-block.md
    └── callout.md
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Template not found | Check template folder path in settings |
| JS not executing | Enable "Enable JavaScript execution" |
| Prompt not appearing | Check for syntax errors in template |
| Date wrong format | Use moment.js format strings |
| File not renaming | Ensure `await` before `tp.file.rename()` |

### Debug Mode

Add to template for debugging:

```markdown
<%*
console.log("Debug:", tp.file.title);
console.log("Folder:", tp.file.folder());
-%>
```

Check Developer Console (`Cmd+Option+I`) for output.

---

## Summary

Templater enables **intelligent automation**:

| Feature | Use Case |
|---------|----------|
| Dynamic dates | Daily notes, deadlines |
| User prompts | Customized templates |
| Suggesters | Dropdown selections |
| File operations | Auto-rename, organize |
| JavaScript | Complex logic, calculations |
| Folder templates | Auto-apply by location |

**Start with:** Daily note template with dates and navigation links.

---

## Next Steps
→ [[git-integration]] — Version control your vault
→ [[dataview-queries]] — Query your templated notes

