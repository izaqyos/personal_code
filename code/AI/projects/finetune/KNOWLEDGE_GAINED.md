# Knowledge Gained: LLM Fine-Tuning Project

> **Purpose**: Document key learnings to retain knowledge and teach other developers
> **Last Updated**: 2026-01-07

---

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Model Selection](#model-selection)
3. [Training Techniques](#training-techniques)
4. [Data Preparation](#data-preparation)
5. [Local Training on Apple Silicon](#local-training-on-apple-silicon)
6. [Deployment](#deployment)
7. [Lessons Learned](#lessons-learned)
8. [Common Pitfalls](#common-pitfalls)
9. [Resources](#resources)

---

## Core Concepts

### What is Fine-Tuning?
Fine-tuning adapts a pre-trained LLM to perform better on specific tasks or domains by training it further on your own data.

```
Pre-trained Model (general knowledge)
        ↓
    Fine-tuning (your data)
        ↓
Specialized Model (your domain expertise)
```

### Types of Fine-Tuning

| Type | Description | When to Use |
|------|-------------|-------------|
| **Full Fine-tuning** | Update all model weights | Maximum customization, needs lots of compute |
| **LoRA** | Train small adapter layers | Good balance of quality and efficiency |
| **QLoRA** | LoRA + quantization | Best for limited hardware (our choice) |
| **Prompt Tuning** | Only tune soft prompts | Minimal changes, quick experiments |

### Key Terms Glossary

| Term | Definition |
|------|------------|
| **LoRA** | Low-Rank Adaptation - trains small matrices that modify model behavior |
| **QLoRA** | Quantized LoRA - uses 4-bit quantization to reduce memory |
| **Quantization** | Reducing precision (32-bit → 4-bit) to save memory |
| **GGUF** | File format for quantized models (used by Ollama) |
| **Adapter** | Small trained layers added to frozen base model |
| **Rank (r)** | LoRA parameter controlling adapter size (higher = more capacity) |
| **Alpha** | LoRA scaling factor (typically 2x rank) |

---

## Model Selection

### Key Factors for Choosing a Model

1. **Size vs Hardware**: Must fit in available RAM
   - 7B model in 4-bit ≈ 4-5GB VRAM/RAM
   - Rule: Model size in 4-bit ≈ (params in B) × 0.5-0.7 GB

2. **Base vs Instruct**:
   - Base models: better for continued pre-training
   - Instruct models: better for chat/instruction following (our use case)

3. **License**: Check commercial use is allowed
   - Apache 2.0, MIT: Generally safe
   - Llama license: Check restrictions

4. **Training Data Quality**: Code-specific models outperform general ones for code tasks

### Why We Chose Qwen2.5-Coder-7B-Instruct

```
✅ Size: 7B fits comfortably in 48GB with QLoRA
✅ Type: Instruct-tuned for chat use case
✅ License: Apache 2.0 (permissive)
✅ Performance: Top benchmarks for code understanding
✅ Languages: Excellent JS and Python support
```

---

## Training Techniques

### QLoRA Explained

QLoRA combines two techniques:
1. **Quantization**: Load base model in 4-bit to save memory
2. **LoRA**: Train small adapter matrices (not the whole model)

```
Memory Comparison (7B model):
- Full fine-tuning: ~56GB (won't fit)
- LoRA (16-bit): ~28GB (tight)
- QLoRA (4-bit): ~8-12GB (comfortable) ✓
```

### Key Hyperparameters

```yaml
# These are the important knobs to tune

lora:
  r: 16              # Rank: 8-64 typical. Higher = more capacity, more memory
  alpha: 32          # Usually 2x rank. Scales the adapter contribution
  dropout: 0.05      # Regularization. 0.05-0.1 typical

training:
  learning_rate: 2e-4    # Start here, reduce if loss spikes
  batch_size: 4          # Limited by memory
  gradient_accumulation: 4  # Effective batch = batch_size × this
  epochs: 3              # 2-5 typical for fine-tuning
  warmup_ratio: 0.03     # Gradual LR increase at start
```

### What Gets Trained?

In LoRA, we only train adapters on attention layers:
- `q_proj` (query projection)
- `k_proj` (key projection)
- `v_proj` (value projection)
- `o_proj` (output projection)

The base model weights stay FROZEN. This is why it's memory efficient.

---

## Data Preparation

### The Data Quality Principle

> **"Garbage in, garbage out"** - Data quality matters more than quantity

### Our Data Strategy

| Source | Type | Quality | Notes |
|--------|------|---------|-------|
| PR Reviews | Real human feedback | High | Gold standard |
| Knowledge Base | Documentation | High | Team-specific patterns |
| Cursor-generated | Synthetic Q&A | Medium | Scale with quality |
| Manual curation | Golden examples | Highest | Benchmark set |

### Dataset Format (Alpaca-style)

```json
{
  "instruction": "What does this function do?",
  "input": "function calculateTotal(items) {\n  return items.reduce((sum, item) => sum + item.price, 0);\n}",
  "output": "This function calculates the total price of all items in an array. It uses reduce() to iterate through each item and sum up their price properties, starting from 0."
}
```

### Data Quality Checklist

- [ ] No sensitive data (API keys, passwords, PII)
- [ ] Code is syntactically valid
- [ ] Responses are accurate and helpful
- [ ] Consistent formatting across examples
- [ ] Variety of question types
- [ ] Representative of actual use cases

---

## Local Training on Apple Silicon

### Why MLX?

MLX is Apple's framework optimized for Apple Silicon:
- Native Metal GPU acceleration
- Unified memory (CPU/GPU share RAM)
- Designed for ML workloads on Mac

```bash
# Install MLX ecosystem
pip install mlx mlx-lm
```

### Memory Management on M4

```
48GB Unified Memory Budget:
├── macOS overhead: ~4-6GB
├── Model (7B, 4-bit): ~4-5GB
├── Training state: ~8-12GB
├── Gradients/optimizer: ~8-10GB
└── Buffer: ~15GB headroom ✓
```

### Training Time Expectations

| Model | Method | Dataset Size | Approx Time |
|-------|--------|--------------|-------------|
| 3B | QLoRA | 1000 samples | 2-3 hours |
| 7B | QLoRA | 1000 samples | 6-8 hours |
| 7B | QLoRA | 5000 samples | 12-18 hours |

### Tips for Overnight Runs

1. **Prevent sleep**: `caffeinate -i python train.py`
2. **Save checkpoints**: Every N steps, save adapter weights
3. **Log to file**: Capture stdout/stderr for debugging
4. **Monitor**: Use `htop` or Activity Monitor

---

## Deployment

### Export Pipeline

```
Trained Adapter (LoRA weights)
        ↓
Merge with Base Model
        ↓
Convert to GGUF Format
        ↓
Load into Ollama
```

### Ollama Modelfile

```dockerfile
FROM ./model-q4_k_m.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

SYSTEM """You are a code assistant trained on our team's codebase.
You help with code review, explaining code, and answering questions
about our JavaScript and Python projects."""
```

### Quantization Options

| Format | Size | Quality | Speed |
|--------|------|---------|-------|
| Q4_K_M | Smallest | Good | Fastest |
| Q5_K_M | Medium | Better | Fast |
| Q6_K | Larger | Best | Slower |
| Q8_0 | Largest | Near-original | Slowest |

**Recommendation**: Start with Q4_K_M, upgrade if quality insufficient.

---

## Lessons Learned

> This section will be updated as we progress through the project

### Session 1: Brainstorming (2026-01-06)
- **Model Selection**: For local M4 training, 7B models with QLoRA are the sweet spot
- **Instruct vs Base**: Use instruct-tuned models for chat/review use cases
- **Memory Rule**: QLoRA 4-bit needs ~1.5x model size in GB for training

### Session 2: Planning & Setup (2026-01-07)
- **Data Strategy Pivot**: Personal code repos are better for public projects (no IP concerns)
- **Real vs Synthetic Data**: PR reviews provide real human feedback (higher quality than pure synthetic)
- **Cursor for Data Gen**: AI-assisted dataset creation is practical - generate Q&A from real code
- **Dataset Quality**: 80 high-quality examples > 150 mediocre ones
- **Variety Matters**: Mix categories (review, explain, improve, debug) for well-rounded model

---

## Common Pitfalls

### 1. Training Data Issues
- **Problem**: Model outputs nonsense or repeats training data
- **Cause**: Dataset too small, low quality, or overfit
- **Solution**: More diverse data, fewer epochs, add regularization

### 2. Memory Errors
- **Problem**: OOM during training
- **Cause**: Batch size too large, sequence too long
- **Solution**: Reduce batch_size, use gradient accumulation

### 3. Loss Not Decreasing
- **Problem**: Training loss stays flat
- **Cause**: Learning rate too low, or data issue
- **Solution**: Increase LR, check data format

### 4. Model Forgets Base Knowledge
- **Problem**: Loses general abilities after fine-tuning
- **Cause**: Trained too long, LR too high
- **Solution**: Fewer epochs, lower LR, use LoRA (preserves base)

### 5. Inconsistent Outputs
- **Problem**: Same prompt gives wildly different answers
- **Cause**: Temperature too high, model undertrained
- **Solution**: Lower temperature, more training data

---

## Resources

### Essential Reading
- [QLoRA Paper](https://arxiv.org/abs/2305.14314) - The technique we're using
- [LoRA Paper](https://arxiv.org/abs/2106.09685) - Foundation of adapter training
- [MLX Documentation](https://ml-explore.github.io/mlx/) - Apple's ML framework

### Tools Documentation
- [Hugging Face PEFT](https://huggingface.co/docs/peft) - LoRA implementation
- [Ollama](https://ollama.ai/) - Local model serving
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - GGUF conversion

### Community Resources
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA) - Community for local LLM running
- [Hugging Face Hub](https://huggingface.co/models) - Model repository

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                 LLM FINE-TUNING CHEAT SHEET             │
├─────────────────────────────────────────────────────────┤
│ TRAINING COMMAND (example):                             │
│   python train.py --model Qwen2.5-Coder-7B-Instruct    │
│                   --method qlora                        │
│                   --data ./data/training/dataset.json   │
│                                                         │
│ KEY HYPERPARAMETERS:                                    │
│   r=16, alpha=32, lr=2e-4, epochs=3, batch=4           │
│                                                         │
│ MEMORY RULE OF THUMB:                                   │
│   QLoRA 4-bit needs ~1.5x model size in GB             │
│   7B model → ~10-12GB training memory                  │
│                                                         │
│ DEPLOYMENT:                                             │
│   1. Merge adapter: merge_lora.py                       │
│   2. Convert: llama.cpp convert.py                      │
│   3. Deploy: ollama create mymodel -f Modelfile         │
└─────────────────────────────────────────────────────────┘
```

---

*This document is a living resource. Update it as you learn!*
