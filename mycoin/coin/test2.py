import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {"grant_type": "authorization_code", "client_id": "93da95892b353ba2f66bc307b5d9de6e", "redirect_uri": "https://example.com/oauth",
 "code": "rNarcOlkIsnj8nISGwyc7VUCf54tCBLJ1uaIMOLkHFE3cuK3bsXaJuYGHH9HFDiEkI6QbQo9cxcAAAF4VKY28g"}

print(requests.post(url, data=data).text)
