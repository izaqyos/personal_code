# Canvas & Visual Thinking

> When text isn't enough — spatial organization for complex ideas.

---

## 🎨 What is Canvas?

Canvas is Obsidian's built-in **infinite whiteboard** for:
- Mind mapping
- System architecture diagrams
- Project planning
- Brainstorming
- Connecting ideas visually

**Developer analogy:** It's like Miro/FigJam/Excalidraw, but integrated with your vault.

---

## 🚀 Getting Started

### Create a Canvas
1. `Cmd+P` → "Canvas: Create new canvas"
2. Or: Right-click folder → New canvas
3. File extension: `.canvas`

### Canvas Elements

| Element | How to Add | Use Case |
|---------|------------|----------|
| **Card** | Double-click empty space | Quick notes, ideas |
| **Note** | Drag `.md` file onto canvas | Link existing notes |
| **Image** | Drag image file | Visual references |
| **Website** | Drag URL | Embed web content |
| **Group** | Select items → Right-click → Group | Organize clusters |

---

## ⌨️ Canvas Shortcuts

| Action | Shortcut |
|--------|----------|
| New card | Double-click empty space |
| Connect nodes | Drag from edge of card |
| Select multiple | `Shift+Click` or drag box |
| Group selection | `Cmd+G` |
| Zoom to fit | `Cmd+0` |
| Zoom in/out | `Cmd++` / `Cmd+-` or scroll |
| Pan | Space + drag, or middle-click drag |
| Delete | `Backspace` or `Delete` |
| Duplicate | `Cmd+D` |
| Edit card | Double-click card |
| Exit edit mode | `Esc` |

---

## 🗺️ Use Cases for Developers & Managers

### 1. System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│     API     │────▶│  Database   │
│   (React)   │     │   (FastAPI) │     │  (Postgres) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│    Auth     │     │    Cache    │
│  (Auth0)    │     │   (Redis)   │
└─────────────┘     └─────────────┘
```

Create this in Canvas:
1. Add cards for each component
2. Connect with arrows
3. Group by domain (frontend, backend, data)
4. Link to detailed notes: `[[API Design]]`, `[[Database Schema]]`

### 2. Project Planning / Roadmap

```
┌─────────────────────────────────────────────────────────┐
│                        Q1 2024                          │
├─────────────┬─────────────┬─────────────┬──────────────┤
│    Jan      │     Feb     │     Mar     │   Milestone  │
├─────────────┼─────────────┼─────────────┼──────────────┤
│ [[Auth]]    │ [[API v2]]  │ [[Launch]]  │  🚀 v2.0     │
│ [[Setup]]   │ [[Testing]] │ [[Docs]]    │              │
└─────────────┴─────────────┴─────────────┴──────────────┘
```

### 3. Team Org Chart

```
                    ┌──────────────┐
                    │ [[CTO]]      │
                    │ Engineering  │
                    └──────┬───────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ [[Manager A]]│ │ [[Manager B]]│ │ [[Manager C]]│
    │ Frontend     │ │ Backend      │ │ Platform     │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │               │               │
     ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
     ▼           ▼   ▼           ▼   ▼           ▼
 [[Dev 1]]  [[Dev 2]]  [[Dev 3]]  [[Dev 4]]  [[Dev 5]]
```

### 4. Decision Making / Options Analysis

```
┌─────────────────────────────────────────────────────────┐
│                    DECISION: Database Choice            │
└─────────────────────────────────────────────────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PostgreSQL │     │   MongoDB   │     │  DynamoDB   │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ ✅ ACID     │     │ ✅ Flexible │     │ ✅ Scalable │
│ ✅ SQL      │     │ ✅ Fast dev │     │ ✅ Managed  │
│ ❌ Scaling  │     │ ❌ No joins │     │ ❌ Vendor   │
│ ⭐ Team exp │     │ ❌ Eventual │     │ ❌ Learning │
└─────────────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│              CHOSEN: PostgreSQL                         │
│              See: [[ADR-003 Database Choice]]           │
└─────────────────────────────────────────────────────────┘
```

### 5. Learning Mind Map

```
                         ┌──────────────┐
                         │   [[Python]] │
                         └──────┬───────┘
          ┌──────────────────┬──┴───┬────────────────────┐
          ▼                  ▼      ▼                    ▼
   ┌──────────────┐   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ Data Types   │   │ Control  │  │ Functions│  │  OOP     │
   └──────┬───────┘   │  Flow    │  └────┬─────┘  └────┬─────┘
          │           └──────────┘       │             │
    ┌─────┴─────┐                  ┌─────┴─────┐ ┌─────┴─────┐
    ▼           ▼                  ▼           ▼ ▼           ▼
 [[Lists]]  [[Dicts]]         [[Lambda]]  [[Args]] [[Classes]] [[Inherit]]
```

### 6. Meeting / Brainstorm Capture

Use canvas during meetings to:
1. Capture ideas as cards (quick!)
2. Group related ideas in real-time
3. Draw connections
4. Convert to action items after

---

## 🎯 Canvas Best Practices

### Do's ✅
- **Link to notes** — Cards can contain `[[links]]`
- **Embed notes** — Drag notes onto canvas for live content
- **Use groups** — Color-code and organize
- **Keep it focused** — One canvas per topic/project
- **Name meaningfully** — `project-x-architecture.canvas`

### Don'ts ❌
- Don't put everything on one canvas
- Don't use canvas for linear content (use notes)
- Don't forget to link to detailed notes
- Don't make it too zoomed out to read

---

## 🔧 Canvas Settings

**Settings → Core plugins → Canvas:**
- Default new card dimensions
- Snap to grid
- Display card labels

---

## 🎯 Exercise: Create Your Learning Map

Create a canvas called `learning-roadmap.canvas`:

1. **Add cards** for each of your 6 learning tracks:
   - Python
   - LeetCode
   - Obsidian
   - Networking
   - Prompt Engineering
   - Rust

2. **Connect** related topics (Python ↔ LeetCode)

3. **Group** by:
   - 🟢 Active (currently working on)
   - 🟡 In Progress (started)
   - ⚪ Planned (future)

4. **Link** each card to its main note:
   - Double-click card
   - Type `[[Python Learning]]` etc.

5. **Add sub-topics** branching from main cards

---

## 🔮 Alternative: Excalidraw Plugin

For more **hand-drawn style** diagrams, consider the **Excalidraw** plugin:

| Feature | Canvas | Excalidraw |
|---------|--------|------------|
| Built-in | ✅ Yes | Plugin |
| Style | Clean, app-like | Hand-drawn |
| Drawing tools | Basic | Full suite |
| Note embedding | ✅ Excellent | ✅ Good |
| Export | PNG, JSON | PNG, SVG |
| Best for | Organization | Diagrams |

We'll cover Excalidraw in the plugins section!

---

## Summary

Canvas is your **spatial thinking** tool:
- 🗺️ **Architecture** — System design, tech stack
- 📅 **Planning** — Roadmaps, timelines
- 👥 **People** — Org charts, stakeholder maps
- 🤔 **Decisions** — Options analysis, trade-offs
- 🧠 **Learning** — Mind maps, concept relationships
- 💡 **Brainstorming** — Free-form idea capture

---

## Next: Phase 3
→ [[03-advanced/dataview-queries]] — SQL-like queries for your notes


