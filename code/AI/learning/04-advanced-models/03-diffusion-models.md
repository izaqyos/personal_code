# Diffusion Models

> State-of-the-art generative models that learn by denoising.

---

## Overview

Diffusion models generate data by learning to reverse a gradual noising process.

```
Forward Process (Fixed):
Clean image ──→ Add noise ──→ Add noise ──→ ... ──→ Pure noise
    x₀           x₁            x₂                    xₜ

Reverse Process (Learned):
Pure noise ──→ Denoise ──→ Denoise ──→ ... ──→ Clean image
    xₜ           xₜ₋₁        xₜ₋₂              x₀

The model learns to predict and remove noise at each step!
```

---

## Intuition

### Forward: Destruction is Easy

```
Start: Sharp image of a cat
Add 1% noise: Still a cat, bit fuzzy
Add more noise: Getting blurry
... (1000 steps) ...
End: Pure random noise

Each step is tiny - just add small Gaussian noise
After enough steps, ALL images become indistinguishable noise
```

### Reverse: Reconstruction is Learning

```
Start: Random noise
Remove some noise: Vague shapes appear
Remove more: Object emerges
... (1000 steps) ...
End: Clear cat image

Key insight: At each step, "removing noise" = predicting what to remove
A neural network learns this prediction!
```

---

## Mathematical Framework

### Forward Process

```
q(xₜ | xₜ₋₁) = N(xₜ; √(1-βₜ)xₜ₋₁, βₜI)

Where βₜ is the noise schedule (small, e.g., 0.0001 to 0.02)

Simplified: xₜ = √(1-βₜ)xₜ₋₁ + √βₜ ε,  where ε ~ N(0, I)

After t steps (closed form):
xₜ = √ᾱₜ x₀ + √(1-ᾱₜ) ε

Where:
αₜ = 1 - βₜ
ᾱₜ = α₁ × α₂ × ... × αₜ (cumulative product)
```

### Reverse Process

```
p_θ(xₜ₋₁ | xₜ) = N(xₜ₋₁; μ_θ(xₜ, t), Σ_θ(xₜ, t))

The neural network predicts:
- μ_θ: Mean of the denoised image
- Σ_θ: Variance (often fixed)

Equivalently, predict the noise ε_θ(xₜ, t)
```

---

## Training

### Simple Loss (Predict Noise)

```python
def training_step(model, x0):
    # 1. Sample random timestep
    t = torch.randint(0, T, (batch_size,))

    # 2. Sample noise
    noise = torch.randn_like(x0)

    # 3. Create noisy image (forward process)
    alpha_bar_t = get_alpha_bar(t)
    xt = sqrt(alpha_bar_t) * x0 + sqrt(1 - alpha_bar_t) * noise

    # 4. Predict noise
    predicted_noise = model(xt, t)

    # 5. Loss: how well did we predict the noise?
    loss = F.mse_loss(predicted_noise, noise)

    return loss
```

### The Denoising Objective

```
Loss = E_{t,x₀,ε}[ ||ε - ε_θ(xₜ, t)||² ]

"Predict the noise that was added at timestep t"

This is equivalent to:
- Predicting x₀ directly
- Predicting the score ∇log p(xₜ)
```

---

## Sampling (Generation)

```python
def sample(model, shape):
    # Start from pure noise
    x = torch.randn(shape)

    for t in reversed(range(T)):
        # Predict noise
        predicted_noise = model(x, t)

        # Compute mean
        alpha_t = get_alpha(t)
        alpha_bar_t = get_alpha_bar(t)
        alpha_bar_prev = get_alpha_bar(t-1) if t > 0 else 1.0

        # DDPM sampling formula
        mean = (1 / sqrt(alpha_t)) * (
            x - (1 - alpha_t) / sqrt(1 - alpha_bar_t) * predicted_noise
        )

        # Add noise (except at t=0)
        if t > 0:
            sigma_t = sqrt((1 - alpha_bar_prev) / (1 - alpha_bar_t) * (1 - alpha_t))
            x = mean + sigma_t * torch.randn_like(x)
        else:
            x = mean

    return x
```

---

## Architecture: U-Net

Standard diffusion model architecture:

```
        Input: [noisy image, timestep embedding]
                        │
    ┌───────────────────┼───────────────────┐
    │                   ↓                   │
    │   Encoder     ┌───────┐               │
    │   64──128     │Conv   │───────────────│──→ Skip to decoder
    │   128──256    │ResNet │───────────────│──→
    │   256──512    │Attn   │───────────────│──→
    │               └───────┘               │
    │                   │                   │
    │                   ↓                   │
    │              [Bottleneck]             │
    │                   │                   │
    │                   ↓                   │
    │   Decoder     ┌───────┐               │
    │   512──256    │Conv   │←──────────────│
    │   256──128    │ResNet │←──────────────│
    │   128──64     │Attn   │←──────────────│
    │               └───────┘               │
    │                   │                   │
    └───────────────────┼───────────────────┘
                        ↓
              Output: predicted noise

Key components:
- Residual blocks
- Self-attention layers
- Skip connections
- Timestep conditioning (added to features)
```

---

## Conditioning (Text-to-Image)

### Cross-Attention Conditioning

```
For each attention layer in U-Net:

Q = image_features @ Wq    (from image)
K = text_embedding @ Wk    (from text)
V = text_embedding @ Wv    (from text)

Attention = softmax(QKᵀ/√d) @ V

Text guides which parts of the image to modify!
```

### Classifier-Free Guidance (CFG)

Stronger adherence to prompt:

```python
def guided_sample(model, x, t, text_embed, guidance_scale=7.5):
    # Unconditional prediction
    noise_uncond = model(x, t, text_embed=None)

    # Conditional prediction
    noise_cond = model(x, t, text_embed=text_embed)

    # Interpolate (extrapolate, actually)
    noise = noise_uncond + guidance_scale * (noise_cond - noise_uncond)

    return noise

# guidance_scale > 1: Stronger text adherence
# guidance_scale = 1: Normal sampling
# guidance_scale = 0: Unconditional
```

---

## Latent Diffusion (Stable Diffusion)

Work in compressed latent space:

```
Image Space (512×512×3):        Latent Space (64×64×4):
    ~786k pixels                    ~16k values (50× smaller!)

Pipeline:
1. Image ──→ VAE Encoder ──→ Latent
2. Latent ──→ Diffusion (noising/denoising) ──→ Latent
3. Latent ──→ VAE Decoder ──→ Image

Benefits:
- Much faster training/sampling
- Lower memory usage
- Semantically meaningful space
```

---

## Implementation

### Simple U-Net Block

```python
class UNetBlock(nn.Module):
    def __init__(self, in_ch, out_ch, time_dim):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, padding=1)
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding=1)
        self.time_mlp = nn.Linear(time_dim, out_ch)
        self.norm1 = nn.GroupNorm(8, out_ch)
        self.norm2 = nn.GroupNorm(8, out_ch)

        if in_ch != out_ch:
            self.skip = nn.Conv2d(in_ch, out_ch, 1)
        else:
            self.skip = nn.Identity()

    def forward(self, x, time_emb):
        h = self.norm1(F.silu(self.conv1(x)))

        # Add time embedding
        time_emb = self.time_mlp(F.silu(time_emb))
        h = h + time_emb[:, :, None, None]

        h = self.norm2(F.silu(self.conv2(h)))

        return h + self.skip(x)


class SimpleDiffusion(nn.Module):
    def __init__(self, img_channels=3, base_ch=64, time_dim=256):
        super().__init__()

        # Time embedding
        self.time_mlp = nn.Sequential(
            SinusoidalPositionEmbedding(time_dim),
            nn.Linear(time_dim, time_dim * 4),
            nn.GELU(),
            nn.Linear(time_dim * 4, time_dim)
        )

        # Encoder
        self.down1 = UNetBlock(img_channels, base_ch, time_dim)
        self.down2 = UNetBlock(base_ch, base_ch * 2, time_dim)
        self.pool = nn.MaxPool2d(2)

        # Bottleneck
        self.mid = UNetBlock(base_ch * 2, base_ch * 2, time_dim)

        # Decoder
        self.up2 = UNetBlock(base_ch * 4, base_ch, time_dim)
        self.up1 = UNetBlock(base_ch * 2, base_ch, time_dim)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear')

        # Output
        self.out = nn.Conv2d(base_ch, img_channels, 1)

    def forward(self, x, t):
        # Time embedding
        t_emb = self.time_mlp(t)

        # Encoder
        d1 = self.down1(x, t_emb)
        d2 = self.down2(self.pool(d1), t_emb)

        # Bottleneck
        mid = self.mid(self.pool(d2), t_emb)

        # Decoder with skip connections
        u2 = self.up2(torch.cat([self.upsample(mid), d2], dim=1), t_emb)
        u1 = self.up1(torch.cat([self.upsample(u2), d1], dim=1), t_emb)

        return self.out(u1)
```

---

## Modern Improvements

### DDIM (Deterministic Sampling)

Faster sampling (50 steps instead of 1000):

```python
# DDPM: Stochastic, needs ~1000 steps
# DDIM: Deterministic, can use ~50 steps

def ddim_step(model, x, t, t_prev, eta=0):
    pred_noise = model(x, t)

    alpha_t = get_alpha_bar(t)
    alpha_prev = get_alpha_bar(t_prev)

    # Predict x0
    pred_x0 = (x - sqrt(1 - alpha_t) * pred_noise) / sqrt(alpha_t)

    # Direction pointing to xt
    dir_xt = sqrt(1 - alpha_prev - sigma**2) * pred_noise

    # Random noise (eta=0 for deterministic)
    sigma = eta * sqrt((1 - alpha_prev) / (1 - alpha_t)) * sqrt(1 - alpha_t / alpha_prev)

    x_prev = sqrt(alpha_prev) * pred_x0 + dir_xt + sigma * torch.randn_like(x)

    return x_prev
```

### Flow Matching

Simpler training, straight paths:

```
Instead of discrete noise schedule,
learn continuous flow from noise to data
```

---

## Exercises

1. **Implement**: Train simple diffusion on MNIST
2. **Schedules**: Compare linear vs cosine noise schedules
3. **Sampling**: Implement DDIM, compare speed vs quality
4. **Conditioning**: Add class conditioning to diffusion model
5. **Latent**: Build VAE, train diffusion in latent space

---

## Key Takeaways

- Diffusion = learn to reverse gradual noising
- Training: predict the noise added at each step
- U-Net: standard architecture with skip connections
- Conditioning via cross-attention enables text-to-image
- Latent diffusion (Stable Diffusion) is much more efficient
- CFG strengthens prompt adherence
- DDIM enables faster sampling

---

## Next Steps

→ Continue to [04-emerging-architectures.md](./04-emerging-architectures.md)
