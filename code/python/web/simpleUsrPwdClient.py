#!/usr/local/bin/python3

import requests

resp = requests.get( 'https://host.example.com:44300/api/entities', auth=('<user>',  '<password>'), verify=False)
print(resp.json())
