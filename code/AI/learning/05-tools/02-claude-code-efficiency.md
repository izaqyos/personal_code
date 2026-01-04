# Efficient Use of Claude Code

> Maximize your productivity with Claude Code CLI.

---

## Overview

Claude Code is Anthropic's official CLI for Claude, providing terminal-based AI assistance for software engineering tasks.

---

## Getting Started

### Installation

```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or run directly
npx @anthropic-ai/claude-code

# Verify installation
claude --version
```

### Basic Usage

```bash
# Start interactive session
claude

# Start with a specific task
claude "Create a Python script that..."

# Continue previous conversation
claude --continue
```

---

## Core Commands

### Essential Commands

```bash
/help           # Show all commands
/clear          # Clear conversation history
/compact        # Summarize and compress context
/model          # Change the AI model
/vim            # Toggle vim mode for input
/history        # Show command history
```

### File Operations

```bash
# Claude can read, write, and edit files
"Read the file src/model.py"
"Create a new file called utils.py with..."
"Edit the train function to add logging"
```

### Shell Integration

```bash
# Run shell commands through Claude
"Run pytest and fix any failing tests"
"Install the required dependencies"
"Check git status and create a commit"
```

---

## Effective Prompting

### Be Direct and Specific

```bash
❌ "Can you help with my code?"
✅ "Fix the TypeError in src/train.py line 45 where the model expects a dict but receives a list"

❌ "Make my training faster"
✅ "Add mixed precision training and gradient accumulation to the training loop in train.py"
```

### Provide Context

```bash
# Reference specific files
"Read src/model.py and src/data.py, then create a training script that uses both"

# Explain the goal
"I'm building an image classifier. Create a Dataset class for loading images from data/train/"

# Mention constraints
"Implement this using only standard library, no external dependencies"
```

### Multi-Step Tasks

```bash
# Break complex tasks into steps
"Let's implement a transformer model. First, read the existing code in src/ to understand the project structure"

# Then follow up
"Now create the attention mechanism in src/attention.py"
"Next, implement the full transformer block"
```

---

## ML-Specific Workflows

### 1. Project Scaffolding

```bash
# Claude can create entire project structures
"Create a PyTorch project structure with:
- src/ for source code
- data/ for datasets
- configs/ for yaml configs
- scripts/ for training/eval scripts
Include a proper setup.py and requirements.txt"
```

### 2. Model Implementation

```bash
# Implement from papers
"Implement the Vision Transformer (ViT) from scratch in src/models/vit.py.
Include:
- Patch embedding
- Positional encoding
- Transformer encoder
- Classification head
Add type hints and docstrings"
```

### 3. Training Scripts

```bash
"Create a training script in scripts/train.py that:
- Loads config from configs/train.yaml
- Supports distributed training
- Logs to wandb
- Saves checkpoints every N epochs
- Has early stopping
Reference src/models/ for the model definition"
```

### 4. Debugging

```bash
# Share error and get help
"I'm getting this error when training:
RuntimeError: CUDA out of memory...

My batch size is 32 and model has 100M params.
Help me reduce memory usage without hurting performance much"
```

### 5. Code Review

```bash
"Review src/model.py for:
- Potential bugs
- Performance issues
- Best practices
- Missing error handling"
```

---

## Advanced Features

### Context Management

```bash
# Claude remembers conversation context
# Use /compact to summarize when context gets long
/compact

# Clear and start fresh
/clear
```

### Project Files

Create `CLAUDE.md` in project root for persistent context:

```markdown
# Project: Image Classification

## Overview
PyTorch-based image classifier for medical imaging.

## Key Files
- src/models/resnet.py - Main model
- src/data/dataset.py - Custom dataset
- configs/train.yaml - Training config

## Conventions
- Use type hints everywhere
- Follow PEP 8
- Test coverage > 80%

## Current Task
Implementing attention mechanism for improved accuracy.
```

### Custom Commands (.claude/commands/)

Create reusable commands:

```bash
# .claude/commands/lint.md
Run flake8 and mypy on the codebase.
Fix any issues found automatically.
Show me a summary of what was fixed.
```

Then use:
```bash
/lint
```

---

## Integration with Git

### Commits

```bash
"Create a commit with all the changes we made.
Use a descriptive message following conventional commits"
```

### Pull Requests

```bash
"Create a pull request for the current branch.
Include:
- Summary of changes
- Testing done
- Any breaking changes"
```

### Code Review Workflow

```bash
# Review a PR
"Fetch PR #123 and review the changes"

# Fix review comments
"Address the review comments on PR #123"
```

---

## Configuration

### Settings File (~/.claude/settings.json)

```json
{
  "model": "claude-sonnet-4-20250514",
  "theme": "dark",
  "editor": "vim",
  "autoSave": true,
  "verbose": false
}
```

### Environment Variables

```bash
export ANTHROPIC_API_KEY="your-key"
export CLAUDE_MODEL="claude-sonnet-4-20250514"
```

---

## Best Practices

### DO:
```
✅ Start with reading relevant files
✅ Break complex tasks into steps
✅ Verify changes before moving on
✅ Use /compact for long conversations
✅ Create CLAUDE.md for project context
✅ Review all generated code
```

### DON'T:
```
❌ Make changes without understanding them
❌ Skip testing generated code
❌ Share API keys or secrets
❌ Let context get too long without /compact
❌ Accept code blindly for security-critical paths
```

---

## Common Patterns

### Explore → Plan → Implement

```bash
# 1. Explore
"Read the codebase and explain the architecture"

# 2. Plan
"How should we implement feature X? Give me options"

# 3. Implement
"Let's go with option 2. Start by creating..."
```

### Test-Driven Development

```bash
# 1. Write tests first
"Write tests for a function that calculates attention scores"

# 2. Implement
"Now implement the function to pass these tests"

# 3. Verify
"Run the tests and fix any failures"
```

### Iterative Refinement

```bash
# Start simple
"Create a basic training loop"

# Add complexity
"Add mixed precision training"
"Add gradient accumulation"
"Add checkpointing"
"Add logging"
```

---

## Troubleshooting

### Context Too Long

```bash
/compact
# Or start fresh
/clear
```

### Wrong File Edited

```bash
# Claude maintains file state
"Undo the last change to src/model.py"
# Or use git
"Run git checkout src/model.py"
```

### Model Not Understanding

```bash
# Provide more context
"Read these files first: src/model.py, src/train.py
Now, with this context, implement..."
```

---

## Exercises

1. **Setup**: Create a new ML project using Claude Code from scratch
2. **Implement**: Build a complete training pipeline through conversation
3. **Debug**: Practice debugging with error messages
4. **Review**: Have Claude review and improve existing code
5. **Automate**: Create custom commands for your workflow

---

## Key Takeaways

- Claude Code excels at multi-file, multi-step tasks
- Always start by reading relevant files for context
- Break complex tasks into smaller steps
- Use /compact to manage long conversations
- Create CLAUDE.md for project-specific context
- Review and test all generated code
- Use custom commands for repetitive tasks

---

## Next Steps

→ Continue to [03-python-ml-libraries.md](./03-python-ml-libraries.md)
