import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK'
secret_key = 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub'
server_url = "https://api.upbit.com"
query = {
    'currency': 'BTC',
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
print(jwt_token)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/withdraws/chance", params=query, headers=headers)

print(res.json())