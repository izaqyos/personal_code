# Transformers

Attention-based architecture for sequence modeling.

## Overview

Transformers use self-attention to process sequences in parallel, replacing recurrence.

```
Input → Embedding → Positional Encoding → 
        Encoder Layers → Output

Each encoder layer:
  Multi-Head Attention → Add & Norm → FFN → Add & Norm
```

## Self-Attention Mechanism

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

def scaled_dot_product_attention(query, key, value, mask=None):
    """
    Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
    """
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    attention_weights = F.softmax(scores, dim=-1)
    output = torch.matmul(attention_weights, value)
    
    return output, attention_weights
```

### Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # Linear projections and reshape to (batch, heads, seq_len, d_k)
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Attention
        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)
        
        # Concatenate heads
        attn_output = attn_output.transpose(1, 2).contiguous().view(
            batch_size, -1, self.d_model
        )
        
        return self.W_o(attn_output)
```

## Positional Encoding

Adds position information since attention is permutation-invariant.

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]
```

## Transformer Encoder Layer

```python
class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-attention with residual
        attn_output = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed-forward with residual
        ffn_output = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_output))
        
        return x
```

## Complete Transformer Encoder

```python
class TransformerEncoder(nn.Module):
    def __init__(self, vocab_size, d_model=512, num_heads=8, 
                 num_layers=6, d_ff=2048, max_len=512, dropout=0.1):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len)
        self.dropout = nn.Dropout(dropout)
        
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
    
    def forward(self, x, mask=None):
        x = self.embedding(x) * math.sqrt(self.d_model)
        x = self.pos_encoding(x)
        x = self.dropout(x)
        
        for layer in self.layers:
            x = layer(x, mask)
        
        return x
```

## Using PyTorch's Built-in Transformer

```python
import torch.nn as nn

# Encoder only
encoder_layer = nn.TransformerEncoderLayer(
    d_model=512,
    nhead=8,
    dim_feedforward=2048,
    dropout=0.1,
    batch_first=True
)
encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)

# Full Transformer
transformer = nn.Transformer(
    d_model=512,
    nhead=8,
    num_encoder_layers=6,
    num_decoder_layers=6,
    dim_feedforward=2048,
    dropout=0.1,
    batch_first=True
)
```

## Text Classification with Transformer

```python
class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size, num_classes, d_model=256, 
                 num_heads=4, num_layers=2, max_len=512):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=num_heads,
            dim_feedforward=d_model * 4,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers)
        
        self.classifier = nn.Linear(d_model, num_classes)
    
    def forward(self, x, mask=None):
        x = self.embedding(x)
        x = self.pos_encoding(x)
        x = self.encoder(x, src_key_padding_mask=mask)
        
        # Use [CLS] token or mean pooling
        x = x.mean(dim=1)  # Mean pooling
        
        return self.classifier(x)
```

## Using Hugging Face Transformers

### Pre-trained Models

```python
from transformers import (
    AutoTokenizer, 
    AutoModel, 
    AutoModelForSequenceClassification
)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Tokenize
inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)

# Get embeddings
last_hidden_states = outputs.last_hidden_state  # (batch, seq, hidden)
pooler_output = outputs.pooler_output  # (batch, hidden) - [CLS] token
```

### Fine-tuning for Classification

```python
from transformers import (
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

# Load model for classification
model = AutoModelForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    evaluation_strategy="epoch"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

## Common Pre-trained Models

### Encoder-Only (BERT family)
```python
# BERT - Bidirectional, masked language modeling
from transformers import BertModel, BertTokenizer

# RoBERTa - Optimized BERT training
from transformers import RobertaModel, RobertaTokenizer

# DistilBERT - Smaller, faster BERT
from transformers import DistilBertModel, DistilBertTokenizer
```

### Decoder-Only (GPT family)
```python
# GPT-2
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Generate text
input_ids = tokenizer.encode("Hello, I'm a language model", return_tensors='pt')
outputs = model.generate(input_ids, max_length=50)
print(tokenizer.decode(outputs[0]))
```

### Encoder-Decoder (T5, BART)
```python
# T5 - Text-to-text
from transformers import T5ForConditionalGeneration, T5Tokenizer

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Summarization
input_text = "summarize: " + long_text
inputs = tokenizer(input_text, return_tensors='pt', truncation=True)
outputs = model.generate(**inputs)
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Attention Visualization

```python
# Get attention weights
outputs = model(**inputs, output_attentions=True)
attentions = outputs.attentions  # Tuple of (batch, heads, seq, seq)

# Visualize
import matplotlib.pyplot as plt
import seaborn as sns

attention = attentions[0][0, 0].detach().numpy()  # First layer, first head
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

plt.figure(figsize=(10, 8))
sns.heatmap(attention, xticklabels=tokens, yticklabels=tokens)
plt.title('Attention Weights')
plt.show()
```

## Key Concepts

### Attention Patterns
```
Self-Attention: Token attends to all tokens in sequence
Cross-Attention: Decoder attends to encoder outputs
Causal Attention: Token only attends to previous tokens (GPT)
```

### Scaling Laws
```
Model quality scales with:
- Number of parameters
- Amount of training data
- Compute used for training

Bigger models = better performance (with enough data)
```

## Quick Reference

```python
# PyTorch Transformer
nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward)
nn.TransformerEncoder(encoder_layer, num_layers)

# Hugging Face
AutoTokenizer.from_pretrained('bert-base-uncased')
AutoModel.from_pretrained('bert-base-uncased')
AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=n)

# Key dimensions
d_model = 512      # Model/embedding dimension
num_heads = 8      # Attention heads
d_ff = 2048        # Feed-forward dimension (usually 4 * d_model)
num_layers = 6     # Number of encoder/decoder layers
```

## Related Topics
- [Neural Networks](neural_networks.md)
- [RNNs](rnn.md)
- [LLMs](../03_generative_ai/llms.md)
