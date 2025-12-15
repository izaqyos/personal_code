# Publishing & Sharing Options

> Take your notes public — from quick shares to full-blown digital gardens.

---

## 🌐 Why Publish?

| Goal | Solution |
|------|----------|
| **Share knowledge** | Blog, digital garden |
| **Build in public** | Learning notes, TILs |
| **Team documentation** | Internal wiki |
| **Portfolio** | Professional presence |
| **Quick share** | Send single note to someone |

---

## 📊 Publishing Options Overview

| Method | Cost | Effort | Best For |
|--------|------|--------|----------|
| Obsidian Publish | $10/mo | Low | Beautiful, integrated |
| Quartz | Free | Medium | Developers, full control |
| MkDocs | Free | Medium | Documentation sites |
| Hugo + Obsidian | Free | High | Custom blogs |
| Notion Export | Free | Low | Quick shares |
| GitHub Pages | Free | Medium | Tech-savvy users |

---

## 🏆 Option 1: Obsidian Publish

### What You Get

- One-click publishing from Obsidian
- Beautiful default themes
- Graph view on web
- Search functionality
- Custom domain support
- Password protection

### Setup

1. **Subscribe:** Settings → Publish → Start trial or Subscribe
2. **Select files:** Choose which notes to publish
3. **Configure:** Set site name, custom domain, theme
4. **Publish:** Click "Publish changes"

### Pricing

- $10/month (or $8/month annual)
- Includes custom domain, themes, password protection

### Best For

- Non-technical users
- Quick setup needed
- Integration matters (links, graph, backlinks work)

---

## 🔧 Option 2: Quartz (Free, Static Site)

### What It Is

Open-source static site generator designed for Obsidian vaults.

### Features

- Full-text search
- Graph view
- Backlinks
- Tag pages
- Dark/light mode
- Free hosting (GitHub Pages, Netlify, Vercel)

### Setup

```bash
# Clone Quartz
git clone https://github.com/jackyzha0/quartz.git
cd quartz

# Install dependencies
npm install

# Copy your vault content
cp -r ~/vaults/public/content/* content/

# Build and preview
npx quartz build --serve
```

### Configuration

Edit `quartz.config.ts`:

```typescript
const config: QuartzConfig = {
  configuration: {
    pageTitle: "My Digital Garden",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    baseUrl: "yoursite.github.io/quartz",
    ignorePatterns: ["private", "templates"],
    theme: {
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "JetBrains Mono"
      },
      colors: {
        lightMode: { /* ... */ },
        darkMode: { /* ... */ }
      }
    }
  }
};
```

### Deploy to GitHub Pages

```bash
# In quartz directory
npx quartz sync --no-pull

# Or configure GitHub Actions for automatic deploy
```

### Best For

- Developers who want full control
- Free hosting needs
- Digital garden aesthetic

---

## 📚 Option 3: MkDocs

### What It Is

Documentation site generator that works great with markdown.

### Setup

```bash
# Install
pip install mkdocs mkdocs-material

# Create project
mkdocs new my-docs
cd my-docs

# Copy your notes
cp -r ~/vaults/docs/* docs/

# Preview
mkdocs serve
```

### Configuration

`mkdocs.yml`:

```yaml
site_name: My Knowledge Base
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - content.code.copy

nav:
  - Home: index.md
  - Guides:
    - Getting Started: guides/start.md
    - Advanced: guides/advanced.md
  - Reference:
    - API: reference/api.md

plugins:
  - search
  - tags

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - toc:
      permalink: true
```

### Deploy

```bash
mkdocs gh-deploy  # Deploy to GitHub Pages
```

### Best For

- Technical documentation
- Structured navigation
- Team wikis

---

## 🚀 Option 4: Hugo + Obsidian

### What It Is

Hugo is a fast static site generator. Combined with obsidian-to-hugo scripts, you can publish your vault.

### Setup

```bash
# Install Hugo
brew install hugo

# Create site
hugo new site my-blog
cd my-blog

# Add theme
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

### Obsidian to Hugo Script

```python
#!/usr/bin/env python3
# convert_obsidian_to_hugo.py

import re
import os
from pathlib import Path

def convert_wikilinks(content):
    """Convert [[wikilinks]] to [text](url) format"""
    pattern = r'\[\[([^\]|]+)\|?([^\]]*)\]\]'
    
    def replace(match):
        target = match.group(1)
        alias = match.group(2) or target
        slug = target.lower().replace(' ', '-')
        return f'[{alias}](/posts/{slug})'
    
    return re.sub(pattern, replace, content)

def process_vault(vault_path, hugo_content_path):
    vault = Path(vault_path)
    hugo = Path(hugo_content_path)
    
    for md_file in vault.glob('**/*.md'):
        content = md_file.read_text()
        converted = convert_wikilinks(content)
        
        # Add Hugo frontmatter if missing
        if not converted.startswith('---'):
            title = md_file.stem
            converted = f"""---
title: "{title}"
date: {md_file.stat().st_mtime}
draft: false
---

{converted}"""
        
        dest = hugo / 'posts' / md_file.name
        dest.write_text(converted)

if __name__ == '__main__':
    process_vault('~/vaults/public', '~/my-blog/content')
```

### Best For

- Existing Hugo users
- Custom blog layouts
- Maximum flexibility

---

## 📤 Option 5: Quick Sharing

### Share Single Notes

**Method 1: Export to PDF**
```
Cmd+P → Export to PDF
```

**Method 2: Copy as HTML**
```
Cmd+P → Copy as HTML
```
Paste into email or other app.

**Method 3: Notion-style sharing**

Use **Share Note** plugin:
```
Settings → Community plugins → Share Note → Install
Right-click note → Share → Get public link
```

### GitHub Gist

```bash
# Share a note as gist
gh gist create ~/vaults/public/notes/my-note.md --public
```

---

## 🔐 Access Control

### Obsidian Publish

- **Public** — Anyone can view
- **Password protected** — Require password
- **Unlisted** — Not indexed, but accessible via URL

### Self-Hosted Options

| Method | Description |
|--------|-------------|
| Netlify password | Built-in password protection |
| Cloudflare Access | SSO/identity-based access |
| Basic Auth | nginx/Apache password |
| Private repo | GitHub private + Pages |

### Selective Publishing

```
vault/
├── public/          # → Publish
│   ├── blog/
│   └── tutorials/
├── private/         # → Don't publish
│   ├── journal/
│   └── personal/
└── drafts/          # → Publish when ready
```

Use `.gitignore` or publish config to exclude private folders.

---

## 🎨 Customization

### Obsidian Publish

```
Settings → Publish → Site settings
- Custom CSS
- Custom domain
- Navigation order
- Favicon
```

### Quartz/Hugo/MkDocs

Full CSS/HTML control — edit theme files directly.

### Common Customizations

| Feature | How |
|---------|-----|
| Custom domain | DNS CNAME record |
| Analytics | Google Analytics, Plausible |
| Comments | Giscus (GitHub), Disqus |
| Newsletter | Buttondown, Substack |
| Search | Built-in or Algolia |

---

## 📝 Content Strategy

### What to Publish

| Type | Description |
|------|-------------|
| **Evergreen** | Timeless reference content |
| **TIL** | Today I Learned snippets |
| **Tutorials** | Step-by-step guides |
| **MOCs** | Curated topic indexes |
| **Book notes** | Summaries and takeaways |

### What NOT to Publish

- Personal journal entries
- 1:1 meeting notes
- Private project details
- Incomplete drafts (unless labeled)
- Copyrighted content

### Publishing Workflow

```
1. Write in private vault
2. Polish and review
3. Move to public folder
4. Add frontmatter/metadata
5. Build and preview
6. Deploy
```

---

## 🔄 Automation

### GitHub Actions for Quartz

`.github/workflows/deploy.yml`:

```yaml
name: Deploy Quartz

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Build
        run: |
          npm install
          npx quartz build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### Obsidian Git + Build Hook

```bash
#!/bin/bash
# post-commit hook

# Trigger Netlify/Vercel build
curl -X POST $DEPLOY_HOOK_URL
```

---

## 📊 Comparison Summary

| Feature | Obsidian Publish | Quartz | MkDocs |
|---------|-----------------|--------|--------|
| **Cost** | $10/mo | Free | Free |
| **Setup** | 1-click | Medium | Medium |
| **Customization** | Limited | Full | Full |
| **Graph view** | ✅ | ✅ | ❌ |
| **Backlinks** | ✅ | ✅ | Plugin |
| **Search** | ✅ | ✅ | ✅ |
| **Comments** | ❌ | Add-on | Add-on |
| **Best for** | Simplicity | Digital garden | Docs |

---

## 🎯 My Recommendation

### For Developers

```
Quartz + GitHub Pages
- Free
- Full control
- Git-based workflow
- Great for digital gardens
```

### For Non-Developers

```
Obsidian Publish
- Simple setup
- Integrated with Obsidian
- Beautiful defaults
- $10/month
```

### For Documentation

```
MkDocs Material
- Professional appearance
- Great navigation
- Code highlighting
- Search built-in
```

---

## Summary

Publishing options by use case:

| Use Case | Recommendation |
|----------|----------------|
| Personal blog | Quartz, Hugo |
| Digital garden | Quartz, Obsidian Publish |
| Team docs | MkDocs, GitBook |
| Quick share | Share Note plugin, PDF export |
| Maximum control | Hugo + custom theme |
| Minimal effort | Obsidian Publish |

**Start simple:** Use Obsidian Publish trial or Share Note plugin. Migrate to self-hosted later if needed.

---

## Related
→ [[git-integration]] — Version control for your published content
→ [[multi-vault-strategies]] — Separate public and private vaults

