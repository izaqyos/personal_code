#!/usr/bin/env python3
import os

import requests

# Credentials come from the environment, never from source control.
resp = requests.get(
    'https://host.example.com:44300/api/entities',
    auth=(os.environ['API_USER'], os.environ['API_PASSWORD']),
    verify=False,
)
print(resp.json())
