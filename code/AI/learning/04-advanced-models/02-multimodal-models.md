# Multimodal Models

> AI systems that understand and generate across multiple modalities: text, images, audio, video.

---

## Overview

Multimodal models bridge different types of data, enabling tasks like:
- Image captioning
- Visual question answering
- Text-to-image generation
- Audio-visual understanding

```
┌─────────────────────────────────────────────────────────────┐
│                    Multimodal AI                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Image ─┐                                                   │
│          │                                                   │
│   Text  ─┼──→ Multimodal Model ──→ Understanding/Generation │
│          │                                                   │
│   Audio ─┘                                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Approaches

### 1. Early Fusion

Combine modalities at input level:

```
     Image         Text
       │            │
       ↓            ↓
   [Patches]    [Tokens]
       │            │
       └────┬───────┘
            ↓
     Combined Sequence
            ↓
      Transformer
            ↓
        Output

Example: ViT + Text tokens concatenated
```

### 2. Late Fusion

Process separately, combine later:

```
   Image              Text
     │                  │
     ↓                  ↓
Vision Encoder    Text Encoder
     │                  │
     ↓                  ↓
  Features          Features
     │                  │
     └────────┬─────────┘
              ↓
         Fusion Layer
              ↓
           Output

Example: CLIP (contrastive learning)
```

### 3. Cross-Attention Fusion

Modalities attend to each other:

```
   Image              Text
     │                  │
     ↓                  ↓
Vision Encoder    Text Decoder
     │                  │
     └──────────→ Cross-Attention
                        │
                        ↓
                    Generation

Example: Flamingo, LLaVA
```

---

## CLIP: Contrastive Language-Image Pretraining

OpenAI's foundational vision-language model:

```
                Image Encoder          Text Encoder
                     │                      │
                     ↓                      ↓
Image ──→ ViT ──→ [CLS] embed    "a dog" ──→ Transformer ──→ [EOS] embed
                     │                      │
                     └──────────────────────┘
                              │
                              ↓
                    Contrastive Learning:
                    Matching pairs similar
                    Non-matching pairs different
```

### CLIP Training

```python
# Pseudocode for CLIP training
def clip_loss(image_embeddings, text_embeddings, temperature=0.07):
    # Normalize embeddings
    image_embeddings = F.normalize(image_embeddings, dim=-1)
    text_embeddings = F.normalize(text_embeddings, dim=-1)

    # Compute similarity matrix
    logits = image_embeddings @ text_embeddings.T / temperature
    # logits[i,j] = similarity between image i and text j

    # Labels: diagonal entries should be high (matching pairs)
    labels = torch.arange(len(image_embeddings))

    # Symmetric cross-entropy loss
    loss_i2t = F.cross_entropy(logits, labels)      # Image → Text
    loss_t2i = F.cross_entropy(logits.T, labels)    # Text → Image

    return (loss_i2t + loss_t2i) / 2
```

### Zero-Shot Classification with CLIP

```python
# Classify image without training
classes = ["cat", "dog", "car", "house"]
prompts = [f"a photo of a {c}" for c in classes]

# Get embeddings
image_features = clip.encode_image(image)
text_features = clip.encode_text(prompts)

# Predict
similarities = image_features @ text_features.T
prediction = classes[similarities.argmax()]
```

---

## Vision-Language Models (VLMs)

### LLaVA (Large Language and Vision Assistant)

```
Architecture:
Image ──→ Vision Encoder (CLIP ViT) ──→ Projection ──→ [Visual tokens]
                                                            │
                                              ┌─────────────┘
                                              ↓
Text prompt ──→ LLM Tokenizer ──→ [Text tokens, Visual tokens, Text tokens]
                                              │
                                              ↓
                                       LLM (LLaMA/Vicuna)
                                              │
                                              ↓
                                        Generated text
```

```python
# LLaVA-style visual tokens
class VisualProjection(nn.Module):
    def __init__(self, vision_dim, llm_dim):
        super().__init__()
        self.proj = nn.Linear(vision_dim, llm_dim)

    def forward(self, image_features):
        # image_features: [batch, num_patches, vision_dim]
        # Convert to LLM token space
        visual_tokens = self.proj(image_features)
        return visual_tokens  # [batch, num_patches, llm_dim]
```

### GPT-4V / Claude Vision

Native multimodal LLMs with integrated vision:

```
"Describe this image: [IMAGE]"

Input Processing:
1. Image → Vision Encoder → Patch embeddings
2. Text → Tokenizer → Text embeddings
3. Interleave: [text_embed, image_embed, text_embed]
4. Single forward pass through unified model
```

---

## Text-to-Image Models

### DALL-E / DALL-E 2

```
DALL-E 2 Pipeline:
1. Text ──→ CLIP Text Encoder ──→ text_embed
2. text_embed ──→ Prior ──→ image_embed (predicted CLIP embedding)
3. image_embed ──→ Diffusion Decoder ──→ Image

The "Prior" bridges text and image CLIP spaces
```

### Stable Diffusion

```
Text ──→ CLIP/T5 Encoder ──→ text_embed
                                  │
                                  ↓
Random noise ──→ U-Net (conditioned on text_embed) ──→ Latent
                                                          │
                                                          ↓
                            VAE Decoder ──→ Image

Key: Works in latent space (faster, less memory)
```

---

## Audio-Language Models

### Whisper (Speech-to-Text)

```
Audio ──→ Log-Mel Spectrogram ──→ Encoder ──→ Cross-Attention
                                                    │
                                    ←───────────────┘
                                    │
                              Decoder ──→ Text tokens

Encoder-Decoder Transformer trained on 680k hours of audio
```

### AudioLM / MusicLM

```
Audio Generation:
Text prompt ──→ Text Encoder ──→ Conditioning
                                     │
                                     ↓
              Acoustic Tokens ←── Transformer ──→ Audio Codec ──→ Audio
```

---

## Implementation Example: Simple VLM

```python
import torch
import torch.nn as nn
from transformers import CLIPVisionModel, LlamaForCausalLM

class SimpleVLM(nn.Module):
    def __init__(self):
        super().__init__()
        # Vision encoder
        self.vision_encoder = CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32")

        # Language model
        self.llm = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

        # Projection layer
        self.visual_projection = nn.Linear(
            self.vision_encoder.config.hidden_size,
            self.llm.config.hidden_size
        )

        # Freeze vision encoder
        for param in self.vision_encoder.parameters():
            param.requires_grad = False

    def encode_image(self, images):
        with torch.no_grad():
            vision_outputs = self.vision_encoder(images)
            image_features = vision_outputs.last_hidden_state  # [B, num_patches, vision_dim]

        visual_tokens = self.visual_projection(image_features)
        return visual_tokens

    def forward(self, images, input_ids, attention_mask):
        # Get visual tokens
        visual_tokens = self.encode_image(images)

        # Get text embeddings
        text_embeds = self.llm.get_input_embeddings()(input_ids)

        # Concatenate: [visual_tokens, text_embeds]
        inputs_embeds = torch.cat([visual_tokens, text_embeds], dim=1)

        # Update attention mask
        visual_mask = torch.ones(visual_tokens.shape[:2], device=attention_mask.device)
        attention_mask = torch.cat([visual_mask, attention_mask], dim=1)

        # Forward through LLM
        outputs = self.llm(
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask
        )

        return outputs

# Usage
model = SimpleVLM()
response = model.generate(image, "What is in this image?")
```

---

## Multimodal Benchmarks

| Benchmark | Task | Modalities |
|-----------|------|------------|
| VQA v2 | Visual Question Answering | Image + Text |
| COCO Captions | Image Captioning | Image → Text |
| GQA | Compositional Reasoning | Image + Text |
| TextVQA | OCR + Reasoning | Image + Text |
| MMBench | Comprehensive | Multi |
| SEED-Bench | Generation Quality | Multi |

---

## Exercises

1. **Implement**: Build CLIP-style contrastive learning on small dataset
2. **Zero-shot**: Use CLIP for classification without fine-tuning
3. **VLM**: Add visual tokens to a small language model
4. **Evaluate**: Test VLM on VQA benchmark
5. **Compare**: Early vs late fusion on same task

---

## Key Takeaways

- Multimodal models combine different data types (text, image, audio)
- CLIP: Foundational vision-language model using contrastive learning
- VLMs: Project visual features into LLM space
- Early/Late/Cross-attention: Different fusion strategies
- Diffusion models: Dominant for image generation
- Zero-shot: CLIP enables classification without training

---

## Next Steps

→ Continue to [03-diffusion-models.md](./03-diffusion-models.md)
