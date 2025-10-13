import requests

url = "http://localhost:11434/api/chat"

data = {
    "model": "llama2",
    "messages": [
        {
            "role": "user",
            "content": "Tell me about planet mars"
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)

if response.status_code == 200:
  response_data = response.json()
  print(response_data['message']['content'])  
else:
  print(f"Error: {response.status_code}")
