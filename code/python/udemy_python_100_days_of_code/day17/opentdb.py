import requests

class OpenTDB:
    def __init__(self, url) -> None:
        self.url = url

    def get_questions(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            json_response = response.json()
            return json_response
        else:
            print(f'Request failed with status code: {response.status_code}')
