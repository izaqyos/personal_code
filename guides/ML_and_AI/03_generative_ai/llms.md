# Large Language Models (LLMs)

Understanding and using large language models.

## Overview

LLMs are transformer-based models trained on massive text corpora to predict next tokens.

```
Training: Predict next word given context
Usage: Complete prompts, answer questions, generate text
```

## Key Concepts

### Tokenization
Text is split into tokens (words, subwords, or characters).

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('gpt2')

text = "Hello, world!"
tokens = tokenizer.tokenize(text)
print(tokens)  # ['Hello', ',', 'Ġworld', '!']

# Encode to IDs
token_ids = tokenizer.encode(text)
print(token_ids)  # [15496, 11, 995, 0]

# Decode back
decoded = tokenizer.decode(token_ids)
print(decoded)  # "Hello, world!"
```

### Context Window
Maximum number of tokens the model can process at once.

```
GPT-3.5: 4,096 tokens
GPT-4: 8,192 / 32,768 / 128,000 tokens
Claude: 100,000+ tokens
Llama 2: 4,096 tokens
```

### Temperature
Controls randomness in generation.

```
Temperature 0: Deterministic, always most likely token
Temperature 0.7: Balanced creativity
Temperature 1.0+: More random/creative
```

## Using OpenAI API

```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

# Chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Streaming Response
```python
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Using Open Source Models

### Hugging Face Transformers
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Generate
prompt = "[INST] What is Python? [/INST]"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=256,
    temperature=0.7,
    do_sample=True
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Using Pipeline
```python
from transformers import pipeline

# Simple text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("Hello, I'm a language model", max_length=50)
print(result[0]['generated_text'])

# Chat
chat = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")
messages = [
    {"role": "user", "content": "What's the capital of France?"}
]
response = chat(messages, max_new_tokens=100)
```

## Prompt Engineering

### Basic Principles
```
1. Be specific and clear
2. Provide context and examples
3. Specify output format
4. Use delimiters for clarity
```

### Zero-Shot
```python
prompt = """
Classify the sentiment of the following text as positive, negative, or neutral.

Text: "I love this product! It works perfectly."
Sentiment:
"""
```

### Few-Shot
```python
prompt = """
Classify the sentiment of texts.

Text: "This is amazing!"
Sentiment: positive

Text: "Terrible experience."
Sentiment: negative

Text: "It's okay, nothing special."
Sentiment: neutral

Text: "Best purchase I've ever made!"
Sentiment:
"""
```

### Chain of Thought
```python
prompt = """
Solve this step by step:

Question: If a train travels 120 miles in 2 hours, and then 180 miles 
in 3 hours, what is the average speed for the entire journey?

Let's think step by step:
1. Total distance = 120 + 180 = 300 miles
2. Total time = 2 + 3 = 5 hours
3. Average speed = Total distance / Total time = 300 / 5 = 60 mph

Question: If a car uses 4 gallons of gas to travel 100 miles, how many 
gallons will it use to travel 350 miles?

Let's think step by step:
"""
```

### System Prompts
```python
messages = [
    {
        "role": "system",
        "content": """You are an expert Python programmer. 
        Always provide well-commented, production-ready code.
        Explain your solutions clearly.
        If you're unsure about something, say so."""
    },
    {
        "role": "user",
        "content": "Write a function to merge two sorted lists."
    }
]
```

## Function Calling

```python
# Define tools/functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if function was called
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    # Execute function and return result
```

## Embeddings

Vector representations for semantic search.

```python
# OpenAI embeddings
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello world"
)
embedding = response.data[0].embedding  # 1536 dimensions

# Sentence Transformers (local)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Hello world", "How are you?"])

# Cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
```

## Model Comparison

| Model | Parameters | Context | Speed | Cost |
|-------|------------|---------|-------|------|
| GPT-3.5 | 175B | 16K | Fast | Low |
| GPT-4 | ~1.8T (MOE) | 128K | Slow | High |
| Claude 3 Opus | - | 200K | Medium | High |
| Llama 2 70B | 70B | 4K | Medium | Free |
| Mistral 7B | 7B | 8K | Fast | Free |

## Best Practices

### Cost Optimization
```python
# Use smaller models for simple tasks
# Cache responses for repeated queries
# Batch requests when possible
# Use streaming for long responses
```

### Error Handling
```python
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def call_api(messages):
    try:
        return client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
    except openai.RateLimitError:
        print("Rate limited, retrying...")
        raise
    except openai.APIError as e:
        print(f"API error: {e}")
        raise
```

### Structured Output
```python
prompt = """
Extract information and return JSON:

{
  "name": "...",
  "email": "...",
  "company": "..."
}

Text: John Smith from Acme Corp, email john@acme.com
"""

# Or use function calling for guaranteed structure
```

## Local Deployment

### Ollama
```bash
# Install and run locally
ollama run llama2

# API compatible
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello!"
}'
```

### vLLM (High Performance)
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-hf")
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)

outputs = llm.generate(["Hello, my name is"], sampling_params)
```

## Quick Reference

```python
# OpenAI
client.chat.completions.create(model, messages, temperature, max_tokens)

# Hugging Face
AutoModelForCausalLM.from_pretrained(model_name)
model.generate(inputs, max_new_tokens, temperature)

# Key parameters
temperature: 0-2 (0=deterministic, 1=balanced, 2=creative)
max_tokens: Maximum output length
top_p: Nucleus sampling (0.9 typical)
presence_penalty: Discourage repetition
frequency_penalty: Discourage common tokens
```

## Related Topics
- [Transformers](../02_deep_learning/transformers.md)
- [RAG](rag.md)
- [Fine-tuning](fine_tuning.md)
