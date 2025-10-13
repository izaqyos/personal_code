from openai import OpenAI

# Replace with your DeepSeek API token
DEEPSEEK_API_TOKEN = 'YOUR_DEEPSEEK_API_KEY_HERE'

# Initialize the OpenAI client
client = OpenAI(api_key=DEEPSEEK_API_TOKEN, base_url="https://api.deepseek.com")

#messages = [
#        {
#        "role": "user",
#        "content": "Create a simple calculator function in Rust that supports addition, subtraction, multiplication, and division.", 
#        }
#]
#
#response = client.chat.completions.create(
#   model="deepseek-reasoner", 
#   messages=messages,
#)
#
#reasoning_content = response.choices[0].message.reasoning_content
#content = response.choices[0].message.content
#print(reasoning_content)
#print(content)

# Function to send a prompt to the DeepSeek API
def send_prompt(prompt, model="deepseek-reasoner"):
    try:
        response = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=200,  # Adjust as needed
            temperature=0.7  # Adjust as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Prompt 1: Create a simple calculator function in Rust
rust_prompt = "Create a simple calculator function in Rust that supports addition, subtraction, multiplication, and division."
rust_code = send_prompt(rust_prompt)

# Prompt 2: Create a simple calculator function in C++
cpp_prompt = "Create a simple calculator function in C++ that supports addition, subtraction, multiplication, and division."
cpp_code = send_prompt(cpp_prompt)

# Prompt 3: Create a simple calculator function in Python
python_prompt = "Create a simple calculator function in Python that supports addition, subtraction, multiplication, and division."
python_code = send_prompt(python_prompt)

# Output the results
print("Rust Calculator Function:")
print(rust_code if rust_code else "Failed to generate Rust code.")

print("\nC++ Calculator Function:")
print(cpp_code if cpp_code else "Failed to generate C++ code.")

print("\nPython Calculator Function:")
print(python_code if python_code else "Failed to generate Python code.")
