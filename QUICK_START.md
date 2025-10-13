# 🚀 Quick Start Guide

**Get your personal code archive into Git in 15 minutes!**

---

## ⚡ TL;DR

```bash
cd /Users/izaqyos/work/git/personal_code

# 1. Clean up (REQUIRED)
rm -rf code/python/sap/cfPortalLogin/  # Contains test credentials

# 2. Initialize Git
git init
git add .
git commit -m "Initial commit: Personal code archive"

# 3. Push to GitHub
git remote add origin git@github.com:YOUR_USERNAME/personal-code-archive.git
git branch -M main
git push -u origin main

# Done! ✅
```

---

## 📋 Pre-Flight Checklist

Before running the above commands:

### 1. Review Security Report
```bash
cat SECURITY_VALIDATION_REPORT.md
```

**Key Action Items**:
- [ ] ⚠️ Remove or sanitize `code/python/sap/cfPortalLogin/main.py`
- [ ] 🔍 Review SAP-related directories (if company work)
- [ ] ✅ Verify no personal emails in test files

### 2. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `personal-code-archive` (or your choice)
3. **Visibility: PRIVATE** ⚠️ Important!
4. Don't initialize with README (you already have one)
5. Click "Create repository"

### 3. Set up SSH Key (if not already done)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

---

## 🎯 Step-by-Step Guide

### Step 1: Clean Up (5 min)

```bash
cd /Users/izaqyos/work/git/personal_code

# Option A: Remove SAP content (if it was company work)
rm -rf code/python/sap/
rm -rf code/graphviz/sap/

# Option B: Just remove the file with credentials
rm -rf code/python/sap/cfPortalLogin/

# Verify .gitignore exists
cat .gitignore
```

### Step 2: Initialize Git (2 min)

```bash
# Initialize repository
git init

# Stage all files
git add .

# Review what will be committed
git status

# Check for accidentally included sensitive files
git status | grep -E "(\.env$|\.pem$|\.key$|credentials)"
# Should return nothing

# First commit
git commit -m "Initial commit: Personal code archive

- Code examples across multiple languages
- System design implementations
- Utility scripts and automation
- Learning projects and tutorials
- All sensitive data sanitized"
```

### Step 3: Connect to GitHub (3 min)

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/personal-code-archive.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Verify
git remote -v
```

### Step 4: Verify (5 min)

```bash
# Test clone in temp directory
cd /tmp
git clone git@github.com:YOUR_USERNAME/personal-code-archive.git test_clone
cd test_clone
ls -la

# If successful, clean up
cd /tmp
rm -rf test_clone

echo "✅ Success! Your code is backed up!"
```

---

## 🔄 Daily Usage

### Commit Changes
```bash
cd /Users/izaqyos/work/git/personal_code

# Add new/modified files
git add .

# Commit with message
git commit -m "Added new Python script for data analysis"

# Push to GitHub
git push origin main
```

### Pull Changes (from another computer)
```bash
cd ~/work/git/personal_code
git pull origin main
```

### Check Status
```bash
git status          # See what's changed
git log --oneline   # See recent commits
```

---

## 🆕 New Computer Setup

On a brand new laptop:

```bash
# 1. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install basic tools
brew install git

# 3. Set up Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 4. Set up SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add to GitHub

# 5. Clone your code
mkdir -p ~/work/git
cd ~/work/git
git clone git@github.com:YOUR_USERNAME/personal-code-archive.git personal_code

# 6. Run setup scripts
cd personal_code/new_computer
./firstTimeInstall.sh

# Done! You're ready to code on the new machine! ✅
```

---

## 🚨 Common Issues & Solutions

### Issue: "Permission denied (publickey)"
```bash
# Solution: Add SSH key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Test connection
ssh -T git@github.com
```

### Issue: "Repository too large"
```bash
# Solution: Use Git LFS for large files
brew install git-lfs
git lfs install
git lfs track "*.xlsx" "*.pdf" "*.zip"
git add .gitattributes
git commit -m "Add Git LFS"
git push origin main
```

### Issue: "Everything up-to-date" but changes exist
```bash
# Solution: Check if files are staged
git status
git add .
git commit -m "Commit unstaged changes"
git push origin main
```

---

## 📚 Next Steps

After successfully setting up Git:

1. **Set Up Secondary Backup** (Recommended)
   ```bash
   # See BACKUP_STRATEGY_RECOMMENDATIONS.md
   ```

2. **Automate Backups** (Optional)
   ```bash
   # Set up automated daily commits
   # See scripts/bash/auto_commit.sh
   ```

3. **Add GitLab Mirror** (Optional)
   ```bash
   # For extra redundancy
   git remote add gitlab git@gitlab.com:YOUR_USERNAME/personal-code-archive.git
   git push gitlab main
   ```

4. **Create Automated Backup Scripts**
   ```bash
   # Cloud backup
   # See scripts/bash/cloud_backup.sh
   
   # External drive backup
   # See scripts/bash/external_backup.sh
   ```

---

## 📖 Documentation Reference

- **SECURITY_VALIDATION_REPORT.md** - Security scan results
- **BACKUP_STRATEGY_RECOMMENDATIONS.md** - Comprehensive backup strategy
- **README.md** - Complete repository documentation
- **.gitignore** - Files excluded from Git

---

## ✅ Success Checklist

After completing this guide, you should have:

- [ ] ✅ Git repository initialized
- [ ] ✅ All files committed
- [ ] ✅ GitHub private repository created
- [ ] ✅ Code pushed to GitHub
- [ ] ✅ Tested clone from GitHub
- [ ] ✅ Sensitive data removed/sanitized
- [ ] ✅ .gitignore in place
- [ ] ✅ Documentation reviewed

---

## 🎉 Congratulations!

Your personal code archive is now safely backed up and accessible from anywhere!

**Time to complete**: 15-30 minutes  
**Cost**: $0 (GitHub free tier)  
**Result**: Years of work safely backed up ✅

---

## 🔗 Helpful Commands Cheat Sheet

```bash
# Daily workflow
git status                 # Check what's changed
git add .                  # Stage all changes
git commit -m "message"    # Commit changes
git push origin main       # Push to GitHub
git pull origin main       # Pull latest changes

# Information
git log --oneline          # See commit history
git remote -v              # See remote repositories
git branch                 # See branches

# Undo operations
git checkout -- file.txt   # Discard changes to file
git reset HEAD~1           # Undo last commit (keep changes)
git reflog                 # See all operations (for recovery)

# Maintenance
git gc                     # Cleanup and optimize
du -sh .git/              # Check repository size
```

---

**Need help?** Review the full documentation in `BACKUP_STRATEGY_RECOMMENDATIONS.md`

**Questions?** Open an issue in your GitHub repository to track them!

