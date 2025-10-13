from openai import OpenAI

DEEPSEEK_API_TOKEN = 'YOUR_DEEPSEEK_API_KEY_HERE'

client = OpenAI(api_key=DEEPSEEK_API_TOKEN, base_url="https://api.deepseek.com")

messages =  [{"role": "user", "content": "Create a simple calculator function in Rust that supports addition, subtraction, multiplication, and division."}]

response = client.chat.completions.create(
   model="deepseek-reasoner", 
   messages=messages,
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content
print(reasoning_content)
print(content)

