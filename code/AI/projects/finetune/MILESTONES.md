# Fine-Tuning Project: Detailed Milestones & Instructions

> **Data Source**: `/Users/yosii/work/git/personal_code` (~10,294 source files)
> **GitHub**: `izaqyos/personal_code`
> **Last Updated**: 2026-01-07

---

## Overview

This document provides step-by-step instructions for each milestone. Each milestone includes:
- **Objective**: What we're trying to achieve
- **Input**: What's needed to start
- **Output**: What's produced
- **Dependencies**: What must be completed first
- **Owner**: Who/what does the work (You / AI / Script)

---

## Milestone Map

```
M1: Collect Code        ──┐
                          ├──► M3: Generate Q&A Dataset ──► M5: First Training Run
M2: Export PR Reviews   ──┘              │                          │
                                         │                          ▼
M4: Baseline Evaluation ─────────────────┴──────────────► M6: Evaluate & Compare
                                                                    │
                                                                    ▼
                                                          M7: Full Training
                                                                    │
                                                                    ▼
                                                          M8: Deploy to Ollama
```

---

## M1: Collect Source Code from Personal Repo

### Objective
Extract and clean source code from your personal_code repository, excluding sensitive files, binaries, and generated code.

### Details

| Field | Value |
|-------|-------|
| **Owner** | Python Script (`collect_code.py`) |
| **Input** | Path: `/Users/yosii/work/git/personal_code` |
| **Output** | `data/raw/collected_code.json` + `data/raw/manifest.json` |
| **Dependencies** | None (first step) |
| **Est. Time** | 2-5 minutes |

### Step-by-Step Instructions

```bash
# 1. Navigate to scripts directory
cd /Users/yosii/work/git/personal_code/code/AI/projects/finetune/scripts

# 2. Run the collection script
python collect_code.py \
  --repos /Users/yosii/work/git/personal_code \
  --output ../data/raw/ \
  --include-tests

# 3. Review the output
cat ../data/raw/manifest.json | head -50
```

### Expected Output Structure
```json
{
  "metadata": {
    "collected_at": "2026-01-07T...",
    "stats": {
      "total_files": 10294,
      "collected_files": ~2000-5000,
      "by_language": {"javascript": 3000, "python": 1500, ...}
    }
  },
  "files": [
    {"relative_path": "code/nodejs/example.js", "content": "...", "language": "javascript"}
  ]
}
```

### Success Criteria
- [ ] Script completes without errors
- [ ] `collected_code.json` created with 1000+ files
- [ ] No sensitive files included (check manifest)
- [ ] File sizes reasonable (< 50MB total JSON)

---

## M2: Export PR Reviews from GitHub

### Objective
Extract pull request review comments from your GitHub repository to use as high-quality training data.

### Details

| Field | Value |
|-------|-------|
| **Owner** | Python Script (`export_pr_reviews.py`) + GitHub CLI |
| **Input** | GitHub repo: `izaqyos/personal_code` |
| **Output** | `data/pr_reviews/pr_reviews_raw.json` + `pr_reviews_training.json` |
| **Dependencies** | GitHub CLI installed and authenticated |
| **Est. Time** | 5-15 minutes (depends on PR count) |

### Prerequisites

```bash
# 1. Install GitHub CLI (if not installed)
brew install gh

# 2. Authenticate with GitHub
gh auth login
# Follow prompts: GitHub.com → HTTPS → Login with browser

# 3. Verify authentication
gh auth status
# Should show: ✓ Logged in to github.com
```

### Step-by-Step Instructions

```bash
# 1. Navigate to scripts directory
cd /Users/yosii/work/git/personal_code/code/AI/projects/finetune/scripts

# 2. Check how many PRs exist (optional - to estimate time)
gh pr list --repo izaqyos/personal_code --state all --limit 500 | wc -l

# 3. Run the export script
python export_pr_reviews.py \
  --repo izaqyos/personal_code \
  --output ../data/pr_reviews/ \
  --limit 100 \
  --training-format

# 4. Review the output
ls -la ../data/pr_reviews/
cat ../data/pr_reviews/pr_reviews_training.json | head -100
```

### What Gets Exported

The script extracts:
1. **PR metadata**: title, description, author, date
2. **Review comments**: inline code comments with the diff context
3. **Review decisions**: approved, changes requested, etc.

Each review comment becomes a training example:
```json
{
  "instruction": "Review this code change in src/utils.js:",
  "input": "@@ -10,6 +10,8 @@\n function getData() {\n+  const result = fetch(url);\n+  return result;\n }",
  "output": "This looks good, but you should await the fetch call since it returns a Promise.",
  "category": "code_review",
  "source": "pr_review"
}
```

### If You Have Few/No PRs

If your personal repo has limited PR history, that's okay! The main training data will come from:
- **M3: Cursor-generated Q&A** (primary source)
- **M1: Collected code** (used as input for Q&A generation)

PR reviews are supplementary high-quality data, not required.

### Success Criteria
- [ ] GitHub CLI authenticated successfully
- [ ] Script runs without authentication errors
- [ ] Output files created (even if small)
- [ ] Training format JSON is valid

---

## M3: Generate Q&A Dataset Using Cursor

### Objective
Create high-quality instruction-tuning data by using Cursor AI to generate Q&A pairs from your codebase.

### Details

| Field | Value |
|-------|-------|
| **Owner** | **YOU** (using Cursor AI as assistant) |
| **Input** | Your code files + `example_dataset.json` as template |
| **Output** | `data/training/cursor_generated.json` (100+ examples) |
| **Dependencies** | M1 completed (to know which files to use) |
| **Est. Time** | 2-4 hours (can be done in sessions) |

### Why This Step Requires You

Cursor can help generate Q&A pairs, but YOU need to:
1. Select interesting/representative code files
2. Guide the types of questions to generate
3. Review and approve the quality
4. Ensure the output matches your coding style

### Step-by-Step Cursor Instructions

#### Setup (5 min)
```
1. Open Cursor IDE
2. Open folder: /Users/yosii/work/git/personal_code
3. Have this file open for reference:
   code/AI/projects/finetune/data/training/example_dataset.json
```

#### Phase 1: Code Review Q&A (30-45 min for 30 examples)

**Step 1.1**: Find an interesting file
```
Navigate to: code/nodejs/examples/ or code/python/snippets/
Pick a file with 50-200 lines of meaningful code
```

**Step 1.2**: Select a function or code block (highlight it)

**Step 1.3**: Prompt Cursor (Cmd+K or Ctrl+K):
```
Generate a code review training example for fine-tuning an LLM.

Format the output as JSON matching this schema:
{
  "instruction": "Review this [language] code for potential issues",
  "input": "[the selected code]",
  "output": "[detailed review covering: bugs, security, performance, best practices]",
  "category": "code_review",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

Make the review thorough but constructive. Include:
- At least 2-3 specific observations
- Code suggestions where relevant
- Explanation of WHY something is an issue
```

**Step 1.4**: Review the output
- Is the review accurate?
- Would you give similar feedback?
- Edit if needed, then save

**Step 1.5**: Repeat for different code patterns:
- Error handling code
- API/fetch calls
- Database queries
- Authentication logic
- Utility functions
- React/frontend components (if any)

#### Phase 2: Explain Code Q&A (30-45 min for 30 examples)

**Step 2.1**: Find code with interesting patterns
```
Look for:
- Design patterns (factory, singleton, observer)
- Complex algorithms
- Async/await patterns
- Decorators or middleware
- Data transformations
```

**Step 2.2**: Prompt Cursor:
```
Generate an "explain code" training example for fine-tuning.

Format as JSON:
{
  "instruction": "Explain what this [language] code does and how it works",
  "input": "[the selected code]",
  "output": "[clear explanation including: purpose, how it works step-by-step, when to use it, any caveats]",
  "category": "explain_code",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}

The explanation should be:
- Clear enough for a junior developer
- Include the "why" not just the "what"
- Mention any edge cases or gotchas
```

#### Phase 3: Improvement Suggestions (20-30 min for 20 examples)

**Step 3.1**: Find code that could be better (we all have some!)

**Step 3.2**: Prompt Cursor:
```
Generate a "suggest improvements" training example.

Format as JSON:
{
  "instruction": "How would you improve this [language] code?",
  "input": "[the selected code]",
  "output": "[specific improvements with: what to change, why, and example refactored code]",
  "category": "suggest_improvements",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}
```

#### Phase 4: Debugging Q&A (20-30 min for 20 examples)

**Step 4.1**: Find code with potential bugs OR intentionally introduce a bug

**Step 4.2**: Prompt Cursor:
```
Generate a "find the bug" training example.

Format as JSON:
{
  "instruction": "Find and fix the bug in this [language] code",
  "input": "[code with bug]",
  "output": "[identify the bug, explain why it's a bug, provide the fix]",
  "category": "debugging",
  "language": "[javascript/python]",
  "source": "cursor",
  "quality": "high"
}
```

### Compiling Your Dataset

After generating examples in Cursor, compile them:

```bash
# Create the output file manually or use a script
# Save all your JSON examples to: data/training/cursor_generated.json

# The file should look like:
{
  "version": "1.0.0",
  "metadata": {
    "created_at": "2026-01-07T...",
    "source": "cursor",
    "total_examples": 100
  },
  "data": [
    { "instruction": "...", "input": "...", "output": "...", ... },
    { "instruction": "...", "input": "...", "output": "...", ... }
  ]
}
```

### Tips for Quality

1. **Variety**: Mix different file types, patterns, languages
2. **Length**: Outputs should be 100-500 words (not too short, not too long)
3. **Accuracy**: Verify the explanations/reviews are correct
4. **Style**: Match how YOU would explain code to a colleague
5. **Balance**: Aim for ~30% review, 30% explain, 20% improve, 20% debug

### Success Criteria
- [ ] 100+ examples generated
- [ ] Mix of categories (review, explain, improve, debug)
- [ ] Both JavaScript and Python represented
- [ ] JSON is valid and matches schema
- [ ] Examples are high quality (you'd be happy receiving this feedback)

---

## M4: Run Baseline Evaluation

### Objective
Test the BASE model (before fine-tuning) to establish what it can/cannot do. This gives us a comparison point.

### Details

| Field | Value |
|-------|-------|
| **Owner** | **YOU** (running commands + recording results) |
| **Input** | `evaluation/eval_prompts.json`, Ollama + base model |
| **Output** | `evaluation/baseline_results.json` |
| **Dependencies** | Ollama installed, base model downloaded |
| **Est. Time** | 1-2 hours |

### Prerequisites

```bash
# 1. Install Ollama
brew install ollama

# 2. Start Ollama service (runs in background)
ollama serve &

# 3. Download the base model (this takes a few minutes, ~4GB)
ollama pull qwen2.5-coder:7b-instruct

# 4. Verify it works
ollama run qwen2.5-coder:7b-instruct "What is a closure in JavaScript?"
# Should give a reasonable answer
```

### Step-by-Step Evaluation Process

**Step 1**: Open the eval prompts file
```bash
cat /Users/yosii/work/git/personal_code/code/AI/projects/finetune/evaluation/eval_prompts.json
```

**Step 2**: For each prompt, test the base model

```bash
# Interactive mode - paste prompts one by one
ollama run qwen2.5-coder:7b-instruct

# Or use the API for scripting
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b-instruct",
  "prompt": "Review this JavaScript function for potential issues:\n\nasync function fetchUserData(userId) {\n  const response = await fetch(`/api/users/${userId}`);\n  const data = response.json();\n  return data;\n}",
  "stream": false
}'
```

**Step 3**: Score each response using the criteria in `eval_prompts.json`:

| Score | Meaning |
|-------|---------|
| 5 | Excellent - covers all expected points + extras |
| 4 | Good - covers most expected points |
| 3 | Acceptable - covers some points |
| 2 | Poor - misses major issues |
| 1 | Unacceptable - wrong or unhelpful |

**Step 4**: Record results

Create `evaluation/baseline_results.json`:
```json
{
  "model": "qwen2.5-coder:7b-instruct",
  "evaluated_at": "2026-01-07",
  "evaluator": "yosii",
  "results": [
    {
      "prompt_id": "explain_001",
      "score": 4,
      "response": "[paste the model's response]",
      "notes": "Correctly explained debouncing, missed mentioning 'this' context binding"
    },
    {
      "prompt_id": "review_001",
      "score": 3,
      "response": "[paste response]",
      "notes": "Caught missing await, but didn't mention response.ok check"
    }
  ],
  "summary": {
    "average_score": 3.5,
    "strengths": ["Good at explaining concepts", "Catches obvious bugs"],
    "weaknesses": ["Misses security issues", "Generic suggestions"]
  }
}
```

### What to Look For

When evaluating, note:
1. **Does it understand the code?** (basic comprehension)
2. **Does it catch the expected issues?** (per eval_prompts.json)
3. **Are suggestions actionable?** (specific vs generic)
4. **Is the tone appropriate?** (professional, constructive)
5. **Does it hallucinate?** (makes up facts about the code)

### Why This Matters

After fine-tuning, you'll run the SAME evaluation. Improvements should show:
- Higher average scores
- Better on YOUR specific code patterns
- More relevant/specific suggestions
- Familiarity with your codebase style

### Success Criteria
- [ ] Ollama installed and running
- [ ] Base model downloaded and responding
- [ ] All 10 eval prompts tested
- [ ] Results recorded in baseline_results.json
- [ ] Summary of strengths/weaknesses documented

---

## M5: First Training Run (Validation)

### Objective
Run a quick training with a small dataset to verify the setup works before committing to overnight training.

### Details

| Field | Value |
|-------|-------|
| **Owner** | Python Script + MLX + **YOU** (monitoring) |
| **Input** | 100 training examples from M3 |
| **Output** | LoRA adapter weights in `models/finetuned/test_run/` |
| **Dependencies** | M3 completed (dataset), M4 completed (baseline) |
| **Est. Time** | 30-60 minutes |

### Prerequisites

```bash
# Install dependencies
cd /Users/yosii/work/git/personal_code/code/AI/projects/finetune
pip install -r requirements.txt

# Verify MLX works
python -c "import mlx; print('MLX OK')"
```

### Instructions

*Detailed training script to be created in next session*

### Success Criteria
- [ ] Training starts without errors
- [ ] Loss decreases over steps
- [ ] Checkpoint saved successfully
- [ ] Model can be loaded and generates text

---

## M6: Evaluate Fine-Tuned Model

### Objective
Test the fine-tuned model with the same prompts as baseline to measure improvement.

### Details

| Field | Value |
|-------|-------|
| **Owner** | **YOU** |
| **Input** | Fine-tuned model, `eval_prompts.json` |
| **Output** | `evaluation/finetuned_results.json` |
| **Dependencies** | M5 completed |
| **Est. Time** | 1-2 hours |

### Process
Same as M4, but with fine-tuned model.

---

## M7: Full Training Run

### Objective
Train on the complete dataset overnight.

### Details

| Field | Value |
|-------|-------|
| **Owner** | Python Script (running overnight) |
| **Input** | Full dataset (500+ examples) |
| **Output** | Final LoRA adapter |
| **Dependencies** | M5 successful, M6 shows improvement |
| **Est. Time** | 8-18 hours (overnight) |

---

## M8: Deploy to Ollama

### Objective
Export the model and deploy for daily use.

### Details

| Field | Value |
|-------|-------|
| **Owner** | **YOU** + conversion scripts |
| **Input** | Trained LoRA adapter |
| **Output** | Ollama model ready to use |
| **Dependencies** | M7 completed, M6 shows good results |
| **Est. Time** | 1-2 hours |

---

## Quick Reference: Milestone Summary

| # | Milestone | Owner | Time | Status |
|---|-----------|-------|------|--------|
| M1 | Collect Code | Script | 5 min | ⬜ Not Started |
| M2 | Export PR Reviews | Script + gh | 15 min | ⬜ Not Started |
| M3 | Generate Q&A (Cursor) | **YOU** | 2-4 hrs | ⬜ Not Started |
| M4 | Baseline Evaluation | **YOU** | 1-2 hrs | ⬜ Not Started |
| M5 | First Training Run | Script | 30-60 min | ⬜ Not Started |
| M6 | Evaluate Fine-Tuned | **YOU** | 1-2 hrs | ⬜ Not Started |
| M7 | Full Training | Script | Overnight | ⬜ Not Started |
| M8 | Deploy to Ollama | **YOU** + Script | 1-2 hrs | ⬜ Not Started |

---

## Recommended Order

```
Day 1 (Setup):
  └── M1 (5 min) → M2 (15 min) → Start M3

Day 2 (Data Generation):
  └── Continue M3 → M4 (parallel if model downloaded)

Day 3 (First Training):
  └── M5 → M6 → Iterate if needed

Day 4 (Full Training):
  └── M7 (start before bed)

Day 5 (Deploy):
  └── M6 (final eval) → M8
```

---

*Update this document as you complete each milestone!*
