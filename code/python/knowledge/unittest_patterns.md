# Python Unittest Patterns

## Overview

Patterns for writing effective unit tests using Python's built-in `unittest` module.

---

## 1. Basic Test Structure

```python
import unittest

class TestMyFunction(unittest.TestCase):
    
    def setUp(self):
        """Called before each test method."""
        self.data = {"key": "value"}
    
    def tearDown(self):
        """Called after each test method."""
        pass
    
    def test_something(self):
        """Test names must start with 'test_'."""
        result = my_function(self.data)
        self.assertEqual(result, "expected")

if __name__ == "__main__":
    unittest.main()
```

---

## 2. Common Assertions

```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Truthiness
self.assertTrue(x)
self.assertFalse(x)

# None
self.assertIsNone(x)
self.assertIsNotNone(x)

# Type
self.assertIsInstance(obj, MyClass)

# Containment
self.assertIn("key", my_dict)
self.assertNotIn("missing", my_list)

# Comparison
self.assertGreater(a, b)
self.assertGreaterEqual(a, b)
self.assertLess(a, b)

# Exceptions
with self.assertRaises(ValueError):
    risky_function()

# Regex
self.assertRegex(text, r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
```

---

## 3. Mocking with unittest.mock

### Basic Patching

```python
from unittest.mock import patch, MagicMock

class TestWithMocks(unittest.TestCase):
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.close')
    def test_chart_renders(self, mock_close, mock_show):
        """Decorators are applied bottom-up."""
        plot_chart(data)
        mock_show.assert_called_once()
        mock_close.assert_called_once()
```

### Mocking Return Values

```python
@patch('my_module.requests.get')
def test_api_call(self, mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"data": "test"}
    )
    
    result = fetch_data()
    self.assertEqual(result["data"], "test")
```

### Mocking Objects

```python
@patch.object(Path, 'exists')
def test_file_check(self, mock_exists):
    mock_exists.return_value = True
    self.assertTrue(check_file())
```

### Patching Builtins

```python
from io import StringIO

@patch('builtins.print')
def test_output(self, mock_print):
    my_function()
    mock_print.assert_called_with("Expected output")

# Capture stdout
@patch('sys.stdout', new_callable=StringIO)
def test_stdout(self, mock_stdout):
    print("Hello")
    self.assertIn("Hello", mock_stdout.getvalue())
```

---

## 4. Temporary Files and Directories

```python
import tempfile
from pathlib import Path

class TestWithTempFiles(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.json"
        
        with open(self.test_file, 'w') as f:
            json.dump({"key": "value"}, f)
    
    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
        os.rmdir(self.temp_dir)
    
    def test_load_file(self):
        data = load_json(self.test_file)
        self.assertEqual(data["key"], "value")
```

---

## 5. Test Organization

### Grouping by Concern

```python
class TestDataLoading(unittest.TestCase):
    """Tests for data loading functions."""
    pass

class TestValidation(unittest.TestCase):
    """Tests for input validation."""
    pass

class TestNegativeCases(unittest.TestCase):
    """Negative test cases."""
    pass

class TestEdgeCases(unittest.TestCase):
    """Edge case tests."""
    pass
```

### Running Specific Tests

```bash
# Run all tests in a file
python -m unittest test_module.py

# Run specific test class
python -m unittest test_module.TestDataLoading

# Run specific test method
python -m unittest test_module.TestDataLoading.test_load_valid_file

# Verbose output
python -m unittest -v test_module.py
```

---

## 6. Custom Test Runner

```python
def run_tests():
    """Run all tests with summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestDataLoading,
        TestValidation,
        TestNegativeCases,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Calculate pass rate
    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    print(f"\nPass Rate: {passed/total*100:.1f}%")
    
    return len(result.failures) == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
```

---

## 7. Real Example: Testing Visualization

```python
class TestPlotBarChart(unittest.TestCase):
    """Tests for bar chart generation."""
    
    def setUp(self):
        self.test_data = {
            "reviews": [
                {"github_username": "user1", "display_name": "User One", "full_2025": 100},
                {"github_username": "user2", "display_name": "User Two", "full_2025": 50},
            ]
        }
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.close')
    def test_bar_chart_renders(self, mock_close, mock_show):
        """Test that bar chart renders without error."""
        viz.plot_bar_chart(self.test_data, "full_2025")
        mock_show.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('builtins.print')
    def test_bar_chart_empty_data(self, mock_print):
        """Test bar chart with empty data returns early."""
        data = {"reviews": []}
        viz.plot_bar_chart(data, "full_2025")
        mock_print.assert_called()  # Should print warning
```

---

## Common Patterns

| Pattern | When to Use |
|---------|-------------|
| `@patch()` decorator | Mock external dependencies |
| `setUp/tearDown` | Shared test fixtures |
| `assertRaises` | Testing exception handling |
| `MagicMock` | Complex mock objects |
| Custom runner | CI/CD with reporting |

---

## See Also

- [unittest docs](https://docs.python.org/3/library/unittest.html)
- [unittest.mock docs](https://docs.python.org/3/library/unittest.mock.html)
- `~/work/CheckPoint/Jira/statistics/test_visualize_reviews.py` - Real example

---

**Created:** 2026-01-27  
**Source:** Code Review Statistics project
