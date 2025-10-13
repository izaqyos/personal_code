import requests
import json

# Replace with your Ollama server URL
url = "http://localhost:11434/api/chat"

# Define the request data
data = {
    "model": "llama2",
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        }
    ],
    "stream": True
}

# Send the POST request with streaming enabled
response = requests.post(url, json=data, stream=True)

# Check for successful response
if response.status_code == 200:
  print("Ollama is generating responses. Receiving data in chunks...")

  # Loop through the streaming response data
  line_len = 256
  total_len = 0
  to_print = ""
  for line in response.iter_lines():
    # Decode the line (assuming JSON format)
    if line:  # Check if line is not empty
      decoded_line = line.decode("utf-8")
      to_print += json.loads(decoded_line)['message']['content']
      response_data = len(to_print) 
      total_len += len(to_print)
      if total_len > line_len:
        print(to_print)
        to_print = ""
        total_len = 0

  print(to_print)
  print("Streaming response completed.")
else:
  print(f"Error: {response.status_code}")
