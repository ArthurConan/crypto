import base64
import hashlib
import json

from flask import Flask, request
from flask_restful import Resource, Api
from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)
api = Api(app)


class Crypto(object):
        
    def __init__(self, data, password, block_size = 16):
        self.data = data
        self.password = password
        self.block_size = block_size
        
    def encrypt(self):
        private_key = hashlib.sha256(self.password.encode("utf-8")).digest()
        b_size = self.block_size
        PAD = lambda s: s + (b_size - len(s) % b_size
                             ) * chr(b_size - len(s) % b_size)
        raw = PAD(self.data)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        
        return "Encrypted text = {}".format(base64.b64encode(iv + 
                                 cipher.encrypt(raw)))
    
    def decrypt(self, enc):
        private_key = hashlib.sha256(self.password.encode("utf-8")).digest()
        UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        
        return "Plain text = {}".format(UNPAD(cipher.decrypt(enc[16:])))
    
    
class My_api(Resource):
    
    def post(self):
        data = json.loads(request.data)
        cipher = Crypto(data['data'],data['password'])
        encrypted = cipher.encrypt()
        decrypted = cipher.decrypt(encrypted)
        return {'result': encrypted + bytes.decode(decrypted)}
        
      

api.add_resource(My_api, '/crypto')

if __name__ == '__main__':
    app.run(debug=True)
