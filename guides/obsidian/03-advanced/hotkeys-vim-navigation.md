# Hotkeys & Vim-Style Navigation

> Keyboard-first workflows for developers who hate the mouse.

---

## ⌨️ Why Hotkeys Matter

Every mouse movement is context-switching. For developers used to Vim/NeoVim:
- **Muscle memory** transfers from your editor
- **Flow state** stays uninterrupted
- **Speed** increases dramatically

---

## 🔧 Built-in Vim Mode

### Enable Vim Mode

```
Settings → Editor → Vim key bindings → Toggle ON
```

### What You Get

| Feature | Status |
|---------|--------|
| Normal/Insert/Visual modes | ✅ Full support |
| hjkl navigation | ✅ Works |
| Text objects (iw, ap, etc.) | ✅ Works |
| Search (/, ?, n, N) | ✅ Works |
| Registers (", +) | ✅ Works |
| Macros (q, @) | ✅ Works |
| Marks (m, ') | ⚠️ Limited |
| Ex commands (:w, :q) | ⚠️ Limited |

---

## 🎯 Essential Obsidian Hotkeys

### Navigation (Memorize These!)

| Action | Default | Recommended |
|--------|---------|-------------|
| Quick switcher | `Cmd+O` | Keep |
| Command palette | `Cmd+P` | Keep |
| Search in files | `Cmd+Shift+F` | Keep |
| Go back | `Cmd+Alt+←` | `Ctrl+O` (Vim-style) |
| Go forward | `Cmd+Alt+→` | `Ctrl+I` (Vim-style) |
| Focus file explorer | None | `Cmd+E` |
| Focus editor | None | `Cmd+Shift+E` |

### Note Operations

| Action | Default | Recommended |
|--------|---------|-------------|
| New note | `Cmd+N` | Keep |
| Open link | `Cmd+Click` | `Enter` in link |
| Open in new pane | `Cmd+Alt+Enter` | Keep |
| Close current pane | `Cmd+W` | Keep |
| Toggle sidebar | None | `Cmd+\` |

### Editing

| Action | Default | Recommended |
|--------|---------|-------------|
| Toggle checklist | None | `Cmd+Enter` |
| Toggle bold | `Cmd+B` | Keep |
| Toggle italic | `Cmd+I` | Keep |
| Toggle code | `Cmd+`` ` | Keep |
| Insert link | `Cmd+K` | Keep |
| Toggle preview | `Cmd+E` | Keep |

---

## 🔄 Custom Hotkey Setup

### Access Hotkeys Settings

```
Settings → Hotkeys
```

### Vim-Inspired Bindings

Set these for a Vim-like experience:

```
Cmd+O → Quick switcher (already default, like :e)
Cmd+P → Command palette (like telescope)
Cmd+E → Toggle edit/preview (like :set wrap)
Cmd+/ → Toggle comments (if available)
Cmd+] → Increase indent
Cmd+[ → Decrease indent
```

### Pane Navigation

```
Cmd+\ → Toggle left sidebar
Cmd+Shift+\ → Toggle right sidebar
Ctrl+1 → Focus on pane 1
Ctrl+2 → Focus on pane 2
Ctrl+H/J/K/L → Move between panes (with plugin)
```

---

## 📝 Vim Mode Configuration

### Custom `.obsidian.vimrc`

Create `.obsidian.vimrc` in your vault root for custom Vim mappings:

```vim
" .obsidian.vimrc

" Use jk to exit insert mode
imap jk <Esc>

" Use H and L for start/end of line
nmap H ^
nmap L $

" Yank to end of line (consistent with D and C)
nmap Y y$

" Center screen after search
nmap n nzz
nmap N Nzz

" Quick save (triggers Obsidian save)
nmap <Space>w :w<CR>

" Navigate headings
exmap nextHeading jsfile .obsidian/scripts/nextHeading.js
exmap prevHeading jsfile .obsidian/scripts/prevHeading.js
nmap ]] :nextHeading<CR>
nmap [[ :prevHeading<CR>

" Follow link under cursor
exmap followLink obcommand editor:follow-link
nmap gd :followLink<CR>

" Go back (like Ctrl+O in Vim)
exmap goBack obcommand app:go-back
nmap <C-o> :goBack<CR>

" Go forward
exmap goForward obcommand app:go-forward
nmap <C-i> :goForward<CR>

" Toggle fold
exmap toggleFold obcommand editor:toggle-fold
nmap za :toggleFold<CR>

" Focus on file explorer
exmap focusExplorer obcommand file-explorer:reveal-active-file
nmap <Space>e :focusExplorer<CR>

" Quick switcher (like telescope)
exmap quickSwitcher obcommand switcher:open
nmap <Space>f :quickSwitcher<CR>

" Command palette
exmap commandPalette obcommand command-palette:open
nmap <Space>p :commandPalette<CR>

" Daily note
exmap dailyNote obcommand daily-notes:goto-today
nmap <Space>d :dailyNote<CR>
```

### Enable vimrc Support

1. Install **Vimrc Support** plugin
2. Create `.obsidian.vimrc` in vault root
3. Restart Obsidian

---

## 🔌 Recommended Plugins for Vim Users

### 1. Vimrc Support

Enables `.obsidian.vimrc` file for custom mappings.

### 2. Pane Relief

Adds commands for better pane navigation:
- Focus pane by direction
- Maximize current pane
- Swap panes

**Recommended bindings:**
```vim
exmap focusLeft obcommand pane-relief:focus-left
exmap focusRight obcommand pane-relief:focus-right
exmap focusUp obcommand pane-relief:focus-top
exmap focusDown obcommand pane-relief:focus-bottom

nmap <C-h> :focusLeft<CR>
nmap <C-l> :focusRight<CR>
nmap <C-k> :focusUp<CR>
nmap <C-j> :focusDown<CR>
```

### 3. Cycle Through Panes

Simple pane cycling with `Ctrl+Tab`.

### 4. Quick Switcher++

Enhanced quick switcher with:
- Recent files
- Headings within files
- Symbols

### 5. Another Quick Switcher

Even more powerful, with fuzzy finding and commands.

---

## 🎯 Workflow: Vim-Style Daily Routine

### Morning Startup

```
<Space>d     → Open daily note
<Space>f     → Quick switch to check tasks
]]           → Jump to next heading
```

### During Work

```
<Space>f     → Find any note quickly
gd           → Follow link under cursor
<C-o>        → Go back to previous note
<C-i>        → Go forward
/keyword     → Search in current note
```

### Note Taking

```
i            → Insert mode
jk           → Exit to normal mode
<Space>w     → Save
[[           → Auto-complete links (in insert mode)
```

### End of Day

```
<Space>d     → Return to daily note
gg           → Go to top
/##\sTasks   → Find Tasks section
o            → New line, insert mode
```

---

## ⚡ Speed Tips

### Quick Link Following

```vim
" In normal mode on a link, press gd to follow
nmap gd :followLink<CR>

" Or Enter in normal mode
nmap <CR> :followLink<CR>
```

### Heading Navigation

```vim
" Jump between headings
nmap ]] :nextHeading<CR>
nmap [[ :prevHeading<CR>
```

### Quick Note Creation

```vim
" Leader key workflows
nmap <Space>n :obcommand file-explorer:new-file<CR>
nmap <Space>N :obcommand file-explorer:new-folder<CR>
```

---

## 📋 Cheat Sheet: My Recommended Setup

### Leader Key Mappings (`<Space>` as leader)

| Key | Action |
|-----|--------|
| `<Space>f` | Find file (quick switcher) |
| `<Space>g` | Global search |
| `<Space>p` | Command palette |
| `<Space>e` | Reveal in explorer |
| `<Space>d` | Daily note |
| `<Space>w` | Save |
| `<Space>t` | Toggle todo |
| `<Space>/` | Search in file |

### Navigation

| Key | Action |
|-----|--------|
| `gd` | Follow link |
| `<C-o>` | Go back |
| `<C-i>` | Go forward |
| `]]` | Next heading |
| `[[` | Previous heading |
| `<C-h/j/k/l>` | Move between panes |

### Standard Vim

| Key | Action |
|-----|--------|
| `H` | Start of line |
| `L` | End of line |
| `jk` | Exit insert mode |
| `Y` | Yank to end of line |
| `n/N` | Search next/prev (centered) |

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Vim mode not working | Check Settings → Editor → Vim key bindings |
| vimrc not loading | Install Vimrc Support plugin, restart |
| Mapping conflicts | Check Hotkeys settings for conflicts |
| Some commands don't work | Use `obcommand` with exact command ID |
| Visual mode selection weird | Known limitation, use Shift+movement |

### Find Command IDs

```
Cmd+P → Type command → Look at the command ID in developer console
```

Or check `.obsidian/hotkeys.json` for existing mappings.

---

## Summary

For Vim users, Obsidian can feel almost native:

1. **Enable Vim mode** in settings
2. **Install Vimrc Support** plugin
3. **Create `.obsidian.vimrc`** with custom mappings
4. **Add pane navigation** plugins
5. **Build muscle memory** with leader key workflows

The goal: **Never touch the mouse** for daily operations.

---

## Next Steps
→ [[dataview-queries]] — Query notes like a database
→ [[templater-automation]] — Automate with JavaScript

