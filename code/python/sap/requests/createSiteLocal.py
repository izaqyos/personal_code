import requests

url = "http://localhost:3003/semantic/entity/site"

payload = "{\n  \"name\": \"yosi\",\n  \"id\": \"123\"\n}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "7005c13d-dc7d-4191-8822-369797713cfd"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

