# Local LLM Fine-Tuning Project Plan

> **Status**: Planning Phase → Implementation Setup
> **Last Updated**: 2026-01-07
> **Hardware**: MacBook Pro M4 (48GB RAM)

---

## Table of Contents
1. [Project Objectives](#project-objectives)
2. [Requirements Summary](#requirements-summary)
3. [Brainstorming Results](#brainstorming-results)
4. [Selected Approach](#selected-approach)
5. [Planning Phase](#planning-phase)
6. [Detailed Design](#detailed-design)
7. [Implementation](#implementation)
8. [Testing & Evaluation](#testing--evaluation)

---

## Project Objectives

### Primary
- Get hands-on experience with the LLM fine-tuning process

### Secondary
- Fine-tune a model that is fast, efficient, and low-cost
- Run locally via Ollama or Hugging Face on MacBook Pro M4
- Keep data private (team source code stays local)

---

## Requirements Summary

| Requirement | Value |
|-------------|-------|
| Hardware | MacBook Pro M4, 48GB RAM |
| Languages in Codebase | JavaScript (primary), Python (secondary) |
| Codebase Size | ~10,294 source files (personal_code repo) |
| Data Source | `/Users/yosii/work/git/personal_code` |
| GitHub Repo | `izaqyos/personal_code` |
| Primary Use Case | Chat about code, code review |
| Training Location | Local (overnight runs) |
| Inference Runtime | Ollama or Hugging Face |
| Privacy | Must be fully local/private |

---

## Brainstorming Results

### Models Evaluated

#### Tier 1: Smaller Models (2-4B) - Fastest Training & Inference
| Model | Size | License | Strengths |
|-------|------|---------|-----------|
| Qwen2.5-Coder | 1.5B, 3B | Apache 2.0 | Best-in-class for size |
| Phi-3-mini | 3.8B | MIT | Efficient, great reasoning |
| CodeGemma | 2B | Apache 2.0 | Google's code-specific model |
| DeepSeek-Coder | 1.3B | MIT | Purpose-built for code |

#### Tier 2: Optimal Balance (7-8B) - Good Speed on M4
| Model | Size | License | Strengths |
|-------|------|---------|-----------|
| Qwen2.5-Coder | 7B | Apache 2.0 | Top performer, multilingual |
| DeepSeek-Coder-V2-Lite | 2.4B active (MoE) | MIT | Fast MoE architecture |
| CodeGemma | 7B | Apache 2.0 | Strong code completion |
| StarCoder2 | 3B, 7B | OpenRAIL | Trained on permissive code |

#### Tier 3: Maximum Capability (with quantization)
| Model | Size | Notes |
|-------|------|-------|
| CodeLlama | 7B, 13B | Q4 quantization works on M4 |
| Mistral 7B | 7B | General purpose, strong coder |

### Training Time Estimates (Local M4, 48GB RAM)

| Model Size | Training Method | Est. Time | Feasibility |
|------------|-----------------|-----------|-------------|
| 1.3-3B | QLoRA 4-bit | 4-8 hours | Easy |
| 7B | QLoRA 4-bit | 12-24 hours | Overnight |
| 13B | QLoRA 4-bit | 36-48 hours | Weekend run |

### Local Training Tools
- **MLX + mlx-lm**: Apple's native framework, fastest on Apple Silicon
- **Unsloth**: Experimental MLX support, great optimizations
- **Hugging Face + PEFT**: Works but slower than MLX

---

## Selected Approach

### Recommended Model (Primary)
**Qwen2.5-Coder-7B-Instruct**
- Best overall for chat about code
- Instruct-tuned base = better conversations
- Excellent JS/Python support
- Estimated training: 12-18 hours on M4

### Backup Options
1. **DeepSeek-Coder-6.7B-Instruct** - Strong alternative, MIT license
2. **Qwen2.5-Coder-3B-Instruct** - For faster iteration (4-6 hour trains)

### Training Method
- **QLoRA (4-bit quantization)** with LoRA adapters
- Memory efficient, fits in 48GB RAM
- Can train 7B models overnight

### Deployment Target
- **Ollama** for easy local serving
- Export to **GGUF** format for compatibility

---

## Planning Phase

### Phase 1: Data Preparation Pipeline
> Transform 2.5M lines of raw code into conversational training data

#### 1.1 Data Collection
- [ ] Inventory all repositories to include
- [ ] Identify file types and languages
- [ ] Exclude sensitive files (credentials, secrets, .env)
- [ ] Exclude generated/vendor code (node_modules, dist, etc.)

#### 1.2 Data Cleaning
- [ ] Remove binary files
- [ ] Filter out minified code
- [ ] Handle duplicate/similar files
- [ ] Normalize formatting

#### 1.3 Dataset Generation Strategy (DECIDED)

**Approach**: Leverage existing assets + Cursor AI assistance

**Data Sources:**
1. **PR Code Reviews** - Real review comments from team PRs (high quality)
2. **Knowledge Base** - Existing documentation and tribal knowledge
3. **Cursor-Assisted Generation** - Use Cursor to generate Q&A from code

**Why this approach works:**
- PR reviews are REAL human feedback, not synthetic
- Knowledge base captures team-specific patterns and decisions
- Cursor can help scale Q&A generation while maintaining quality
- Combines automated generation with human-curated examples

```
Data Sources → Training Data:
├── PR Reviews      → Code review Q&A pairs
├── Knowledge Base  → "How does X work?" pairs
├── Cursor + Code   → Explanation & analysis pairs
└── Manual Curation → High-quality golden examples
```

**Generation Workflow:**
1. Export PR review comments with associated code diffs
2. Convert knowledge base docs to Q&A format
3. Use Cursor to generate additional Q&A from key files
4. Manually curate ~100 "golden" examples for quality baseline

#### 1.4 Dataset Format
Target format for instruction tuning:
```json
{
  "instruction": "Review this JavaScript function for potential issues",
  "input": "function fetchData(url) { ... }",
  "output": "This function has several concerns: 1) No error handling..."
}
```

### Phase 2: Environment Setup

#### 2.1 Dependencies
```bash
# Core ML frameworks for Apple Silicon
pip install mlx mlx-lm

# Hugging Face ecosystem
pip install transformers datasets peft accelerate

# Quantization and optimization
pip install bitsandbytes scipy

# Ollama (for deployment)
brew install ollama
```

#### 2.2 Model Download
```bash
# Using Hugging Face CLI
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct

# Or via MLX
mlx_lm.convert --hf-path Qwen/Qwen2.5-Coder-7B-Instruct
```

#### 2.3 Directory Structure
```
finetune/
├── FINETUNE_PROJECT_PLAN.md   # Project plan (this file)
├── KNOWLEDGE_GAINED.md        # Learning documentation for teaching others
├── data/
│   ├── raw/                   # Raw code from repos
│   │   └── .gitkeep
│   ├── pr_reviews/            # Exported PR review data
│   │   └── .gitkeep
│   ├── knowledge_base/        # Team knowledge docs
│   │   └── .gitkeep
│   ├── processed/             # Cleaned/processed code
│   │   └── .gitkeep
│   └── training/              # Final training datasets
│       ├── .gitkeep
│       └── schema.json        # Dataset format specification
├── scripts/
│   ├── collect_code.py        # Gather code from repos
│   ├── export_pr_reviews.py   # Export PR reviews from GitHub
│   ├── generate_qa.py         # Create Q&A pairs
│   ├── prepare_dataset.py     # Format for training
│   └── validate_dataset.py    # Validate dataset quality
├── training/
│   ├── config.yaml            # Training hyperparameters
│   └── train.py               # Training script
├── models/
│   ├── base/                  # Downloaded base model
│   │   └── .gitkeep
│   └── finetuned/             # Output adapter/model
│       └── .gitkeep
├── evaluation/
│   ├── eval_prompts.json      # Test prompts for evaluation
│   ├── baseline_results.json  # Pre-finetune results
│   └── finetuned_results.json # Post-finetune results
└── experiments/               # Experiment tracking
    └── .gitkeep
```

### Phase 3: Fine-Tuning Strategy

#### 3.1 Training Configuration (QLoRA)
```yaml
# Suggested starting hyperparameters
model: Qwen/Qwen2.5-Coder-7B-Instruct
method: qlora
quantization: 4bit

lora:
  r: 16                    # LoRA rank
  alpha: 32                # LoRA alpha
  dropout: 0.05
  target_modules:          # Layers to adapt
    - q_proj
    - k_proj
    - v_proj
    - o_proj

training:
  epochs: 3
  batch_size: 4
  gradient_accumulation: 4
  learning_rate: 2e-4
  warmup_ratio: 0.03
  max_seq_length: 2048

optimization:
  optimizer: adamw_8bit
  scheduler: cosine
```

#### 3.2 Training Phases
1. **Phase A**: Quick test run (100 samples, 1 epoch) - ~30 min
2. **Phase B**: Small scale validation (1000 samples, 2 epochs) - ~2 hours
3. **Phase C**: Full training (all data, 3 epochs) - overnight

### Phase 4: Evaluation Approach

#### 4.1 Qualitative Tests
- [ ] Can it explain functions from the codebase?
- [ ] Does it understand project-specific patterns?
- [ ] Are code review suggestions relevant?
- [ ] Does it know about internal APIs/modules?

#### 4.2 Test Prompts (to create)
```json
[
  {"type": "explain", "prompt": "Explain what the AuthService class does"},
  {"type": "review", "prompt": "Review this PR for potential issues: ..."},
  {"type": "locate", "prompt": "Where is user authentication handled?"},
  {"type": "suggest", "prompt": "How could we improve error handling in..."}
]
```

#### 4.3 Comparison Baseline
- Test same prompts on base model (before fine-tuning)
- Test on fine-tuned model
- Document improvements

### Phase 5: Deployment

#### 5.1 Export to GGUF (for Ollama)
```bash
# Convert to GGUF format
python convert.py --outtype q4_k_m

# Create Ollama modelfile
ollama create team-coder -f Modelfile
```

#### 5.2 Modelfile Template
```dockerfile
FROM ./model-q4_k_m.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9

SYSTEM """You are a code assistant specialized in our team's codebase.
You help with code review, explaining code, and answering questions
about our JavaScript and Python projects."""
```

#### 5.3 Usage
```bash
# Start local server
ollama serve

# Chat with model
ollama run team-coder "Explain how our authentication flow works"
```

---

## Detailed Design

### Data Pipeline Design (COMPLETED)
- [x] Code collection script: `scripts/collect_code.py`
- [x] PR review export script: `scripts/export_pr_reviews.py`
- [x] Dataset schema: `data/training/schema.json`
- [x] Example dataset: `data/training/example_dataset.json`

### Baseline Testing Approach

**Purpose**: Establish what the base model can/cannot do BEFORE fine-tuning.

**Process:**
1. Download base model (Qwen2.5-Coder-7B-Instruct)
2. Run evaluation prompts (`evaluation/eval_prompts.json`)
3. Score responses using evaluation criteria
4. Document results in `evaluation/baseline_results.json`

**Commands to run baseline:**
```bash
# Install Ollama and pull base model
brew install ollama
ollama pull qwen2.5-coder:7b-instruct

# Run interactive test
ollama run qwen2.5-coder:7b-instruct

# Or use the evaluation script (to be created)
python scripts/evaluate_model.py --model qwen2.5-coder:7b-instruct --output evaluation/baseline_results.json
```

**What to measure:**
- Can it explain code accurately?
- Does it catch security issues in reviews?
- Are suggestions practical and relevant?
- Does it understand JavaScript/Python idioms?

### Training Pipeline Design
- **Framework**: MLX (Apple Silicon optimized) as primary, HuggingFace as fallback
- **Checkpoint strategy**: Save every 500 steps + end of each epoch
- **Resume capability**: Built into MLX training loop

---

## Implementation

### Project Structure (COMPLETED)
```
finetune/
├── FINETUNE_PROJECT_PLAN.md   ✅
├── KNOWLEDGE_GAINED.md        ✅
├── requirements.txt           ✅
├── data/
│   ├── raw/                   ✅
│   ├── pr_reviews/            ✅
│   ├── knowledge_base/        ✅
│   ├── processed/             ✅
│   └── training/
│       ├── schema.json        ✅
│       └── example_dataset.json ✅
├── scripts/
│   ├── collect_code.py        ✅
│   └── export_pr_reviews.py   ✅
├── models/                    ✅
├── evaluation/
│   └── eval_prompts.json      ✅
└── experiments/               ✅
```

### Implementation Checklist
- [x] Set up project structure
- [x] Implement data collection scripts
- [ ] Generate training dataset (YOUR TASK: use Cursor + PR reviews)
- [ ] Run baseline evaluation
- [ ] Configure training environment
- [ ] Run training
- [ ] Export model
- [ ] Deploy to Ollama

---

## Testing & Evaluation

> TO BE COMPLETED AFTER IMPLEMENTATION

### Results Log
| Date | Model | Dataset Size | Training Time | Notes |
|------|-------|--------------|---------------|-------|
| | | | | |

---

## Notes & Decisions Log

### 2026-01-06 - Initial Brainstorming
- Decided on Qwen2.5-Coder-7B-Instruct as primary model
- Confirmed local training is feasible on M4 with 48GB RAM
- Key challenge identified: creating conversational dataset from raw code
- Training method: QLoRA 4-bit for memory efficiency

### 2026-01-07 - Data Strategy & Project Setup
- **Data Strategy Decided**: Use PR code reviews + knowledge base + Cursor-assisted generation
- Advantage: PR reviews are REAL human feedback, not purely synthetic
- Created full project directory structure
- Added KNOWLEDGE_GAINED.md for learning documentation
- Goal: Document learnings to teach other developers

### 2026-01-07 - Pivot to Personal Code
- **Data Source Changed**: Using `personal_code` repo instead of team repos (IP concerns)
- Repo: `/Users/yosii/work/git/personal_code` (~10,294 source files)
- GitHub: `izaqyos/personal_code` (public-safe)
- Created detailed MILESTONES.md with step-by-step instructions
- Each milestone has: objective, input, output, dependencies, owner

---

## Resources & References

### Documentation
- [MLX Documentation](https://ml-explore.github.io/mlx/)
- [Qwen2.5-Coder](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
- [PEFT/LoRA Guide](https://huggingface.co/docs/peft)
- [Ollama](https://ollama.ai/)

### Tutorials
- MLX Fine-tuning: https://github.com/ml-explore/mlx-examples/tree/main/llms
- QLoRA Paper: https://arxiv.org/abs/2305.14314

---

## Next Steps

### Immediate (Your Tasks)
1. **Generate Q&A dataset using Cursor**
   - Open your repos in Cursor
   - Use PR review history to create code_review Q&A pairs
   - Use knowledge base docs to create explain_code Q&A pairs
   - Target: 100+ high-quality examples for first training run

2. **Export PR reviews from GitHub**
   ```bash
   cd scripts
   python export_pr_reviews.py --repo your-org/your-repo --training-format --output ../data/pr_reviews/
   ```

3. **Run baseline evaluation**
   ```bash
   ollama pull qwen2.5-coder:7b-instruct
   ollama run qwen2.5-coder:7b-instruct
   # Test with prompts from evaluation/eval_prompts.json
   ```

### After Data is Ready
4. **Validate dataset** - Check format, quality, no sensitive data
5. **First training run** - 100 samples, 1 epoch (~30 min) to verify setup
6. **Iterate** - Adjust hyperparameters based on results

### Future Sessions
7. **Full training run** - All data, 3 epochs (overnight)
8. **Evaluation** - Compare against baseline
9. **Deployment** - Export to GGUF, deploy to Ollama

---

*This document will be updated as the project progresses.*
