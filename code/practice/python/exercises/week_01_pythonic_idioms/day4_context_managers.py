"""
Week 1, Day 4: Context Managers - __enter__ and __exit__

Learning Objectives:
- Understand the context manager protocol
- Implement custom context managers using __enter__ and __exit__
- Learn when and why to use context managers
- Practice resource management patterns

Time: 10-15 minutes
"""

import sys
import time
from typing import Any, Optional

# ============================================================
# EXERCISE 1: Understanding Context Managers
# ============================================================

def basic_context_manager_usage():
    """
    Review built-in context managers and their benefits.
    
    Context managers ensure proper resource cleanup even if exceptions occur.
    """
    print("--- Exercise 1: Basic Context Manager Usage ---")
    
    # Standard file handling with context manager
    # TODO: Write to a file using 'with' statement
    with open('temp_test.txt', 'w') as f:
        f.write("Hello, Context Managers!")
    
    # File is automatically closed here
    print("✓ File written and automatically closed")
    
    # Compare with manual handling (not recommended)
    f = open('temp_test2.txt', 'w')
    try:
        f.write("Manual handling")
    finally:
        f.close()
    print("✓ Manual file handling (verbose and error-prone)")
    
    print()

# ============================================================
# EXERCISE 2: Implementing Custom Context Manager (Class-based)
# ============================================================

class Timer:
    """
    A context manager that measures execution time.
    
    TODO: Implement __enter__ and __exit__ methods
    """
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Called when entering the 'with' block"""
        # TODO: Record start time
        self.start_time = time.perf_counter()
        print(f"⏱️  Starting: {self.name}")
        return self  # Return self to be used as 'as' variable
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value
            exc_tb: Exception traceback
        
        Returns:
            False to propagate exceptions, True to suppress them
        """
        # TODO: Record end time and print duration
        self.end_time = time.perf_counter()
        duration = self.end_time - self.start_time
        print(f"⏱️  Finished: {self.name} - {duration:.4f}s")
        
        # Handle exceptions if any
        if exc_type is not None:
            print(f"❌ Exception occurred: {exc_type.__name__}: {exc_val}")
        
        return False  # Don't suppress exceptions

def test_timer():
    """Test the Timer context manager"""
    print("--- Exercise 2: Custom Timer Context Manager ---")
    
    # TODO: Use the Timer context manager
    with Timer("Fast operation"):
        sum([i**2 for i in range(1000)])
    
    with Timer("Slow operation"):
        time.sleep(0.1)
        sum([i**2 for i in range(100000)])
    
    # Test with exception
    try:
        with Timer("Operation with error"):
            time.sleep(0.05)
            raise ValueError("Something went wrong!")
    except ValueError:
        print("✓ Exception was propagated correctly")
    
    print()

# ============================================================
# EXERCISE 3: Database Connection Context Manager
# ============================================================

class DatabaseConnection:
    """
    Simulates a database connection with proper resource management.
    
    TODO: Implement a context manager for database connections
    """
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.is_connected = False
    
    def __enter__(self):
        """Establish database connection"""
        # TODO: Simulate connection
        print(f"🔌 Connecting to database: {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        self.is_connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        # TODO: Simulate cleanup
        print(f"🔌 Closing connection to: {self.db_name}")
        self.is_connected = False
        self.connection = None
        
        if exc_type is not None:
            print(f"❌ Rolling back due to error: {exc_val}")
            # In real scenario, rollback transaction
        
        return False
    
    def execute(self, query: str):
        """Execute a query"""
        if not self.is_connected:
            raise RuntimeError("Not connected to database")
        print(f"  📝 Executing: {query}")
        return f"Result of {query}"

def test_database_connection():
    """Test the DatabaseConnection context manager"""
    print("--- Exercise 3: Database Connection Manager ---")
    
    # TODO: Use the DatabaseConnection context manager
    with DatabaseConnection("users_db") as db:
        db.execute("SELECT * FROM users")
        db.execute("INSERT INTO users VALUES ('Alice', 30)")
    
    print("✓ Connection automatically closed\n")
    
    # Test with exception
    try:
        with DatabaseConnection("products_db") as db:
            db.execute("SELECT * FROM products")
            raise ValueError("Query failed!")
    except ValueError:
        print("✓ Connection closed even after exception\n")
    
    print()

# ============================================================
# EXERCISE 4: File Lock Context Manager
# ============================================================

class FileLock:
    """
    A context manager that ensures exclusive access to a file.
    
    TODO: Implement a file locking mechanism
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.lock_filename = f"{filename}.lock"
        self.locked = False
    
    def __enter__(self):
        """Acquire lock"""
        # TODO: Create lock file
        print(f"🔒 Acquiring lock on: {self.filename}")
        
        # Check if already locked
        import os
        if os.path.exists(self.lock_filename):
            raise RuntimeError(f"File {self.filename} is already locked")
        
        # Create lock file
        with open(self.lock_filename, 'w') as f:
            f.write(str(time.time()))
        
        self.locked = True
        print(f"✓ Lock acquired")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock"""
        # TODO: Remove lock file
        import os
        if self.locked and os.path.exists(self.lock_filename):
            os.remove(self.lock_filename)
            print(f"🔓 Lock released on: {self.filename}")
            self.locked = False
        
        return False

def test_file_lock():
    """Test the FileLock context manager"""
    print("--- Exercise 4: File Lock Manager ---")
    
    # TODO: Use the FileLock context manager
    with FileLock("important_data.txt"):
        print("  Working with file...")
        time.sleep(0.1)
        print("  File operations complete")
    
    print("✓ Lock automatically released\n")
    print()

# ============================================================
# EXERCISE 5: Temporary Directory Context Manager
# ============================================================

class TemporaryDirectory:
    """
    Create a temporary directory that's automatically cleaned up.
    
    TODO: Implement temporary directory management
    """
    
    def __init__(self, prefix: str = "tmp_"):
        self.prefix = prefix
        self.path = None
    
    def __enter__(self):
        """Create temporary directory"""
        import os
        import tempfile
        
        # TODO: Create temp directory
        self.path = tempfile.mkdtemp(prefix=self.prefix)
        print(f"📁 Created temporary directory: {self.path}")
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove temporary directory"""
        import shutil
        
        # TODO: Clean up directory
        if self.path:
            shutil.rmtree(self.path)
            print(f"🗑️  Removed temporary directory: {self.path}")
        
        return False

def test_temporary_directory():
    """Test the TemporaryDirectory context manager"""
    print("--- Exercise 5: Temporary Directory Manager ---")
    
    # TODO: Use the TemporaryDirectory context manager
    with TemporaryDirectory(prefix="my_temp_") as temp_dir:
        print(f"  Working in: {temp_dir}")
        
        # Create some files
        import os
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Temporary data")
        
        print(f"  Created file: {test_file}")
    
    print("✓ Directory and contents automatically removed\n")
    print()

# ============================================================
# EXERCISE 6: Suppressing Exceptions
# ============================================================

class SuppressException:
    """
    A context manager that suppresses specific exceptions.
    
    TODO: Implement exception suppression
    """
    
    def __init__(self, *exception_types):
        self.exception_types = exception_types
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suppress specified exceptions"""
        # TODO: Return True if exception should be suppressed
        if exc_type is not None and issubclass(exc_type, self.exception_types):
            print(f"🔇 Suppressed exception: {exc_type.__name__}: {exc_val}")
            return True  # Suppress the exception
        return False

def test_suppress_exception():
    """Test the SuppressException context manager"""
    print("--- Exercise 6: Exception Suppression ---")
    
    # Suppress FileNotFoundError
    with SuppressException(FileNotFoundError):
        with open('nonexistent_file.txt', 'r') as f:
            content = f.read()
    
    print("✓ FileNotFoundError was suppressed\n")
    
    # Don't suppress other exceptions
    try:
        with SuppressException(FileNotFoundError):
            raise ValueError("This should not be suppressed")
    except ValueError as e:
        print(f"✓ ValueError was not suppressed: {e}\n")
    
    print()

# ============================================================
# BONUS CHALLENGE: Nested Context Managers
# ============================================================

class TransactionManager:
    """
    Manages database-like transactions with commit/rollback.
    
    TODO: Implement transaction management
    """
    
    def __init__(self, name: str):
        self.name = name
        self.changes = []
    
    def __enter__(self):
        print(f"🔄 Starting transaction: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, commit
            print(f"✅ Committing transaction: {self.name}")
            print(f"   Changes: {self.changes}")
        else:
            # Exception occurred, rollback
            print(f"❌ Rolling back transaction: {self.name}")
            self.changes.clear()
        
        return False
    
    def add_change(self, change: str):
        """Add a change to the transaction"""
        self.changes.append(change)
        print(f"  + {change}")

def test_nested_contexts():
    """Test nested context managers"""
    print("--- Bonus: Nested Context Managers ---")
    
    # Successful nested transactions
    with TransactionManager("Outer") as outer:
        outer.add_change("Change 1")
        
        with TransactionManager("Inner") as inner:
            inner.add_change("Change 2")
            inner.add_change("Change 3")
        
        outer.add_change("Change 4")
    
    print()
    
    # Failed inner transaction
    try:
        with TransactionManager("Outer") as outer:
            outer.add_change("Change 1")
            
            with TransactionManager("Inner") as inner:
                inner.add_change("Change 2")
                raise ValueError("Inner transaction failed!")
            
            outer.add_change("This won't execute")
    except ValueError:
        print("✓ Inner transaction rolled back\n")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Context Manager Protocol:
    - __enter__: O(1) typically (depends on resource acquisition)
    - __exit__: O(1) typically (depends on cleanup)
    - Overhead is minimal compared to manual try/finally
    
    Benefits:
    - Guarantees cleanup even with exceptions
    - More readable than try/finally
    - Composable (can nest multiple contexts)
    
    Security Considerations:
    - Always clean up resources in __exit__
    - Be careful with exception suppression (return True)
    - Ensure __exit__ is idempotent (safe to call multiple times)
    - Lock files should include process ID to detect stale locks
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1, Day 4: Context Managers")
    print("=" * 60)
    print()
    
    basic_context_manager_usage()
    test_timer()
    test_database_connection()
    test_file_lock()
    test_temporary_directory()
    test_suppress_exception()
    test_nested_contexts()
    
    # Cleanup test files
    import os
    for f in ['temp_test.txt', 'temp_test2.txt']:
        if os.path.exists(f):
            os.remove(f)
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Context managers guarantee resource cleanup")
    print("2. Implement __enter__ and __exit__ for custom managers")
    print("3. __exit__ receives exception info and can suppress it")
    print("4. Use context managers for files, locks, connections, etc.")

