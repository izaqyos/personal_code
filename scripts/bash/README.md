# Bash Scripts Collection

[![GitHub Repository](https://img.shields.io/badge/GitHub-bash__scripts-blue?logo=github)](https://github.com/izaqyos/bash_scripts)
[![Shell](https://img.shields.io/badge/Shell-100%25-89e051)](https://github.com/izaqyos/bash_scripts)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/izaqyos/bash_scripts/blob/main/LICENSE)

This repository contains a collection of bash scripts for various system administration, development, and utility tasks. Each script is designed to be self-contained and well-documented.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/izaqyos/bash_scripts.git
cd bash_scripts

# Make scripts executable
chmod +x *.sh

# Example: Clean Rust projects
./rust_cleaner.sh ~/rust-projects

# Example: Compare directories
./dir-diff.sh /path/to/source /path/to/destination
```

## Table of Contents

- [System Utilities](#system-utilities)
- [Directory & File Management](#directory--file-management)
- [Security & Encryption](#security--encryption)
- [Development Tools](#development-tools)
- [Backup & Sync](#backup--sync)
- [Testing Scripts](#testing-scripts)

---

## System Utilities

### `banner.sh`
**Purpose**: Creates ASCII art text banners from input strings using a custom bitmap font.

**Usage**:
```bash
./banner.sh "Hello World"
./banner.sh "2023" "STATUS" "OK"
```

**Features**:
- Supports alphanumeric characters, symbols, and punctuation
- Custom bitmap font rendering
- Multiple arguments create separate banners
- Terminal-width output formatting

---

### `load_nvm.sh`
**Purpose**: Manually loads NVM (Node Version Manager) into the current shell session.

**Usage**:
```bash
source ./load_nvm.sh
# or
. ./load_nvm.sh
```

**Features**:
- Loads NVM with bash completion
- Shows current Node.js version after loading
- Optional auto-switch to LTS version (commented out)

---

### `timeout3.sh`
**Purpose**: Shell script with timeout functionality (implementation details in script).

**Usage**:
```bash
./timeout3.sh [options]
```

---

### `traptest.sh` & `trap_ctrl_c`
**Purpose**: Demonstration scripts for signal handling and cleanup operations.

**Usage**:
```bash
./traptest.sh
```

---

## Directory & File Management

### `dir-diff.sh`
**Purpose**: Compares two directories using `diff -r --brief` and reports differences with color-coded output.

**Usage**:
```bash
./dir-diff.sh /path/to/source /path/to/destination
```

**Features**:
- Color-coded output (green/red/blue/yellow)
- Identifies files only in source `[+]`
- Identifies files only in destination `[-]`
- Identifies differing files `[~]`
- Handles type mismatches (file vs directory vs symlink)

**Example**:
```bash
./dir-diff.sh ~/project/src ~/backup/src
```

---

### `rsync-diff.sh`
**Purpose**: Compares two directories using `rsync` dry-run and reports differences with detailed change codes.

**Usage**:
```bash
./rsync-diff.sh /path/to/source /path/to/destination
```

**Features**:
- Uses rsync's itemized change output for detailed comparison
- Shows content differences, permission changes, size differences
- More comprehensive than `dir-diff.sh` for attribute comparison
- Color-coded output with rsync change codes

**Example**:
```bash
./rsync-diff.sh ~/documents ~/backup/documents
```

---

### `rsync-dirs.sh`
**Purpose**: Synchronizes destination directory to match source directory using rsync, with optional interactive mode.

**Usage**:
```bash
# Non-interactive sync (with confirmation)
./rsync-dirs.sh /path/to/source /path/to/destination

# Interactive mode (prompts before each deletion)
./rsync-dirs.sh -i /path/to/source /path/to/destination
```

**Features**:
- **Direction**: Always source → destination
- **Safety**: Confirmation prompts before sync
- **Interactive mode**: Prompts before each file deletion
- **Comprehensive sync**: Uses `rsync -avc --delete`
- **Color-coded status messages**

**⚠️ Warning**: Files in destination not present in source will be **deleted**.

---

## Security & Encryption

### `secure-dir.sh`
**Purpose**: Creates an encrypted APFS sparse bundle from an existing directory with optional verification and source deletion.

**Usage**:
```bash
./secure-dir.sh --source ~/sensitive-data --size 50 --output ~/SecureData.sparsebundle
./secure-dir.sh --source ~/docs --size 100 --output ~/Encrypted.sparsebundle --verify-script ./dir-diff.sh
```

**Parameters**:
- `--source <path>`: Source directory to encrypt
- `--size <GB>`: Maximum size in gigabytes
- `--output <path>`: Output `.sparsebundle` path
- `--verify-script <path>`: Optional verification script

**Features**:
- **AES-256 encryption**
- **APFS sparse bundle format**
- **Password confirmation**
- **Optional content verification**
- **Safe source deletion** (after confirmation)
- **Comprehensive error handling**

---

### `create-empty-vault.sh`
**Purpose**: Creates a new, empty, encrypted APFS sparse disk image for secure file storage.

**Usage**:
```bash
./create-empty-vault.sh --size 50 --output ~/MyVault.sparseimage
```

**Parameters**:
- `--size <GB>`: Maximum size in gigabytes
- `--output <path>`: Output `.sparseimage` path

**Features**:
- **AES-256 encryption**
- **Sparse format** (only uses space as needed)
- **Password-protected**
- **APFS filesystem**

**After Creation**:
```bash
# Mount the vault
hdiutil attach ~/MyVault.sparseimage

# Access via Finder or command line
ls /Volumes/MyVault

# Unmount
hdiutil detach /Volumes/MyVault
```

---

### PKI Certificate Generation Scripts

#### `pki_generator.sh`
**Purpose**: Comprehensive PKI certificate generation tool for stress testing and development.

**Usage**:
```bash
./pki_generator.sh -Cm CA -Noc 1000 -Norc 5 -up user -mp machine -dp cisco.com \
  -CAexp 365 -policyCaexp 365 -issuingCaexp 365 -SERexp 365 -CLTexp 365 \
  -hash sha256 -keysz 2048 -RndSn
```

**Key Parameters**:
- `-Cm, --CA_mode`: CA mode (noCA, CA, subCA)
- `-Noc, --number_of_certificates`: Number of certificates to generate
- `-Norc, --number_of_revoked_certificates`: Number of revoked certificates
- `-up, --username_pattern`: Username pattern for user certificates
- `-mp, --machinename_pattern`: Machine name pattern
- `-dp, --domainname_pattern`: Domain pattern
- `-hash, --hash_type`: Hash algorithm (sha256, sha384, sha512, sha1, md5)
- `-keysz, --key_size`: Key size (512, 1024, 2048, 4096, 8192)

**Variants**:
- `pki_generator_new.sh`: Updated version with new features
- `pki_generator_mult_val_RDN.sh`: Multiple value RDN support
- `pki_generator_subj_SSN.sh`: Subject serial number support

---

### Key Management Scripts

#### `zeorize_keys.bash` / `zeorize_keys_machine.bash`
**Purpose**: Secure key deletion and management utilities.

**Usage**:
```bash
./zeorize_keys.bash
./zeorize_keys_machine.bash
```

---

## Development Tools

### `rust_cleaner.sh`
**Purpose**: Recursively scans for Rust Cargo projects and runs `cargo clean` to free up disk space.

**Usage**:
```bash
./rust_cleaner.sh /path/to/development/directory
./rust_cleaner.sh ~/rust-projects
```

**Features**:
- **Recursive project detection**: Finds all `Cargo.toml` files
- **Workspace-aware**: Skips workspace members (cleaned with workspace)
- **Comprehensive reporting**: Shows cleaned, failed, and total projects
- **Error handling**: Continues on individual failures
- **Color-coded output**

**Example Output**:
```
🔍 Starting scan for Rust Cargo projects in: /home/user/rust-projects

[INFO] Cleaning Cargo project: my-app (/home/user/rust-projects/my-app)
[SUCCESS] Successfully cleaned: my-app

📊 Total Cargo projects found: 5
✅ Successfully cleaned: 4
❌ Failed to clean: 1
```

---

### `search_git_repos.sh`
**Purpose**: Searches for patterns across multiple Git repositories with context and highlighting.

**Usage**:
```bash
./search_git_repos.sh "pattern_to_search"
./search_git_repos.sh "TODO" -c 3  # With 3 lines of context
```

**Features**:
- **Multi-repository search**: Searches across predefined repository list
- **Context lines**: Optional before/after context
- **Syntax highlighting**: Bold red highlighting of matches
- **Git repository validation**: Ensures directories are valid Git repos
- **Progress indication**: Shows which repositories are being processed

**Repository Configuration**: Edit the `repo_data` array in the script to add your repositories.

---

## Backup & Sync

### `manage_backups.sh`
**Purpose**: Manages backup files across multiple locations with listing and deletion capabilities.

**Usage**:
```bash
# List 10 newest backups from each location
./manage_backups.sh list

# List 20 newest backups from each location
./manage_backups.sh list 20

# Delete 5 oldest backups from each location (with confirmation)
./manage_backups.sh delete 5
```

**Features**:
- **Multiple backup locations**: Configurable backup directory array
- **Date-based sorting**: Parses dates from filenames (format: `_DD_MM_YY.tar.bz2`)
- **Safe deletion**: Interactive confirmation before deletion
- **Location-specific operations**: Operates on each backup location independently

**Configuration**: Edit the `BACKUP_DIRS` array to specify your backup locations:
```bash
BACKUP_DIRS=(
    "$HOME/backups"
    "$HOME/Library/Mobile Documents/com~apple~CloudDocs"
    "$HOME/Library/CloudStorage/OneDrive-SAPSE"
)
```

---

## Testing Scripts

### `rust_cleaner_tests.sh`
**Purpose**: Comprehensive test suite for `rust_cleaner.sh` with 100% test coverage.

**Usage**:
```bash
./rust_cleaner_tests.sh
```

**Test Categories**:
- **Input validation**: Missing arguments, invalid directories
- **Cargo availability**: Command existence checks
- **Project detection**: Valid/invalid Cargo projects, nested structures
- **Workspace handling**: Workspace member detection and skipping
- **Cleaning functionality**: Success and failure scenarios
- **Edge cases**: Relative paths, spaces, symlinks, deep directories
- **Output validation**: Report format and content verification
- **Concurrent execution**: Multi-instance safety
- **Performance testing**: Large project sets

---

### `dir-diff-test.sh` / `rsync-diff-test.sh` / `rsync-dirs-test.sh`
**Purpose**: Test suites for the respective directory comparison and synchronization scripts.

**Usage**:
```bash
./dir-diff-test.sh
./rsync-diff-test.sh
./rsync-dirs-test.sh
```

---

## Installation & Setup

1. **Clone or download** the scripts to your desired directory
2. **Make scripts executable**:
   ```bash
   chmod +x *.sh
   ```
3. **Install dependencies** as needed:
   - For NVM scripts: Install [NVM](https://github.com/nvm-sh/nvm)
   - For Rust scripts: Install [Rust/Cargo](https://rustup.rs/)
   - For Git scripts: Ensure Git is installed
   - For macOS encryption scripts: macOS with `hdiutil` (built-in)

## Configuration

Several scripts require configuration:

- **`search_git_repos.sh`**: Edit `repo_data` array with your repository paths
- **`manage_backups.sh`**: Edit `BACKUP_DIRS` array with your backup locations
- **PKI scripts**: Adjust certificate parameters as needed

## Best Practices

1. **Test first**: Use test scripts or dry-run modes where available
2. **Backup important data** before running destructive operations
3. **Review script contents** before execution, especially for security-related scripts
4. **Use absolute paths** when possible to avoid confusion
5. **Check dependencies** before running scripts

## Security Considerations

- **Encryption scripts**: Use strong, memorable passwords
- **Key management scripts**: Understand the implications of key deletion
- **Directory sync scripts**: Be careful with deletion operations
- **PKI scripts**: Generated certificates are for testing purposes only

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### How to Contribute:
1. Fork the repository: https://github.com/izaqyos/bash_scripts
2. Create a feature branch: `git checkout -b feature/new-script`
3. Add your script following the guidelines below
4. Test thoroughly using the provided test frameworks
5. Submit a pull request

### Script Guidelines:
1. Include comprehensive documentation at the top
2. Add usage examples in the README
3. Implement proper error handling
4. Use consistent color coding and output formatting
5. Create corresponding test scripts where applicable
6. Follow the existing code style and structure

---

## Script Summary Table

| Script | Purpose | Input | Output | Safety Level |
|--------|---------|-------|--------|--------------|
| `banner.sh` | ASCII art text | Text strings | Terminal output | ✅ Safe |
| `dir-diff.sh` | Directory comparison | Two directories | Difference report | ✅ Safe |
| `rsync-diff.sh` | Advanced dir comparison | Two directories | Detailed differences | ✅ Safe |
| `rsync-dirs.sh` | Directory synchronization | Source/dest dirs | Synchronized destination | ⚠️ Destructive |
| `secure-dir.sh` | Create encrypted volume | Directory + params | Encrypted image | ⚠️ Destructive |
| `create-empty-vault.sh` | Create empty vault | Size + output path | Empty encrypted image | ✅ Safe |
| `rust_cleaner.sh` | Clean Rust projects | Directory path | Disk space freed | ✅ Safe |
| `search_git_repos.sh` | Multi-repo search | Search pattern | Match results | ✅ Safe |
| `manage_backups.sh` | Backup management | Action + count | Listed/deleted backups | ⚠️ Destructive |
| `load_nvm.sh` | Load NVM | None | NVM environment | ✅ Safe |
| `pki_generator.sh` | Generate certificates | PKI parameters | Certificate files | ✅ Safe |

**Legend**:
- ✅ **Safe**: Read-only or non-destructive operations
- ⚠️ **Destructive**: Can modify or delete files (with safeguards)

---

## Repository Information

- **GitHub**: https://github.com/izaqyos/bash_scripts
- **License**: MIT (see LICENSE file)
- **Author**: izaqyos
- **Language**: 100% Shell/Bash

### Links
- [View on GitHub](https://github.com/izaqyos/bash_scripts)
- [Report Issues](https://github.com/izaqyos/bash_scripts/issues)
- [Submit Pull Requests](https://github.com/izaqyos/bash_scripts/pulls)

---

*Last updated: 2025-01-01*
