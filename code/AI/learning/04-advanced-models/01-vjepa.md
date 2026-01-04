# V-JEPA: Video Joint-Embedding Predictive Architecture

> Meta's approach to learning visual representations without labeled data.

---

## Overview

V-JEPA (Video Joint-Embedding Predictive Architecture) learns video representations by predicting masked regions in a learned representation space, rather than pixel space.

```
┌─────────────────────────────────────────────────────────────┐
│                     V-JEPA Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Video ──→ Mask patches ──→ Context Encoder ──→ sₓ         │
│             (80-90%)              │                          │
│                                   │                          │
│                                   ↓                          │
│                              Predictor ──→ ŝᵧ (predictions) │
│                                                  ↕           │
│   Target ────────────────→ Target Encoder ──→ sᵧ (targets)  │
│   (full video)            (EMA of context)                  │
│                                                              │
│   Loss = ||ŝᵧ - sᵧ||²  (in embedding space, not pixels!)   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Innovation: Prediction in Latent Space

### Pixel Prediction (MAE, VideoMAE)
```
Input: Video with masked patches
Task:  Reconstruct actual RGB pixel values

Problems:
- Predicts low-level details (noise, texture)
- Uncertain regions get blurry averages
- Wastes capacity on irrelevant details
```

### Embedding Prediction (V-JEPA)
```
Input: Video with masked patches
Task:  Predict embedding of masked regions

Benefits:
- Focuses on semantic content
- Handles uncertainty gracefully
- Learns higher-level representations
- No decoder needed (simpler!)
```

```
MAE reconstruction:                V-JEPA prediction:
"What color are those pixels?"     "What concept is in that region?"

     🟥🟥⬜⬜                            [Person]    [Walking]
     🟥🟥⬜⬜         vs                    ↓            ↓
     🟦🟦🟧🟧                          [0.2, -0.3]  [0.5, 0.1]
 (pixel reconstruction)              (embedding space)
```

---

## Architecture Components

### 1. Masking Strategy

```
Spatial-temporal masking (very aggressive):

Frame 1:  ████░░░░    Frame 2:  ░░░░████    Frame 3:  ██░░██░░
          ████░░░░              ░░░░████              ██░░██░░
          ████░░░░              ░░░░████              ██░░██░░

█ = masked (80-90% of patches!)
░ = visible

Key: Use larger, contiguous blocks (not random single patches)
Forces model to learn motion and semantics, not local patterns
```

### 2. Context Encoder

```python
class ContextEncoder(nn.Module):
    """
    Standard Vision Transformer, but only sees unmasked patches.
    """
    def __init__(self, image_size, patch_size, embed_dim, depth, num_heads):
        super().__init__()
        self.patch_embed = PatchEmbed(image_size, patch_size, 3, embed_dim)
        self.pos_embed = PositionalEmbedding3D(...)  # Spatiotemporal
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads)
            for _ in range(depth)
        ])

    def forward(self, video, mask):
        # Only encode visible patches
        x = self.patch_embed(video)
        x = x[~mask]  # Select unmasked
        x = x + self.pos_embed
        for block in self.blocks:
            x = block(x)
        return x
```

### 3. Target Encoder (EMA)

```python
class TargetEncoder(nn.Module):
    """
    Same architecture as Context Encoder, but:
    - Sees ALL patches (no masking)
    - Weights are EMA of Context Encoder (no gradient)
    """
    def __init__(self, context_encoder):
        super().__init__()
        self.encoder = copy.deepcopy(context_encoder)

    @torch.no_grad()
    def update_ema(self, context_encoder, momentum=0.996):
        for param_t, param_c in zip(self.encoder.parameters(),
                                     context_encoder.parameters()):
            param_t.data = momentum * param_t.data + (1 - momentum) * param_c.data

    def forward(self, video):
        # Encode full video (no masking)
        return self.encoder(video, mask=None)
```

### 4. Predictor

```python
class Predictor(nn.Module):
    """
    Given context embeddings + mask positions,
    predict target embeddings for masked regions.
    """
    def __init__(self, embed_dim, predictor_dim, depth):
        super().__init__()
        self.mask_token = nn.Parameter(torch.zeros(1, 1, predictor_dim))
        self.proj = nn.Linear(embed_dim, predictor_dim)

        self.blocks = nn.ModuleList([
            TransformerBlock(predictor_dim, num_heads=8)
            for _ in range(depth)
        ])

        self.pred_proj = nn.Linear(predictor_dim, embed_dim)

    def forward(self, context_embed, mask):
        # Project context
        x = self.proj(context_embed)

        # Add mask tokens for positions to predict
        mask_tokens = self.mask_token.expand(batch, num_masked, -1)
        x = torch.cat([x, mask_tokens], dim=1)

        # Cross-attend
        for block in self.blocks:
            x = block(x)

        # Return predictions for masked positions
        predictions = self.pred_proj(x[:, -num_masked:])
        return predictions
```

---

## Training Procedure

```python
def train_step(video, context_encoder, target_encoder, predictor):
    # 1. Create aggressive mask (80-90% masked)
    mask = create_spatiotemporal_mask(video, ratio=0.85)

    # 2. Get context embeddings (visible patches only)
    context_embed = context_encoder(video, mask)

    # 3. Predict embeddings for masked regions
    predicted_embed = predictor(context_embed, mask)

    # 4. Get target embeddings (no gradient, full video)
    with torch.no_grad():
        target_embed = target_encoder(video)
        target_masked = target_embed[mask]  # Only masked positions

    # 5. Loss in embedding space
    loss = F.mse_loss(predicted_embed, target_masked)

    # 6. Update EMA target
    target_encoder.update_ema(context_encoder, momentum=0.996)

    return loss
```

---

## Why V-JEPA Works

### 1. Avoids Pixel-Level Uncertainty
```
Question: "What's in the masked region?"

Pixel prediction:
- Must guess exact colors
- Averages multiple possibilities → blurry result
- "A person... average skin tone, average clothes..."

Embedding prediction:
- Just needs correct semantic
- Multiple valid embeddings are similar
- "A person" (specific pixels don't matter)
```

### 2. EMA Target Provides Stability
```
Without EMA:
- Target changes every step
- Prediction chases moving target
- Can collapse (predict zeros)

With EMA:
- Target changes slowly
- Provides stable learning signal
- Momentum 0.996 = target updates ~0.4% per step
```

### 3. High Masking Ratio Forces Reasoning
```
Low masking (20%):
- Can interpolate from nearby pixels
- Learns local patterns

High masking (90%):
- Must understand what's happening
- "Person walking" requires motion understanding
- Forces semantic representations
```

---

## Comparison with Other Methods

| Method | Prediction Space | Learns From |
|--------|------------------|-------------|
| **MAE** | Pixels | Images |
| **VideoMAE** | Pixels | Video |
| **DINO** | Embedding (CLS token) | Images |
| **I-JEPA** | Embedding (patch) | Images |
| **V-JEPA** | Embedding (spatiotemporal) | Video |

---

## Results and Applications

### Downstream Tasks
```
After pretraining (no labels!), V-JEPA representations excel at:

1. Action Recognition
   - Kinetics-400: State-of-the-art
   - SSv2: Temporal reasoning benchmark

2. Video Understanding
   - Motion prediction
   - Activity detection

3. Frozen Evaluation
   - Linear probe: Just train classifier head
   - Representations are directly useful
```

### Key Findings
- Outperforms pixel-reconstruction methods
- More efficient (no decoder for reconstruction)
- Better temporal understanding
- Transfers well to downstream tasks

---

## Exercises

1. **Implement**: Build simplified V-JEPA for images (I-JEPA style)
2. **Masking**: Experiment with different masking ratios and patterns
3. **Compare**: Train MAE and V-JEPA on same data, compare representations
4. **Probe**: Train linear classifiers on frozen representations
5. **Visualize**: What do different patches' embeddings look like?

---

## Key Takeaways

- V-JEPA predicts in embedding space, not pixel space
- Avoids problems with uncertainty and low-level details
- Uses aggressive masking (80-90%) to force semantic learning
- Target encoder is EMA of context encoder (prevents collapse)
- No decoder needed - simpler and more efficient
- Learns strong video representations without labels

---

## Next Steps

→ Continue to [02-multimodal-models.md](./02-multimodal-models.md)
