"""
Week 9, Day 4: Path Manipulation with pathlib

Learning Objectives:
- Master pathlib.Path
- Learn path operations
- Practice file system navigation
- Handle cross-platform paths
- Build file utilities

Time: 10-15 minutes
"""

from pathlib import Path
import tempfile
import shutil
from datetime import datetime

# ============================================================
# EXERCISE 1: Path Basics
# ============================================================

def path_basics():
    """
    Learn Path object basics.
    
    pathlib: Object-oriented file paths
    """
    print("--- Exercise 1: Path Basics ---")
    
    # Create Path objects
    p = Path('/usr/local/bin')
    print(f"Path: {p}")
    print(f"Type: {type(p)}")
    
    # Current directory
    cwd = Path.cwd()
    print(f"\nCurrent directory: {cwd}")
    
    # Home directory
    home = Path.home()
    print(f"Home directory: {home}")
    
    # Path components
    p2 = Path('/home/user/documents/file.txt')
    print(f"\nPath: {p2}")
    print(f"  Parts: {p2.parts}")
    print(f"  Parent: {p2.parent}")
    print(f"  Name: {p2.name}")
    print(f"  Stem: {p2.stem}")
    print(f"  Suffix: {p2.suffix}")
    
    print()

# ============================================================
# EXERCISE 2: Path Operations
# ============================================================

def path_operations():
    """
    Join and manipulate paths.
    
    TODO: / operator, joinpath, with_*
    """
    print("--- Exercise 2: Path Operations ---")
    
    # Join paths with / operator
    base = Path('/home/user')
    docs = base / 'documents'
    file = docs / 'report.txt'
    print(f"Joined: {file}")
    
    # Multiple joins
    path = Path('/home') / 'user' / 'documents' / 'file.txt'
    print(f"Multiple joins: {path}")
    
    # Change components
    p = Path('/home/user/file.txt')
    print(f"\nOriginal: {p}")
    print(f"  with_name: {p.with_name('newfile.txt')}")
    print(f"  with_stem: {p.with_stem('newfile')}")
    print(f"  with_suffix: {p.with_suffix('.md')}")
    
    # Relative paths
    p1 = Path('/home/user/documents')
    p2 = Path('/home/user/pictures')
    print(f"\nFrom {p1}")
    print(f"  to {p2}")
    # print(f"  relative: {p2.relative_to(p1.parent)}")
    
    print()

# ============================================================
# EXERCISE 3: Path Properties
# ============================================================

def path_properties():
    """
    Check path properties.
    
    TODO: exists, is_file, is_dir, etc.
    """
    print("--- Exercise 3: Path Properties ---")
    
    # Create temp directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test file
        test_file = tmp_path / 'test.txt'
        test_file.write_text('Hello, World!')
        
        # Create test directory
        test_dir = tmp_path / 'subdir'
        test_dir.mkdir()
        
        print(f"Test file: {test_file}")
        print(f"  exists: {test_file.exists()}")
        print(f"  is_file: {test_file.is_file()}")
        print(f"  is_dir: {test_file.is_dir()}")
        
        print(f"\nTest directory: {test_dir}")
        print(f"  exists: {test_dir.exists()}")
        print(f"  is_file: {test_dir.is_file()}")
        print(f"  is_dir: {test_dir.is_dir()}")
        
        # Non-existent path
        fake = tmp_path / 'fake.txt'
        print(f"\nNon-existent: {fake}")
        print(f"  exists: {fake.exists()}")
    
    print()

# ============================================================
# EXERCISE 4: Reading and Writing
# ============================================================

def reading_writing():
    """
    Read and write files with Path.
    
    TODO: read_text, write_text, read_bytes, write_bytes
    """
    print("--- Exercise 4: Reading and Writing ---")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Write text
        file = tmp_path / 'data.txt'
        file.write_text('Hello, pathlib!\nSecond line.')
        print(f"Written to: {file}")
        
        # Read text
        content = file.read_text()
        print(f"Content:\n{content}")
        
        # Write bytes
        binary_file = tmp_path / 'data.bin'
        binary_file.write_bytes(b'\x00\x01\x02\x03')
        print(f"\nBinary written to: {binary_file}")
        
        # Read bytes
        binary_data = binary_file.read_bytes()
        print(f"Binary data: {binary_data.hex()}")
        
        # File info
        print(f"\nFile size: {file.stat().st_size} bytes")
        print(f"Modified: {datetime.fromtimestamp(file.stat().st_mtime)}")
    
    print()

# ============================================================
# EXERCISE 5: Directory Operations
# ============================================================

def directory_operations():
    """
    Create and navigate directories.
    
    TODO: mkdir, iterdir, glob, rglob
    """
    print("--- Exercise 5: Directory Operations ---")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create directories
        subdir = tmp_path / 'level1' / 'level2'
        subdir.mkdir(parents=True, exist_ok=True)
        print(f"Created: {subdir}")
        
        # Create files
        (tmp_path / 'file1.txt').write_text('content1')
        (tmp_path / 'file2.py').write_text('content2')
        (subdir / 'file3.txt').write_text('content3')
        
        # List directory
        print(f"\nContents of {tmp_path}:")
        for item in tmp_path.iterdir():
            print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")
        
        # Glob patterns
        print(f"\nAll .txt files:")
        for txt_file in tmp_path.glob('*.txt'):
            print(f"  {txt_file.name}")
        
        # Recursive glob
        print(f"\nAll .txt files (recursive):")
        for txt_file in tmp_path.rglob('*.txt'):
            print(f"  {txt_file.relative_to(tmp_path)}")
    
    print()

# ============================================================
# EXERCISE 6: Path Resolution
# ============================================================

def path_resolution():
    """
    Resolve and normalize paths.
    
    TODO: resolve, absolute, relative_to
    """
    print("--- Exercise 6: Path Resolution ---")
    
    # Relative path
    rel_path = Path('documents/file.txt')
    print(f"Relative: {rel_path}")
    print(f"Absolute: {rel_path.absolute()}")
    
    # Resolve (follow symlinks, normalize)
    path_with_dots = Path('.') / '..' / 'file.txt'
    print(f"\nWith dots: {path_with_dots}")
    print(f"Resolved: {path_with_dots.resolve()}")
    
    # Check if relative
    print(f"\nIs absolute: {Path('/home/user').is_absolute()}")
    print(f"Is absolute: {Path('documents').is_absolute()}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World - File Organizer
# ============================================================

def file_organizer():
    """
    Organize files by extension.
    
    TODO: Practical file management
    """
    print("--- Exercise 7: File Organizer ---")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test files
        files = [
            'document1.txt', 'document2.txt',
            'image1.jpg', 'image2.png',
            'script1.py', 'script2.py',
            'data.csv'
        ]
        
        for filename in files:
            (tmp_path / filename).write_text(f'Content of {filename}')
        
        print("Original structure:")
        for item in sorted(tmp_path.iterdir()):
            print(f"  {item.name}")
        
        # Organize by extension
        for file in tmp_path.iterdir():
            if file.is_file():
                ext = file.suffix[1:] if file.suffix else 'no_ext'
                ext_dir = tmp_path / ext
                ext_dir.mkdir(exist_ok=True)
                
                new_path = ext_dir / file.name
                file.rename(new_path)
        
        print("\nOrganized structure:")
        for dir_item in sorted(tmp_path.iterdir()):
            if dir_item.is_dir():
                print(f"  {dir_item.name}/")
                for file in sorted(dir_item.iterdir()):
                    print(f"    {file.name}")
    
    print()

# ============================================================
# PATHLIB VS OS.PATH
# ============================================================

def pathlib_vs_ospath():
    """
    Compare pathlib with os.path.
    """
    print("--- pathlib vs os.path ---")
    
    print("Operation          | os.path              | pathlib")
    print("-" * 60)
    print("Join paths         | os.path.join()       | path / 'sub'")
    print("Get basename       | os.path.basename()   | path.name")
    print("Get directory      | os.path.dirname()    | path.parent")
    print("Get extension      | os.path.splitext()   | path.suffix")
    print("Check exists       | os.path.exists()     | path.exists()")
    print("Check is file      | os.path.isfile()     | path.is_file()")
    print("Check is dir       | os.path.isdir()      | path.is_dir()")
    print("Get absolute       | os.path.abspath()    | path.absolute()")
    print("Expand user        | os.path.expanduser() | Path.home()")
    
    print("\n💡 pathlib advantages:")
    print("  • Object-oriented")
    print("  • Chainable operations")
    print("  • Cross-platform")
    print("  • More readable")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    pathlib Complexity:
    
    Time Complexity:
    - Path creation: O(1)
    - Path joining: O(k) where k is components
    - exists/is_file/is_dir: O(1) system call
    - iterdir: O(n) where n is items
    - glob: O(n) where n is matching files
    - rglob: O(n) recursive traversal
    
    Space Complexity:
    - Path object: O(k) for path string
    - iterdir: O(1) with generator
    - glob: O(m) for m matches
    
    Best Practices:
    - Use pathlib over os.path
    - Use / operator for joining
    - Use exist_ok=True for mkdir
    - Use parents=True for nested dirs
    - Iterate with iterdir() not listdir()
    
    Security:
    - Validate user-provided paths
    - Use resolve() to check real path
    - Check for path traversal (..)
    - Validate file extensions
    - Check permissions before operations
    
    Performance:
    - Path objects are lightweight
    - Operations are lazy
    - Use generators for large dirs
    - Cache resolved paths if needed
    
    Cross-Platform:
    - pathlib handles separators
    - Use Path.home() not ~
    - Test on target platforms
    - Avoid hardcoded separators
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 4: Path Manipulation with pathlib")
    print("=" * 60)
    print()
    
    path_basics()
    path_operations()
    path_properties()
    reading_writing()
    directory_operations()
    path_resolution()
    file_organizer()
    pathlib_vs_ospath()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. pathlib: Modern, object-oriented")
    print("2. Use / operator for joining")
    print("3. Cross-platform by default")
    print("4. More readable than os.path")

