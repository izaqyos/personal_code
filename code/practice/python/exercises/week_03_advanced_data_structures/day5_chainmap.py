"""
Week 3, Day 5: ChainMap - Layered Dictionary Lookups

Learning Objectives:
- Master ChainMap for layered dictionary searches
- Learn configuration hierarchy patterns
- Understand scope chain implementations
- Practice context management with ChainMap

Time: 10-15 minutes
"""

from collections import ChainMap
from typing import Dict, Any

# ============================================================
# EXERCISE 1: ChainMap Basics
# ============================================================

def chainmap_basics():
    """
    Learn basic ChainMap operations.
    
    ChainMap: Groups multiple dicts into single view, searches in order
    """
    print("--- Exercise 1: ChainMap Basics ---")
    
    # Create separate dicts
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 20, 'c': 3}
    dict3 = {'c': 30, 'd': 4}
    
    # Create ChainMap
    cm = ChainMap(dict1, dict2, dict3)
    
    print(f"dict1: {dict1}")
    print(f"dict2: {dict2}")
    print(f"dict3: {dict3}")
    print(f"\nChainMap: {cm}")
    
    # Lookup order: dict1 -> dict2 -> dict3
    print(f"\ncm['a'] = {cm['a']}")  # From dict1
    print(f"cm['b'] = {cm['b']}")  # From dict1 (shadows dict2)
    print(f"cm['c'] = {cm['c']}")  # From dict2 (shadows dict3)
    print(f"cm['d'] = {cm['d']}")  # From dict3
    
    # All keys
    print(f"\nAll keys: {list(cm.keys())}")
    
    print()

# ============================================================
# EXERCISE 2: Configuration Hierarchy
# ============================================================

def configuration_hierarchy():
    """
    Use ChainMap for configuration with defaults and overrides.
    
    TODO: Implement config hierarchy: CLI args > env vars > config file > defaults
    """
    print("--- Exercise 2: Configuration Hierarchy ---")
    
    # Default configuration
    defaults = {
        'host': 'localhost',
        'port': 8080,
        'debug': False,
        'timeout': 30
    }
    
    # Configuration file
    config_file = {
        'host': 'prod.example.com',
        'port': 80
    }
    
    # Environment variables
    env_vars = {
        'debug': True
    }
    
    # Command-line arguments
    cli_args = {
        'port': 9000
    }
    
    # Create ChainMap (priority: CLI > env > config > defaults)
    config = ChainMap(cli_args, env_vars, config_file, defaults)
    
    print("Configuration hierarchy:")
    print(f"  host: {config['host']}")      # From config_file
    print(f"  port: {config['port']}")      # From cli_args
    print(f"  debug: {config['debug']}")    # From env_vars
    print(f"  timeout: {config['timeout']}")  # From defaults
    
    print("\nConfiguration sources:")
    for key in ['host', 'port', 'debug', 'timeout']:
        for i, mapping in enumerate(config.maps):
            if key in mapping:
                source = ['CLI', 'ENV', 'CONFIG', 'DEFAULT'][i]
                print(f"  {key}: {mapping[key]} (from {source})")
                break
    
    print()

# ============================================================
# EXERCISE 3: Modifying ChainMap
# ============================================================

def modifying_chainmap():
    """
    Understand how modifications work in ChainMap.
    
    TODO: Practice updates, deletions, and new_child()
    """
    print("--- Exercise 3: Modifying ChainMap ---")
    
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    cm = ChainMap(dict1, dict2)
    
    print(f"Original ChainMap: {cm}")
    
    # Updates go to first dict only
    cm['a'] = 100
    print(f"\nAfter cm['a'] = 100:")
    print(f"  ChainMap: {cm}")
    print(f"  dict1: {dict1}")
    
    # New keys go to first dict
    cm['e'] = 5
    print(f"\nAfter cm['e'] = 5:")
    print(f"  ChainMap: {cm}")
    print(f"  dict1: {dict1}")
    
    # Delete from first dict
    del cm['a']
    print(f"\nAfter del cm['a']:")
    print(f"  ChainMap: {cm}")
    print(f"  dict1: {dict1}")
    
    print()

# ============================================================
# EXERCISE 4: new_child() Method
# ============================================================

def new_child_examples():
    """
    Use new_child() to create nested scopes.
    
    TODO: Practice scope management
    """
    print("--- Exercise 4: new_child() Method ---")
    
    # Global scope
    global_scope = {'x': 'global_x', 'y': 'global_y'}
    cm = ChainMap(global_scope)
    
    print(f"Global scope: {dict(cm)}")
    
    # Enter function scope
    cm = cm.new_child({'x': 'func_x', 'z': 'func_z'})
    print(f"\nFunction scope: {dict(cm)}")
    print(f"  x = {cm['x']}")  # From function scope
    print(f"  y = {cm['y']}")  # From global scope
    print(f"  z = {cm['z']}")  # From function scope
    
    # Enter block scope
    cm = cm.new_child({'x': 'block_x', 'w': 'block_w'})
    print(f"\nBlock scope: {dict(cm)}")
    print(f"  x = {cm['x']}")  # From block scope
    print(f"  y = {cm['y']}")  # From global scope
    print(f"  z = {cm['z']}")  # From function scope
    print(f"  w = {cm['w']}")  # From block scope
    
    # Exit block scope
    cm = cm.parents
    print(f"\nBack to function scope: {dict(cm)}")
    print(f"  x = {cm['x']}")  # From function scope
    
    # Exit function scope
    cm = cm.parents
    print(f"\nBack to global scope: {dict(cm)}")
    print(f"  x = {cm['x']}")  # From global scope
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - Template Variables
# ============================================================

class TemplateEngine:
    """
    Simple template engine using ChainMap for variable resolution.
    
    TODO: Implement template rendering with scoped variables
    """
    
    def __init__(self, globals: Dict[str, Any] = None):
        self.globals = globals or {}
        self.context = ChainMap(self.globals)
    
    def render(self, template: str, locals: Dict[str, Any] = None) -> str:
        """Render template with local and global variables"""
        # Create new scope with locals
        if locals:
            context = self.context.new_child(locals)
        else:
            context = self.context
        
        # Simple variable substitution
        result = template
        for key, value in context.items():
            result = result.replace(f"{{{key}}}", str(value))
        
        return result
    
    def push_scope(self, variables: Dict[str, Any]):
        """Push new variable scope"""
        self.context = self.context.new_child(variables)
    
    def pop_scope(self):
        """Pop variable scope"""
        self.context = self.context.parents

def test_template_engine():
    """Test template engine"""
    print("--- Exercise 5: Template Engine ---")
    
    # Global variables
    engine = TemplateEngine({
        'site_name': 'MyWebsite',
        'year': 2024
    })
    
    # Render with local variables
    template = "Welcome to {site_name}! User: {username}, Year: {year}"
    result = engine.render(template, {'username': 'Alice'})
    print(f"Rendered: {result}")
    
    # Nested scopes
    print("\nNested scopes:")
    engine.push_scope({'section': 'Blog'})
    template2 = "{site_name} - {section}"
    print(f"  Level 1: {engine.render(template2)}")
    
    engine.push_scope({'subsection': 'Python Tips'})
    template3 = "{site_name} - {section} - {subsection}"
    print(f"  Level 2: {engine.render(template3)}")
    
    engine.pop_scope()
    print(f"  Back to Level 1: {engine.render(template2)}")
    
    print()

# ============================================================
# EXERCISE 6: Variable Scope Chain
# ============================================================

class ScopeManager:
    """
    Manage variable scopes like a programming language.
    
    TODO: Implement scope management for variables
    """
    
    def __init__(self):
        self.scopes = ChainMap({})  # Start with empty global scope
    
    def enter_scope(self):
        """Enter new scope"""
        self.scopes = self.scopes.new_child()
    
    def exit_scope(self):
        """Exit current scope"""
        if len(self.scopes.maps) > 1:
            self.scopes = self.scopes.parents
    
    def set_variable(self, name: str, value: Any):
        """Set variable in current scope"""
        self.scopes[name] = value
    
    def get_variable(self, name: str) -> Any:
        """Get variable (searches up scope chain)"""
        return self.scopes.get(name)
    
    def current_scope_vars(self) -> Dict:
        """Get variables in current scope only"""
        return dict(self.scopes.maps[0]) if self.scopes.maps else {}
    
    def all_visible_vars(self) -> Dict:
        """Get all visible variables"""
        return dict(self.scopes)

def test_scope_manager():
    """Test scope manager"""
    print("--- Exercise 6: Scope Manager ---")
    
    sm = ScopeManager()
    
    # Global scope
    sm.set_variable('x', 10)
    sm.set_variable('y', 20)
    print(f"Global scope: {sm.all_visible_vars()}")
    
    # Function scope
    sm.enter_scope()
    sm.set_variable('x', 100)  # Shadows global x
    sm.set_variable('z', 30)
    print(f"\nFunction scope:")
    print(f"  Current scope: {sm.current_scope_vars()}")
    print(f"  All visible: {sm.all_visible_vars()}")
    print(f"  x = {sm.get_variable('x')}")  # 100 (local)
    print(f"  y = {sm.get_variable('y')}")  # 20 (global)
    
    # Block scope
    sm.enter_scope()
    sm.set_variable('x', 1000)  # Shadows both
    print(f"\nBlock scope:")
    print(f"  Current scope: {sm.current_scope_vars()}")
    print(f"  x = {sm.get_variable('x')}")  # 1000 (block)
    print(f"  y = {sm.get_variable('y')}")  # 20 (global)
    print(f"  z = {sm.get_variable('z')}")  # 30 (function)
    
    # Exit scopes
    sm.exit_scope()
    print(f"\nBack to function scope: x = {sm.get_variable('x')}")  # 100
    
    sm.exit_scope()
    print(f"Back to global scope: x = {sm.get_variable('x')}")  # 10
    
    print()

# ============================================================
# EXERCISE 7: ChainMap vs dict.update()
# ============================================================

def chainmap_vs_update():
    """
    Compare ChainMap with dict.update() approach.
    
    TODO: Understand performance and use case differences
    """
    print("--- Exercise 7: ChainMap vs dict.update() ---")
    
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 20, 'c': 3}
    dict3 = {'c': 30, 'd': 4}
    
    # ChainMap approach (no copying)
    cm = ChainMap(dict1, dict2, dict3)
    print(f"ChainMap: {dict(cm)}")
    print(f"  Preserves original dicts: {dict1}, {dict2}, {dict3}")
    
    # dict.update() approach (copies data)
    merged = {}
    merged.update(dict3)  # Lowest priority
    merged.update(dict2)
    merged.update(dict1)  # Highest priority
    print(f"\nMerged dict: {merged}")
    print(f"  Original dicts unchanged: {dict1}, {dict2}, {dict3}")
    
    # Modify original
    print("\nModifying dict1['a'] = 100:")
    dict1['a'] = 100
    print(f"  ChainMap sees change: {cm['a']}")
    print(f"  Merged dict doesn't: {merged['a']}")
    
    print("\n💡 Use ChainMap when:")
    print("  - You want live updates from source dicts")
    print("  - You need to preserve original dicts")
    print("  - You want layered lookups (scopes)")
    print("  - Memory efficiency matters")
    
    print("\n💡 Use dict.update() when:")
    print("  - You want a snapshot (no live updates)")
    print("  - You need a single flat dict")
    print("  - Performance of lookups is critical")
    
    print()

# ============================================================
# BONUS CHALLENGE: Multi-Level Config
# ============================================================

class MultiLevelConfig:
    """
    Multi-level configuration system with ChainMap.
    
    TODO: Implement config with system, user, and project levels
    """
    
    def __init__(self):
        self.system = {}
        self.user = {}
        self.project = {}
        self._rebuild()
    
    def _rebuild(self):
        """Rebuild ChainMap with current priority"""
        self.config = ChainMap(self.project, self.user, self.system)
    
    def set_system(self, key: str, value: Any):
        """Set system-level config"""
        self.system[key] = value
        self._rebuild()
    
    def set_user(self, key: str, value: Any):
        """Set user-level config"""
        self.user[key] = value
        self._rebuild()
    
    def set_project(self, key: str, value: Any):
        """Set project-level config"""
        self.project[key] = value
        self._rebuild()
    
    def get(self, key: str, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def get_source(self, key: str) -> str:
        """Get which level provides the value"""
        if key in self.project:
            return "project"
        elif key in self.user:
            return "user"
        elif key in self.system:
            return "system"
        return "not found"

def test_multilevel_config():
    """Test multi-level config"""
    print("--- Bonus Challenge: Multi-Level Config ---")
    
    config = MultiLevelConfig()
    
    # System defaults
    config.set_system('editor', 'nano')
    config.set_system('theme', 'light')
    config.set_system('font_size', 12)
    
    # User preferences
    config.set_user('editor', 'vim')
    config.set_user('theme', 'dark')
    
    # Project settings
    config.set_project('editor', 'vscode')
    
    print("Configuration values:")
    for key in ['editor', 'theme', 'font_size']:
        value = config.get(key)
        source = config.get_source(key)
        print(f"  {key}: {value} (from {source})")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    ChainMap Operations:
    - Lookup: O(m) where m is number of maps (usually small)
    - Insert/Update: O(1) - goes to first map
    - Delete: O(1) - from first map
    - new_child(): O(1) - creates new view
    
    vs Merged dict:
    - Lookup: O(1) average
    - Creation: O(n) to copy all data
    - Updates don't affect originals
    
    Space Complexity:
    - ChainMap: O(1) - just stores references
    - Merged dict: O(n) - copies all data
    
    Benefits:
    - No data copying
    - Live updates from source dicts
    - Natural scope chain representation
    - Memory efficient
    
    Use Cases:
    - Configuration hierarchies
    - Variable scope chains
    - Template variable resolution
    - Context management
    - Layered defaults
    
    When NOT to Use:
    - Need fast lookups (many maps = slower)
    - Want snapshot (use dict.update())
    - Need to modify lower layers
    - Serialization required
    
    Security Considerations:
    - Validate all input dicts
    - Be careful with user-provided keys
    - Consider immutable views for read-only access
    - Limit chain depth for performance
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 5: ChainMap")
    print("=" * 60)
    print()
    
    chainmap_basics()
    configuration_hierarchy()
    modifying_chainmap()
    new_child_examples()
    test_template_engine()
    test_scope_manager()
    chainmap_vs_update()
    test_multilevel_config()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. ChainMap groups multiple dicts into single view")
    print("2. Searches dicts in order (first to last)")
    print("3. Perfect for configuration hierarchies and scopes")
    print("4. new_child() creates nested scopes efficiently")

