#!/usr/local/bin/python3

import requests

resp = requests.get( 'https://ldai1uyr.wdf.sap.corp:44300/sap/bc/ui2/poc_cdm3/entities?sap-client=200&useRA=true', auth=('COHENADA',  'k8h2VUsY'), verify=False)
print(resp.json())
