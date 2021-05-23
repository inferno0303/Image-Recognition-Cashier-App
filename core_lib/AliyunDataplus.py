# author：Teemo
# version： 20190507

import datetime
import base64
import hmac
import hashlib
import json
import requests


class AliyunDataplus():
    def __init__(self, ak_id, ak_secret):
        self.ak_id = ak_id
        self.ak_secret = ak_secret

    @classmethod
    def to_md5_base64(cls, body):
        body = body.encode()
        hash = hashlib.md5()
        hash.update(body)
        ret = base64.b64encode(hash.digest()).strip()
        return ret.decode('utf8')

    @classmethod
    def to_sha1_base64(cls, stringToSign, secret):
        stringToSign = stringToSign.encode()
        secret = secret.encode()
        hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
        ret = base64.b64encode(hmacsha1.digest())
        return ret.decode('utf8')

    def run(self, type, image):
        if type == 0:
            image = 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1713763400,2547816042&fm=26&gp=0.jpg'
            body = {'type': 0, 'image_url': image}
        elif type == 1:
            body = {'type': 1, 'content': image}
        else:
            return None

        # 处理body
        body = json.dumps(body, separators=(',', ':'))
        body_md5 = self.to_md5_base64(body)

        # 处理headers
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'date': datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT"),
            'authorization': ''
        }
        stringToSign = 'POST' + '\n' + 'application/json' + '\n' + body_md5 + '\n' + 'application/json' + '\n' + headers['date'] + '\n' + '/image/tag'
        signature = self.to_sha1_base64(stringToSign, self.ak_secret)
        headers['authorization'] = 'Dataplus ' + self.ak_id + ':' + signature

        # 发起请求
        url = 'https://dtplus-cn-shanghai.data.aliyuncs.com/image/tag'
        res = requests.post(url=url, headers=headers, data=body)
        print('[DEBUG] ', res.status_code, res.text)
        return res.text


if __name__ == '__main__':
    ak_id = 'LTAIxFnjake9oXA1'
    ak_secret = '5Bbnfh0hr5wBvc3KpMHLNcfaCDRxAn'
    a = AliyunDataplus(ak_id=ak_id, ak_secret=ak_secret)
    a.run(type=0, image='https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1713763400,2547816042&fm=26&gp=0.jpg')
