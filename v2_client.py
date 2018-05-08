import json
import requests

URL = 'http://127.0.0.1:5000/crypto'
HEADERS = {'Content-Type': 'application/json'}

data = json.dumps({'data':'some_data_to_crypt', 'password': 'some_key_to_crypt'})
response = requests.post(URL, data=data, headers=HEADERS)
print(response.json()['result'])
