# Utility Scripts Collection

A curated collection of useful scripts and utilities accumulated over years of software development, system administration, and automation work. These scripts cover various languages and use cases.

## 📁 Repository Structure

```
├── awk/          - AWK scripts for text processing and data extraction
├── bash/         - Bash scripts for system automation and utilities
├── perl/         - Perl scripts for various automation tasks
├── python/       - Python scripts and utilities
├── ruby/         - Ruby scripts
├── sed/          - SED scripts for text processing
├── sh/           - Shell scripts
└── util/         - General utility scripts
```

## 🔧 Categories

### Bash Scripts (`bash/`)
- **Security**: 
  - `secure-dir.sh` - Create encrypted APFS disk images from directories (macOS)
- **Backup & Sync**:
  - `manage_backups.sh` - Backup management utilities
  - `rsync-dirs.sh`, `rsync-diff.sh` - Rsync-based synchronization tools
  - `dir-diff.sh` - Directory comparison utilities
- **Development**:
  - `rust_cleaner.sh` - Clean Rust project artifacts
- And more...

### Python Scripts (`python/`)
- **Examples**: Python code examples and patterns
- **Learning**: Educational scripts covering Python concepts
- **Network**: Network-related utilities
- **Packaging**: Python packaging examples and tools
- **Tkinter**: GUI examples using Tkinter
- **Threading**: Multithreading examples and patterns
- **My Modules**: Custom Python modules including Gmail utilities

### Perl Scripts (`perl/`)
- **Common modules**: Reusable Perl modules (MyMail.pm, OsUtils.pm)
- **Learning examples**: Perl programming examples
- **Mail utilities**: Email-related scripts
- **Shell utilities**: Shell interaction scripts
- **General utilities**: Various Perl utilities

### AWK Scripts (`awk/`)
- Text processing and data extraction utilities

### SED Scripts (`sed/`)
- Text manipulation and transformation scripts
- `tocify.bash` - Table of contents generator
- Various text processing utilities

### Utilities (`util/`)
- Cross-platform utilities
- File system tools
- Development helpers

## 🚀 Usage

Each script typically includes:
- Usage instructions in comments or via `--help` flag
- Examples of common use cases
- Required dependencies

Example:
```bash
# For most bash scripts:
./script_name.sh --help

# For Python scripts:
python3 script_name.py --help
```

## 📋 Prerequisites

Different scripts have different requirements. Common dependencies include:

- **Bash scripts**: Bash 4.0+, standard Unix utilities
- **Python scripts**: Python 3.6+, various packages (check individual scripts)
- **Perl scripts**: Perl 5.x
- **Ruby scripts**: Ruby 2.x+

## ⚠️ Important Notes

1. **Review before use**: Always review scripts before running them, especially those that modify system state
2. **Test in safe environment**: Test scripts in development/staging environments first
3. **Backup important data**: Always backup before running destructive operations
4. **Path adjustments**: Some scripts may require path adjustments for your environment
5. **Platform compatibility**: Some scripts are platform-specific (macOS, Linux, etc.)

## 🔐 Security

These scripts have been sanitized for public release:
- No passwords or API keys
- No internal company URLs or sensitive information
- Example domains used where applicable

## 📝 License

This collection is provided as-is for educational and utility purposes. Feel free to use, modify, and adapt these scripts for your own needs.

## 🤝 Contributing

While this is a personal collection, suggestions and improvements are welcome. Please open an issue or pull request if you find bugs or have enhancements.

## ⭐ Highlights

Some particularly useful scripts:

- **`bash/secure-dir.sh`**: Create encrypted, password-protected disk images on macOS
- **`bash/manage_backups.sh`**: Automated backup management
- **`bash/dir-diff.sh`**: Advanced directory comparison
- **`python/my_modules/`**: Reusable Python modules
- **`perl/common/`**: Reusable Perl modules for common tasks

## 📚 Documentation

Individual scripts contain inline documentation. For complex scripts, check the header comments for:
- Purpose and description
- Usage examples
- Parameters and options
- Dependencies
- Author notes

---

**Note**: This repository represents years of accumulated scripting knowledge. Some scripts may be dated but are kept for historical reference and potential reuse of techniques.

