# Custom CSS Snippets

> Style your vault your way — from subtle tweaks to complete visual overhauls.

---

## 🎨 What Are CSS Snippets?

CSS snippets are small stylesheet files that override Obsidian's default styling. They're:
- **Modular** — Enable/disable individually
- **Theme-independent** — Work with any theme
- **Version-safe** — Won't break on Obsidian updates
- **Shareable** — Just text files

**Developer analogy:** Like browser userscripts, but for your notes app.

---

## 🚀 Getting Started

### Enable Snippets

1. **Open snippets folder:**
   ```
   Settings → Appearance → CSS snippets → 📁 (folder icon)
   ```
   This opens `.obsidian/snippets/`

2. **Create a `.css` file:**
   ```bash
   touch my-tweaks.css
   ```

3. **Enable the snippet:**
   ```
   Settings → Appearance → CSS snippets → Toggle on your snippet
   ```

4. **Reload to see changes:**
   - `Cmd+R` (or `Ctrl+R` on Windows/Linux)
   - Or toggle the snippet off and on

---

## 🔍 Finding CSS Selectors

### Method 1: Developer Tools

```
Cmd+Option+I (Mac) / Ctrl+Shift+I (Windows/Linux)
```

This opens Obsidian's DevTools — inspect elements just like in a browser.

### Method 2: Community Resources

- [Obsidian CSS Snippets Collection](https://github.com/Dmitriy-Shulha/obsidian-css-snippets)
- [Obsidian Forum — CSS Snippets](https://forum.obsidian.md/c/share-showcase/9)
- [r/ObsidianMD CSS posts](https://reddit.com/r/ObsidianMD)

### Method 3: Theme Source Code

Look at popular themes on GitHub for selector examples:
- Minimal Theme
- Things Theme
- California Coast

---

## 📝 Essential Snippets

### 1. Readable Line Width

```css
/* readable-width.css */
/* Adjust the max width of your notes */

.markdown-source-view.mod-cm6 .cm-content,
.markdown-preview-view {
    max-width: 800px !important;
    margin: 0 auto;
}
```

### 2. Custom Heading Styles

```css
/* custom-headings.css */

/* H1 — Large with underline */
.markdown-preview-view h1,
.cm-header-1 {
    font-size: 2em;
    border-bottom: 2px solid var(--interactive-accent);
    padding-bottom: 0.3em;
}

/* H2 — Colored accent */
.markdown-preview-view h2,
.cm-header-2 {
    color: var(--interactive-accent);
    font-size: 1.6em;
}

/* H3 — Smaller, bold */
.markdown-preview-view h3,
.cm-header-3 {
    font-size: 1.3em;
    font-weight: 700;
}
```

### 3. Checkbox Styling

```css
/* fancy-checkboxes.css */

/* Completed tasks — strikethrough and dim */
.markdown-preview-view li.task-list-item.is-checked {
    text-decoration: line-through;
    color: var(--text-muted);
}

/* Custom checkbox colors */
input[type="checkbox"]:checked {
    background-color: var(--interactive-accent);
    border-color: var(--interactive-accent);
}
```

### 4. Tag Pills

```css
/* tag-pills.css */

.tag {
    background-color: var(--interactive-accent);
    color: var(--text-on-accent);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.85em;
}
```

### 5. Blockquote Styling

```css
/* blockquote-callout.css */

.markdown-preview-view blockquote {
    border-left: 4px solid var(--interactive-accent);
    background: var(--background-secondary);
    padding: 1em;
    margin: 1em 0;
    border-radius: 0 8px 8px 0;
}
```

### 6. Code Block Enhancements

```css
/* code-blocks.css */

/* Inline code */
.cm-inline-code,
code {
    background: var(--background-secondary);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Code blocks */
.markdown-preview-view pre {
    background: var(--background-secondary);
    border-radius: 8px;
    padding: 1em;
    overflow-x: auto;
}

/* Line numbers in code blocks */
.markdown-preview-view pre code {
    counter-reset: line;
}
```

### 7. Image Centering

```css
/* center-images.css */

.markdown-preview-view img {
    display: block;
    margin: 1em auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

---

## 🎯 Developer-Focused Snippets

### Terminal-Style Code Blocks

```css
/* terminal-code.css */

.markdown-preview-view pre {
    background: #1e1e1e;
    color: #d4d4d4;
    border-radius: 8px;
    padding: 1em;
    font-family: 'JetBrains Mono', monospace;
    position: relative;
}

/* Add "terminal" dots */
.markdown-preview-view pre::before {
    content: "● ● ●";
    color: #ff5f56;
    position: absolute;
    top: 8px;
    left: 12px;
    font-size: 10px;
    letter-spacing: 4px;
}
```

### Vim Mode Indicator

```css
/* vim-mode-indicator.css */

/* Show current Vim mode in status bar */
.cm-vim-mode-normal .status-bar::after {
    content: " -- NORMAL --";
    color: var(--text-accent);
}

.cm-vim-mode-insert .status-bar::after {
    content: " -- INSERT --";
    color: #98c379;
}

.cm-vim-mode-visual .status-bar::after {
    content: " -- VISUAL --";
    color: #e5c07b;
}
```

### ADR Status Badges

```css
/* adr-status.css */

/* Style YAML status field display */
.frontmatter-container .mod-status-accepted {
    color: #98c379;
}

.frontmatter-container .mod-status-deprecated {
    color: #e06c75;
}

.frontmatter-container .mod-status-proposed {
    color: #e5c07b;
}
```

---

## 🗂️ Organizing Your Snippets

### Recommended Structure

```
.obsidian/snippets/
├── 00-variables.css      # Custom CSS variables
├── 01-typography.css     # Fonts, headings, line height
├── 02-colors.css         # Color overrides
├── 03-layout.css         # Width, margins, spacing
├── 04-components.css     # Tags, checkboxes, callouts
├── 05-code.css          # Code block styling
└── 99-experimental.css   # Testing new styles
```

### Custom Variables

Create a variables file that other snippets can use:

```css
/* 00-variables.css */

body {
    --my-accent: #7c3aed;
    --my-success: #10b981;
    --my-warning: #f59e0b;
    --my-error: #ef4444;
    --my-radius: 8px;
    --my-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

Then use in other snippets:

```css
/* 04-components.css */

.tag {
    background: var(--my-accent);
    border-radius: var(--my-radius);
}
```

---

## ⚡ CSS Variables Reference

### Built-in Variables

```css
/* Colors */
--background-primary       /* Main background */
--background-secondary     /* Sidebar, panels */
--text-normal             /* Body text */
--text-muted              /* Dimmed text */
--text-accent             /* Links, highlights */
--interactive-accent      /* Active elements */

/* Typography */
--font-text               /* Body font */
--font-monospace          /* Code font */
--font-ui                 /* Interface font */

/* Sizing */
--line-width              /* Note max width */
--file-line-width         /* File explorer width */
```

### Override Variables

```css
/* custom-variables.css */

body {
    --interactive-accent: #7c3aed;
    --font-monospace: 'JetBrains Mono', monospace;
    --line-width: 750px;
}

.theme-dark {
    --background-primary: #0d1117;
    --background-secondary: #161b22;
}

.theme-light {
    --background-primary: #ffffff;
    --background-secondary: #f6f8fa;
}
```

---

## 🔧 Debugging CSS

### Common Issues

| Problem | Solution |
|---------|----------|
| Snippet not applying | Check file extension is `.css`, toggle off/on |
| Overridden by theme | Add `!important` to your rule |
| Works in preview but not edit | Need different selectors for Live Preview |
| Breaks after update | Check Obsidian changelog for CSS changes |

### Debug Mode

Add a debug snippet to visualize layout:

```css
/* debug.css */

* {
    outline: 1px solid rgba(255, 0, 0, 0.2);
}
```

---

## 📦 Popular Snippet Collections

| Resource | Description |
|----------|-------------|
| [Obsidian Snippets](https://github.com/Dmitriy-Shulha/obsidian-css-snippets) | Curated collection |
| [ITS Theme Snippets](https://github.com/SlRvb/Obsidian--ITS-Theme) | Companion snippets |
| [Obsidian Forum](https://forum.obsidian.md/tag/css-snippets) | Community shared |

---

## Summary

CSS snippets let you:
- 🎨 **Customize appearance** without breaking updates
- 📦 **Modular styling** — toggle individual tweaks
- 🔧 **Fine-tune** any visual element
- 🤝 **Share** your customizations easily

**Start simple:**
1. Pick one thing that bothers you visually
2. Find or write a snippet for it
3. Test and refine
4. Gradually build your collection

---

## Next Steps
→ [[hotkeys-vim-navigation]] — Keyboard-driven efficiency
→ [[dataview-queries]] — Query your notes like a database

