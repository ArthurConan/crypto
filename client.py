import json
import requests

URL_ENCRYPT = 'http://127.0.0.1:5000/encrypt'
URL_DECRYPT = 'http://127.0.0.1:5000/decrypt'
HEADERS = {'Content-Type': 'application/json'}

data_encrypt = json.dumps({'data':'some_data_to_crypt', 'password': 'some_key_to_crypt'})
data_decrypt = json.dumps({'data':'AuL8r1SratZA69jmqRd88Q3S981dWwrPDK/tvVFUZuYs9Kh4SpJ/K9PeDD5jbX8A', 'password': 'some_key_to_crypt'})

response_encrypt = requests.post(URL_ENCRYPT, data=data_encrypt, headers=HEADERS)
response_decrypt = requests.post(URL_DECRYPT, data=data_decrypt, headers=HEADERS)
print(response_encrypt.json()['result'])
print(response_decrypt.json()['result'])