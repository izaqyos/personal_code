# API Collection Examples

This document contains example API requests for the Content Design Time Assistant. You can use these examples to test the API directly from your terminal or integrate them into your applications.

## API Endpoint Reference

### POST /api/get_user_prompt

Sends a text prompt to the assistant and receives a classified response.

**Endpoint:** `http://localhost:3001/api/get_user_prompt`

**Request Body:**
```json
{
  "text": "Your prompt text here"
}
```

**Response:**
```json
{
  "response": "The assistant's response text",
  "requestType": "action | help | unknown",
  "actionType": "add_content_provider | remove_content_provider | update_content_provider | delete_content_provider"
}
```

## Example Requests

### Getting Help

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "What are content providers used for?"}' \
  http://localhost:3001/api/get_user_prompt
```

### Adding a Content Provider

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "I need to add a new content provider called DataHub with API key 54321"}' \
  http://localhost:3001/api/get_user_prompt
```

### Updating a Content Provider

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Please update the CloudStorage content provider with a new base URL of https://cloud-api.example.com"}' \
  http://localhost:3001/api/get_user_prompt
```

### Removing a Content Provider

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Remove the content provider named LegacySystem"}' \
  http://localhost:3001/api/get_user_prompt
```

### Deleting a Content Provider

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Delete the outdated content provider TestProvider"}' \
  http://localhost:3001/api/get_user_prompt
```

## Using with Other Tools

### Python Example

```python
import requests
import json

url = "http://localhost:3001/api/get_user_prompt"
headers = {"Content-Type": "application/json"}
data = {"text": "How do I configure a content provider?"}

response = requests.post(url, headers=headers, data=json.dumps(data))
result = response.json()

print(f"Response: {result['response']}")
print(f"Request Type: {result['requestType']}")
if 'actionType' in result and result['actionType']:
    print(f"Action Type: {result['actionType']}")
```

### JavaScript Example

```javascript
fetch('http://localhost:3001/api/get_user_prompt', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: 'Add a new content provider called APIService'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Response:', data.response);
  console.log('Request Type:', data.requestType);
  if (data.actionType) {
    console.log('Action Type:', data.actionType);
  }
})
.catch(error => console.error('Error:', error));
``` 