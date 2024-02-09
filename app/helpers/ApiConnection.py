import requests
import datetime
import time
import hmac
import hashlib
import uuid
import json


class ApiConnection(object):

    uid = str(uuid.uuid4())
    timestamp = str(time.time()).split('.')[0]
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    def __init__(self, url, apiKey, apiSecret):
        self.url = url
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def getHash(self):
        _encoded_key = self.apiKey.encode()
        _encoded_secret = self.apiSecret.encode()
        _encoded_timestamp = self.timestamp.encode()
        h = hmac.new(_encoded_secret, _encoded_key, hashlib.sha512)
        h.update(_encoded_timestamp)
        return h.hexdigest()

    def getHeaders(self):
        headers = {
            'API-Key': self.apiKey,
            'API-Hash': self.getHash(),
            'operation-id': self.uid,
            'Request-Timestamp': self.timestamp,
            'Content-Type': 'application/json'
        }
        return headers

    def getData(self):
        response = requests.request("GET", self.url, headers=self.getHeaders())
        json_data = json.loads(response.text)
        return json_data
