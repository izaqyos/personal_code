# Efficient Use of Cursor IDE

> Maximize your productivity with AI-powered coding in Cursor.

---

## Overview

Cursor is a VS Code fork with deep AI integration. This guide covers techniques to use it effectively for AI/ML development.

---

## Core Features

### 1. Chat (Cmd/Ctrl + L)

```
The AI chat sidebar for:
- Explaining code
- Generating functions
- Debugging help
- Architecture discussions

Pro tips:
- Reference files with @filename
- Reference functions with @functionName
- Use @codebase for project-wide context
- Keep conversations focused on one topic
```

### 2. Inline Edit (Cmd/Ctrl + K)

```
Edit code directly in the editor:

1. Select code (or put cursor on line)
2. Press Cmd+K
3. Describe the change
4. Review and accept/reject

Example prompts:
- "Add type hints"
- "Convert to async"
- "Add error handling"
- "Optimize this loop"
```

### 3. Composer (Cmd/Ctrl + I)

```
Multi-file editing mode:

Best for:
- Refactoring across files
- Creating new features
- Implementing patterns consistently

Usage:
1. Open Composer
2. Describe what you want
3. AI generates changes across files
4. Review each file, accept/reject
```

---

## Effective Prompting in Cursor

### Be Specific

```
❌ Bad:  "Fix this"
✅ Good: "Fix the TypeError on line 23 where model expects a tensor but receives a list"

❌ Bad:  "Make it better"
✅ Good: "Optimize this training loop to use batch processing instead of single samples"
```

### Provide Context

```
Include:
- What the code should do
- Constraints (performance, compatibility)
- Related code/files

Example:
"Implement a custom Dataset class for loading images from @data/images.
It should:
- Support transforms
- Handle missing files gracefully
- Be compatible with DataLoader (multiple workers)
Reference the existing @TextDataset for style"
```

### Use @ References

```
@file.py           - Reference specific file
@folder/           - Reference folder contents
@functionName      - Reference specific function
@codebase          - Search entire project
@docs              - Reference documentation
@web               - Search the web
```

---

## ML-Specific Workflows

### 1. Building Models

```python
# Prompt: "Create a ResNet-18 implementation with:
# - Configurable number of classes
# - Optional pretrained weights
# - Feature extraction mode
# Reference @torchvision.models for API style"

class ResNet18(nn.Module):
    def __init__(self, num_classes=1000, pretrained=True, feature_extract=False):
        super().__init__()
        self.model = torchvision.models.resnet18(pretrained=pretrained)

        if feature_extract:
            for param in self.model.parameters():
                param.requires_grad = False

        self.model.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        return self.model(x)
```

### 2. Writing Training Loops

```python
# Prompt: "Generate a training loop with:
# - Mixed precision training
# - Gradient accumulation
# - Logging to wandb
# - Early stopping
# - Checkpoint saving"

def train(model, train_loader, val_loader, config):
    scaler = torch.cuda.amp.GradScaler()
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(config.epochs):
        model.train()
        for i, (x, y) in enumerate(train_loader):
            with torch.cuda.amp.autocast():
                loss = model(x, y) / config.accumulation_steps

            scaler.scale(loss).backward()

            if (i + 1) % config.accumulation_steps == 0:
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()

        # Validation
        val_loss = validate(model, val_loader)
        wandb.log({"val_loss": val_loss, "epoch": epoch})

        # Checkpointing
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(model, optimizer, epoch, val_loss)
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= config.patience:
                break
```

### 3. Debugging Tensor Operations

```
When you get shape mismatches:

1. Select the problematic code
2. Cmd+K: "Add print statements showing tensor shapes at each step"
3. Run and identify mismatch
4. Cmd+K: "Fix the shape mismatch between [32, 512] and [512, 256]"
```

### 4. Converting Code Between Frameworks

```
# Prompt: "Convert this PyTorch model to JAX/Flax
# Reference @jax_utils.py for our JAX conventions"

# PyTorch
class Attention(nn.Module):
    def __init__(self, dim, heads):
        super().__init__()
        self.heads = heads
        self.scale = (dim // heads) ** -0.5
        self.qkv = nn.Linear(dim, dim * 3)

# Converts to Flax
class Attention(nn.Module):
    dim: int
    heads: int

    @nn.compact
    def __call__(self, x):
        qkv = nn.Dense(self.dim * 3)(x)
        # ...
```

---

## Keyboard Shortcuts

| Action | Mac | Windows |
|--------|-----|---------|
| Open Chat | Cmd + L | Ctrl + L |
| Inline Edit | Cmd + K | Ctrl + K |
| Composer | Cmd + I | Ctrl + I |
| Accept Suggestion | Tab | Tab |
| Reject Suggestion | Esc | Esc |
| New Chat | Cmd + Shift + L | Ctrl + Shift + L |
| Toggle Sidebar | Cmd + B | Ctrl + B |

---

## Settings for ML Development

### Recommended .cursorrules

Create `.cursorrules` in your project root:

```
You are an expert ML/AI engineer.

Code style:
- Use type hints for all function signatures
- Follow PEP 8 style guidelines
- Prefer PyTorch over TensorFlow
- Use dataclasses for configs
- Include docstrings with Args, Returns, Examples

ML conventions:
- Always set random seeds for reproducibility
- Use torch.no_grad() for inference
- Prefer nn.Sequential for simple architectures
- Use einops for tensor operations
- Log metrics with wandb

Testing:
- Write unit tests for model forward passes
- Test with small tensors first
- Verify gradient flow

When generating code:
- Include example usage
- Add shape comments for tensor operations
- Handle edge cases (empty batches, single samples)
```

### Model Selection

```
Settings → Models

For ML code:
- Claude 3.5 Sonnet: Best for complex reasoning
- GPT-4: Good for architecture discussions
- Fast model (GPT-3.5): Quick edits, simple completions

Rule of thumb:
- Complex problems → Claude/GPT-4
- Simple edits → Fast model
```

---

## Common Workflows

### 1. Implementing Papers

```
1. Paste paper section in chat
2. "Implement this attention mechanism from the paper"
3. Review, ask follow-up questions
4. "Now write a test to verify the output shapes"
```

### 2. Debugging CUDA Errors

```
1. Paste the full error traceback
2. "Explain this CUDA error and suggest fixes"
3. Apply suggested fix with Cmd+K
4. "Add device checking to prevent this in future"
```

### 3. Optimizing Training

```
1. Share your training loop
2. "Profile this and suggest optimizations for:
   - Memory usage
   - Training speed
   - Numerical stability"
3. Apply changes incrementally
```

---

## Best Practices

### DO:
- Reference specific files/functions with @
- Break complex requests into steps
- Review all AI-generated code carefully
- Use version control before large changes
- Keep chat contexts focused

### DON'T:
- Accept code blindly without understanding
- Let AI make changes across too many files at once
- Share sensitive data/keys in prompts
- Rely on AI for security-critical code without review

---

## Exercises

1. **Setup**: Configure .cursorrules for your ML project
2. **Model**: Use Composer to generate a complete model + training script
3. **Debug**: Practice debugging with AI assistance
4. **Refactor**: Convert a notebook to proper modules using Composer
5. **Document**: Generate docstrings for an entire file with Cmd+K

---

## Key Takeaways

- Use @references to give AI proper context
- Match model selection to task complexity
- Configure .cursorrules for consistent output
- Review all generated code carefully
- Break complex tasks into smaller steps
- Chat for discussion, Cmd+K for edits, Composer for multi-file

---

## Next Steps

→ Continue to [02-claude-code-efficiency.md](./02-claude-code-efficiency.md)
