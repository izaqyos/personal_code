# Cursor Q&A Generation Guide

> **Purpose**: Step-by-step guide for generating training data using Cursor AI
> **Target**: 100+ high-quality Q&A examples
> **Time Required**: 2-4 hours (can be split across sessions)

---

## Table of Contents
1. [Setup](#setup)
2. [Understanding the Output Format](#understanding-the-output-format)
3. [Category 1: Code Review (30 examples)](#category-1-code-review-30-examples)
4. [Category 2: Explain Code (30 examples)](#category-2-explain-code-30-examples)
5. [Category 3: Suggest Improvements (20 examples)](#category-3-suggest-improvements-20-examples)
6. [Category 4: Debugging (20 examples)](#category-4-debugging-20-examples)
7. [Compiling Your Dataset](#compiling-your-dataset)
8. [Quality Checklist](#quality-checklist)

---

## Setup

### 1. Open Cursor with your codebase
```bash
cursor /Users/yosii/work/git/personal_code
```

### 2. Keep these files open for reference:
- `code/AI/projects/finetune/data/training/example_dataset.json` (format reference)
- `code/AI/projects/finetune/data/training/schema.json` (schema reference)

### 3. Create a new file to collect your examples:
```bash
touch /Users/yosii/work/git/personal_code/code/AI/projects/finetune/data/training/cursor_generated.json
```

### 4. Start with this template in the new file:
```json
{
  "version": "1.0.0",
  "metadata": {
    "created_at": "2026-01-07",
    "source": "cursor",
    "total_examples": 0
  },
  "data": [
  ]
}
```

---

## Understanding the Output Format

Every training example MUST have this structure:

```json
{
  "id": "cursor_001",
  "instruction": "The question or task",
  "input": "The code to analyze (can be empty for general questions)",
  "output": "The detailed answer/response",
  "category": "code_review|explain_code|suggest_improvements|debugging",
  "language": "javascript|python",
  "source": "cursor",
  "quality": "high"
}
```

### Field Guidelines

| Field | Guidelines |
|-------|------------|
| `id` | Unique ID: `cursor_001`, `cursor_002`, etc. |
| `instruction` | Clear question, 10-50 words |
| `input` | The code snippet, 5-100 lines |
| `output` | Detailed response, 100-500 words |
| `category` | One of: code_review, explain_code, suggest_improvements, debugging |
| `language` | javascript or python |

---

## Category 1: Code Review (30 examples)

### Goal
Train the model to give thoughtful code review feedback like a senior developer would.

### Good Files to Review
Navigate to these directories in your personal_code repo:
```
code/nodejs/examples/
code/nodejs/2024_2025_additions/
code/nodejs/axios101/
code/python/snippets/
code/python/tools/
code/python/web/
```

### Prompt Template

Select a code block (20-80 lines), then use Cmd+K (or Ctrl+K) and paste:

```
Generate a code review training example for LLM fine-tuning.

OUTPUT FORMAT (JSON only, no markdown):
{
  "id": "cursor_review_[NUMBER]",
  "instruction": "Review this [JavaScript/Python] [function/code] for potential issues",
  "input": "[THE SELECTED CODE - KEEP EXACT]",
  "output": "[YOUR DETAILED REVIEW]",
  "category": "code_review",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

REVIEW GUIDELINES:
- Start with a brief summary of what the code does
- List 2-4 specific issues or observations
- For each issue: explain WHY it's a problem
- Suggest fixes with code examples where helpful
- End with what's done well (if anything)
- Be constructive, not harsh

THINGS TO CHECK:
- Error handling (missing try/catch, unhandled promises)
- Input validation
- Security issues (injection, XSS, auth)
- Performance concerns
- Code clarity and naming
- Edge cases
- Best practices for the language
```

### Example Input (select this code)
```javascript
async function getUser(id) {
  const response = await fetch('/api/users/' + id);
  const data = response.json();
  return data;
}
```

### Example Output
```json
{
  "id": "cursor_review_001",
  "instruction": "Review this JavaScript async function for potential issues",
  "input": "async function getUser(id) {\n  const response = await fetch('/api/users/' + id);\n  const data = response.json();\n  return data;\n}",
  "output": "This function fetches user data but has several issues:\n\n**1. Missing `await` on `response.json()`**\nThe `json()` method returns a Promise, so without `await`, you're returning a Promise instead of the actual data.\n\n**2. No error handling**\nIf the fetch fails or returns a non-2xx status, the function will silently fail or throw an unhandled error.\n\n**3. URL construction vulnerability**\nConcatenating the `id` directly into the URL could cause issues if `id` contains special characters. Use template literals or `encodeURIComponent`.\n\n**4. No response status check**\nEven if the request succeeds, a 404 or 500 response won't throw - you'll try to parse error HTML as JSON.\n\n**Improved version:**\n```javascript\nasync function getUser(id) {\n  if (!id) throw new Error('User ID required');\n  \n  const response = await fetch(`/api/users/${encodeURIComponent(id)}`);\n  \n  if (!response.ok) {\n    throw new Error(`Failed to fetch user: ${response.status}`);\n  }\n  \n  return await response.json();\n}\n```\n\nThe function is concise and the intent is clear - good foundation to build on.",
  "category": "code_review",
  "language": "javascript",
  "source": "cursor",
  "quality": "high"
}
```

### Variety Checklist for Code Reviews
Generate reviews for different patterns:
- [ ] API/fetch calls (5 examples)
- [ ] Database operations (5 examples)
- [ ] Authentication/security code (5 examples)
- [ ] Error handling patterns (5 examples)
- [ ] Utility functions (5 examples)
- [ ] Async/Promise patterns (5 examples)

---

## Category 2: Explain Code (30 examples)

### Goal
Train the model to explain code clearly, like teaching a junior developer.

### Good Files to Explain
Look for code with interesting patterns:
```
code/nodejs/functional/           # Functional programming
code/nodejs/nodejs_design_patterns/  # Design patterns
code/python/machine_learning/     # ML code
code/python/Algo/                  # Algorithms
code/nodejs/graphQLDemo/          # GraphQL
```

### Prompt Template

```
Generate an "explain code" training example for LLM fine-tuning.

OUTPUT FORMAT (JSON only):
{
  "id": "cursor_explain_[NUMBER]",
  "instruction": "Explain what this [JavaScript/Python] code does and how it works",
  "input": "[THE SELECTED CODE]",
  "output": "[YOUR EXPLANATION]",
  "category": "explain_code",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

EXPLANATION GUIDELINES:
- Start with a one-sentence summary of the purpose
- Break down the code step-by-step
- Explain any patterns or techniques used
- Give the "why" not just the "what"
- Mention when/where you'd use this code
- Note any gotchas or edge cases
- Use simple language (explain to a junior dev)
```

### Patterns to Look For
- Closures
- Higher-order functions (map, filter, reduce)
- Async patterns (Promises, async/await)
- Decorators (Python)
- Middleware patterns
- Event emitters
- Factory functions
- Memoization
- Debounce/throttle
- Recursion

### Variety Checklist for Explanations
- [ ] Closure examples (3)
- [ ] Async/Promise patterns (5)
- [ ] Array methods (map/filter/reduce) (5)
- [ ] Design patterns (5)
- [ ] Algorithm implementations (5)
- [ ] Python decorators/generators (4)
- [ ] Error handling patterns (3)

---

## Category 3: Suggest Improvements (20 examples)

### Goal
Train the model to suggest practical refactoring and improvements.

### Prompt Template

```
Generate a "suggest improvements" training example for LLM fine-tuning.

OUTPUT FORMAT (JSON only):
{
  "id": "cursor_improve_[NUMBER]",
  "instruction": "How would you improve this [JavaScript/Python] code?",
  "input": "[THE SELECTED CODE]",
  "output": "[YOUR SUGGESTIONS WITH REFACTORED CODE]",
  "category": "suggest_improvements",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

IMPROVEMENT GUIDELINES:
- Identify 2-4 specific improvements
- Explain the benefit of each change
- Provide the refactored code
- Keep improvements practical (not over-engineering)
- Consider: readability, performance, maintainability, testability
```

### Things to Improve
- Long functions → break into smaller ones
- Nested callbacks → async/await
- Repeated code → DRY refactoring
- Magic numbers → named constants
- Poor naming → clear naming
- Missing types → add TypeScript/type hints
- Complex conditions → extract to functions

---

## Category 4: Debugging (20 examples)

### Goal
Train the model to identify and fix bugs.

### Option A: Find Real Bugs
Look through your code for potential issues, or git history for bug fixes:
```bash
git log --oneline --grep="fix" --grep="bug" | head -20
```

### Option B: Introduce Bugs
Take working code and introduce a common bug:
- Off-by-one errors
- Missing await
- Wrong comparison (== vs ===)
- Null reference errors
- Type coercion issues
- Scope issues

### Prompt Template

```
Generate a "find the bug" training example for LLM fine-tuning.

OUTPUT FORMAT (JSON only):
{
  "id": "cursor_debug_[NUMBER]",
  "instruction": "Find and fix the bug in this [JavaScript/Python] code",
  "input": "[CODE WITH BUG]",
  "output": "[BUG EXPLANATION AND FIX]",
  "category": "debugging",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

DEBUG RESPONSE GUIDELINES:
- Clearly identify the bug location
- Explain WHY it's a bug (what breaks)
- Show the fix
- Explain how to prevent similar bugs
```

### Common Bug Types to Include
- [ ] Missing await (3)
- [ ] Off-by-one errors (3)
- [ ] Null/undefined access (3)
- [ ] Type coercion issues (2)
- [ ] Scope/closure bugs (3)
- [ ] Async race conditions (3)
- [ ] Logic errors (3)

---

## Compiling Your Dataset

### Option 1: Manual Compilation
As you generate each example in Cursor, copy the JSON object and add it to your `cursor_generated.json` file.

### Option 2: Batch Processing
If you save examples to separate files, use this script to combine them:

```python
# Save as: scripts/compile_cursor_data.py
import json
import glob
from datetime import datetime

def compile_dataset():
    examples = []

    # Read all JSON files in a directory
    for filepath in glob.glob("data/cursor_raw/*.json"):
        with open(filepath) as f:
            data = json.load(f)
            if isinstance(data, list):
                examples.extend(data)
            else:
                examples.append(data)

    # Create final dataset
    dataset = {
        "version": "1.0.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "source": "cursor",
            "total_examples": len(examples),
            "categories": {}
        },
        "data": examples
    }

    # Count categories
    for ex in examples:
        cat = ex.get("category", "unknown")
        dataset["metadata"]["categories"][cat] = \
            dataset["metadata"]["categories"].get(cat, 0) + 1

    # Save
    with open("data/training/cursor_generated.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"Compiled {len(examples)} examples")
    print(f"Categories: {dataset['metadata']['categories']}")

if __name__ == "__main__":
    compile_dataset()
```

---

## Quality Checklist

Before finalizing your dataset, verify:

### Format Checks
- [ ] All JSON is valid (use a JSON validator)
- [ ] Every example has all required fields
- [ ] IDs are unique
- [ ] Categories are from the allowed list

### Content Checks
- [ ] Outputs are 100-500 words (not too short/long)
- [ ] Code in `input` field is syntactically valid
- [ ] Explanations are accurate (spot-check 10%)
- [ ] Mix of JavaScript and Python
- [ ] No sensitive data (API keys, passwords, personal info)

### Balance Checks
Target distribution:
```
code_review:          30 examples (30%)
explain_code:         30 examples (30%)
suggest_improvements: 20 examples (20%)
debugging:            20 examples (20%)
------------------------------------
TOTAL:               100 examples
```

### Quick Validation Script
```python
# Save as: scripts/validate_dataset.py
import json

def validate():
    with open("data/training/cursor_generated.json") as f:
        data = json.load(f)

    errors = []
    required_fields = ["id", "instruction", "input", "output", "category", "language"]
    valid_categories = ["code_review", "explain_code", "suggest_improvements", "debugging"]

    for i, example in enumerate(data["data"]):
        # Check required fields
        for field in required_fields:
            if field not in example:
                errors.append(f"Example {i}: missing '{field}'")

        # Check category
        if example.get("category") not in valid_categories:
            errors.append(f"Example {i}: invalid category '{example.get('category')}'")

        # Check output length
        output_len = len(example.get("output", ""))
        if output_len < 100:
            errors.append(f"Example {i}: output too short ({output_len} chars)")
        if output_len > 3000:
            errors.append(f"Example {i}: output too long ({output_len} chars)")

    if errors:
        print(f"Found {len(errors)} errors:")
        for e in errors[:20]:  # Show first 20
            print(f"  - {e}")
    else:
        print("✅ All examples valid!")

    print(f"\nTotal examples: {len(data['data'])}")

if __name__ == "__main__":
    validate()
```

---

## Tips for Speed

1. **Use Cursor's chat history**: If a generated example is good, modify the code slightly and regenerate for a variation

2. **Batch similar files**: Do all API-related files together, then all utility files, etc.

3. **Copy-paste the prompt template**: Keep it in a scratch file for quick access

4. **Don't overthink**: If an example is "good enough" (accurate, well-formatted), move on

5. **Take breaks**: Quality drops after ~45 min. Do 20-30 examples per session.

---

## Progress Tracker

| Category | Target | Completed |
|----------|--------|-----------|
| Code Review | 30 | ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ |
| Explain Code | 30 | ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ |
| Improvements | 20 | ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ |
| Debugging | 20 | ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ ☐☐☐☐☐ |

Mark with ✓ as you complete each example!

---

*Good luck! Remember: quality > quantity. 80 great examples beat 150 mediocre ones.*
