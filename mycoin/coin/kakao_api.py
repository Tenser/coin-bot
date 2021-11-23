import json
import requests

class KakaoApi:
    def __init__(self, token="LBOUZs7elCXGEJmOz7zSV02JM5tCkwif-lfyXgo9c5sAAAF4VKam_g"):
        #self.token = token
        self.url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        self.headers = {"Authorization": "Bearer " + token}
        self.post = {
            "object_type": "text",
            "text": "text",
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            },
            "button_title": "바로 확인"
        }

    def msg_send(self, text_dict):
        text = "<{title}>\n{market} {rate}".format(title=text_dict['title'], market=text_dict['market'], rate=text_dict['rate'])
        self.post["text"] = text
        data = {"template_object": json.dumps(self.post)}
        print(requests.post(self.url, headers=self.headers, data=data).text)
    
    def token_rewel(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {"grant_type": "refresh_token", "client_id": "93da95892b353ba2f66bc307b5d9de6e", "refresh_token": "LBOUZs7elCXGEJmOz7zSV02JM5tCkwif-lfyXgo9c5sAAAF4VKam_g"}
        json_data = json.loads(requests.post(url, data=data).text)
        print(json_data)
        self.headers["Authorization"] = "Bearer " + json_data["access_token"]
        
