import base64
import hashlib
import json

from flask import Flask, request
from flask_restful import Resource, Api
from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)
api = Api(app)


class Encrypt_string(Resource):
        
    def post(self):
        data = json.loads(request.data)
        string = data['data']
        password = data['password']
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        b_size = 16
        PAD = lambda s: s + (b_size - len(s) % b_size
                             ) * chr(b_size - len(s) % b_size)
        raw = PAD(string)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        
        return {'result': "Encrypted text = {}".format(base64.b64encode(iv + 
                                 cipher.encrypt(raw)))}
    
        
class Decrypt_string(Resource):
        
    def post(self):
        data = json.loads(request.data)
        encrypted = data['data']
        password = data['password']
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
        enc = base64.b64decode(encrypted)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        
        return {'result': "Plain text = {}".format(UNPAD(cipher.decrypt(enc[16:])))}
    

api.add_resource(Encrypt_string, '/encrypt')
api.add_resource(Decrypt_string, '/decrypt')

if __name__ == '__main__':
    app.run(debug=True)