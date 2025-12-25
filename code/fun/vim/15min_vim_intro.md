# 🚀 15-Minute Vim Intro Session

> **Goal**: Get beginners comfortable enough to edit files and NOT feel trapped!

---

## ⏱️ Session Structure

| Time | Topic |
|------|-------|
| 0:00-1:00 | Why Vim? The Hook |
| 1:00-3:00 | Modes - The Key Concept |
| 3:00-6:00 | Survival Kit - Navigation & Editing |
| 6:00-9:00 | Live Demo - Edit a Real File |
| 9:00-11:00 | Power Moves Teaser |
| 11:00-14:00 | 🔥 **KILLER DEMO** - Visual Block Mode |
| 14:00-15:00 | Resources & Q&A |

---

## 🎣 0:00-1:00 — The Hook (Why Vim?)

**Open with:**
> "Vim is on EVERY server. SSH into any Linux box, Vim is there. 
> Once you learn it, you'll edit at the speed of thought."

**Quick flex** (if appropriate):
- Show a 5-second demo: delete a word, duplicate a line, change inside quotes
- "I didn't touch my mouse once."

---

## 🔀 1:00-4:00 — Modes: The Key Concept

**The #1 thing that confuses beginners!**

```
┌─────────────────────────────────────────────────┐
│                  NORMAL MODE                     │
│            (where you start)                     │
│         Navigate, delete, copy, paste            │
│                                                  │
│     i ↓              ↑ Esc                       │
│                                                  │
│                  INSERT MODE                     │
│            Type text like notepad                │
└─────────────────────────────────────────────────┘
```

### The 3 Modes They Need:

| Mode | How to Enter | What It Does |
|------|--------------|--------------|
| **NORMAL** | `Esc` | Navigate, commands, the "home base" |
| **INSERT** | `i` | Type text normally |
| **COMMAND** | `:` | Save, quit, search |

**Mantra**: "When in doubt, hit `Esc`!"

---

## 🛟 4:00-8:00 — The Survival Kit

### Essential Commands (Write these on board/screen!)

```
┌────────────────────────────────────────────────┐
│            🆘 SURVIVAL COMMANDS 🆘              │
├────────────────────────────────────────────────┤
│  :q!     →  QUIT without saving (ESCAPE HATCH) │
│  :wq     →  Save and quit                      │
│  :w      →  Save                               │
│  i       →  Start typing                       │
│  Esc     →  Stop typing, back to normal        │
└────────────────────────────────────────────────┘
```

### Navigation (Keep mouse hands off!)

```
        ↑
        k
    ← h   l →
        j
        ↓
```

**Memory trick**: "j looks like a down arrow with a hook"

### Quick Wins

| Command | What It Does | Memory Trick |
|---------|--------------|--------------|
| `dd` | Delete line | "delete, delete!" |
| `yy` | Copy (yank) line | "yank yank" |
| `p` | Paste below | "put" |
| `u` | Undo | "undo" |
| `Ctrl+r` | Redo | "redo" |
| `w` | Jump word forward | "word" |
| `b` | Jump word backward | "back" |
| `0` | Start of line | Zero = beginning |
| `$` | End of line | $ = end (like regex) |

---

## 🎬 8:00-12:00 — Live Demo

### Create a practice file together:

```bash
vim practice.txt
```

### Walk through this flow:

1. **"We're in Normal mode"** - press `i`
2. **Type**: "Hello, I'm learning Vim!"
3. **Press `Esc`** - "Back to Normal"
4. **Navigate**: `h j k l` - move around
5. **Go to start**: `0`
6. **Delete word**: `dw` - "delete word"
7. **Undo**: `u`
8. **Copy line**: `yy`
9. **Paste**: `p`
10. **Save & quit**: `:wq`

### Let them try! (if interactive session)

Challenge: "Edit the file, change 'Hello' to 'Hi', save and quit"

---

## ⚡ 12:00-14:00 — Power Moves Teaser

> "This is why Vim users never go back..."

### The Verb + Noun Grammar

```
  d  +  w   =  delete word
  c  +  w   =  change word (delete + insert mode)
  y  +  y   =  yank (copy) line
  d  +  $   =  delete to end of line
```

### Mind-Blowing Combos (quick demo)

| Command | Magic |
|---------|-------|
| `ciw` | **C**hange **I**nside **W**ord |
| `ci"` | Change inside quotes `"hello"` → `""` |
| `di(` | Delete inside parentheses |
| `.` | Repeat last action |
| `*` | Search for word under cursor |
| `gg` | Go to top of file |
| `G` | Go to bottom |
| `/pattern` | Search |

> "Vim commands are composable - learn 10 verbs and 10 nouns, you know 100 commands!"

---

## 🔥 THE KILLER DEMO — Visual Block Mode (Jaws Will Drop)

> "This is the moment they realize Vim is from the future."

### The Setup — Create This Code:

```javascript
const name = "Alice"
const age = 25
const city = "NYC"
const job = "Dev"
const level = "Senior"
```

### Demo 1: Add Semicolons to ALL Lines at Once

```
1. Go to end of first line         →  $
2. Enter Visual Block mode         →  Ctrl+v
3. Select down 4 lines             →  4j
4. Go to end of each line          →  $
5. Append                          →  A
6. Type semicolon                  →  ;
7. Press Escape                    →  Esc
   
🎉 ALL LINES NOW HAVE SEMICOLONS!
```

**Result:**
```javascript
const name = "Alice";
const age = 25;
const city = "NYC";
const job = "Dev";
const level = "Senior";
```

### Demo 2: Comment Out Multiple Lines

```
1. Go to first column              →  0
2. Visual Block mode               →  Ctrl+v
3. Select 4 lines down             →  4j
4. Insert at beginning             →  I
5. Type comment                    →  // 
6. Escape                          →  Esc

🎉 ALL LINES COMMENTED!
```

**Result:**
```javascript
// const name = "Alice";
// const age = 25;
// const city = "NYC";
// const job = "Dev";
// const level = "Senior";
```

### Demo 3: Rename Variable Prefix (const → let)

```
1. Visual Block select "const"     →  Ctrl+v → 4j → e
2. Change selection                →  c
3. Type new text                   →  let
4. Escape                          →  Esc

🎉 ALL "const" → "let" SIMULTANEOUSLY!
```

### Why This Blows Minds 🤯

| Normal Editors | Vim Visual Block |
|----------------|------------------|
| Click, type, click, type, click... | One motion, ALL lines |
| Install "multi-cursor" plugin | Built-in since 1991 |
| Hope it works | It ALWAYS works |

> **Presenter tip**: Do this slowly. Let them see each step. 
> The "Esc" moment when all lines change at once = 🤯

---

## 📚 14:00-15:00 — Resources & Close

### Next Steps

1. **Built-in tutor**: Run `vimtutor` in terminal (30 min tutorial)
2. **Practice daily**: Use Vim for small edits, build muscle memory
3. **Cheat sheet**: Keep one nearby first week

### Recommended Resources

- 🎮 [Vim Adventures](https://vim-adventures.com/) - Learn Vim as a game
- 📺 [ThePrimeagen](https://www.youtube.com/c/ThePrimeagen) - Vim motions content
- 📖 `:help` - Built-in docs (type `:help` in Vim)

### The Challenge

> "For the next week, resist the urge to use your mouse in Vim.
> It'll feel slow at first, then suddenly it clicks. 
> After 2 weeks, you'll wonder how you ever lived without it."

---

## 🎁 Bonus: Quick Reference Card

```
╔══════════════════════════════════════════════════════╗
║               VIM SURVIVAL CARD                       ║
╠══════════════════════════════════════════════════════╣
║  ESCAPE HATCH    :q!        Quit, forget everything  ║
║  SAVE & QUIT     :wq        You're done!             ║
║  TYPE TEXT       i          Enter insert mode        ║
║  STOP TYPING     Esc        Back to normal           ║
║  UNDO            u          Undo last change         ║
║  MOVE            h j k l    ← ↓ ↑ →                  ║
║  DELETE LINE     dd         Boom, line gone          ║
║  COPY LINE       yy         Yank it                  ║
║  PASTE           p          Put it                   ║
╚══════════════════════════════════════════════════════╝
```

---

## 🗣️ Presenter Notes

- **Energy matters**: Vim has a steep learning curve reputation - keep it fun!
- **Hands-on > slides**: Get them typing ASAP
- **Don't overwhelm**: 10 commands mastered > 50 commands forgotten
- **Address the fear**: Everyone's scared of being "trapped" - teach `:q!` first!
- **Personal story**: Share your "aha moment" with Vim

---

*"Vim: Because life's too short for slow text editing."* 🔥

