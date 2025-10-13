import requests
from newspaper import Article

print("Starting Summary...")

# Extract article text
article_url = "https://learn.microsoft.com/en-us/azure/well-architected/security/principles"
print(f"Extracting text from {article_url}...") 
article = Article(article_url)
article.download()
article.parse()
prompt = article.text

# Model and API endpoint configuration
model = "llama3.2"
endpoint = "http://localhost:11434/api/generate"
systemPrompt = "Create a concise summary of Azure principles, make sure to highlight the key points."
print(f"Using Model: {model}, Endpoint: {endpoint}")

# Prepare request payload
payload = {
    "model": model,
    "prompt": prompt,
    "stream": False,
    "system": systemPrompt,
    "options": {"temperature": 0.5}
}

# Make API request
response = requests.post(endpoint, json=payload)
response_data = response.json()

# Output response
print(response_data.get("response"))

