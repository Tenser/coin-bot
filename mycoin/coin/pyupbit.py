import json
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

class PyUpbit:

    def __init__(self, access_key='usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK', secret_key='Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub'):
        self.access_key = access_key
        self.secret_key = secret_key

    def get_current_price(self, market, count=1):
        url = "https://api.upbit.com/v1/candles/days"
        querystring = {"count": count}
        querystring["market"] = market
        response = requests.request("GET", url, params=querystring)
        #print(response.text)
        json_data = json.loads(response.text)

        return json_data[0]["trade_price"]

    def get_funding_fee(self, code):
        query = {
            'currency': code,
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }       

        jwt_token = jwt.encode(payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.get("https://api.upbit.com/v1/withdraws/chance", params=query, headers=headers)

        return float(res.json()['currency']['withdraw_fee'])

