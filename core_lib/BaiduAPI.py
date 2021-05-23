# version： 20190529

import base64
import requests


class BaiduAPI:
    def __init__(self):
        pass

    def run(self, access_token, base64_image):
        # url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=WotPXH77INr67MFZSdP8cljq&client_secret=ABL6wycYTI9qKzCwGjHKVC3FWH0bdXVk'
        # headers = {
        #     'Content-Type': 'application/json; charset=UTF-8',
        # }
        # res = requests.post(url=url, headers=headers)
        # print('[DEBUG1] ', res.status_code, res.text)

        base_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=' + access_token
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        body = {'image': base64_image, 'baike_num': 0}
        resp = requests.post(url=base_url, headers=headers, data=body)
        print('[DEBUG2] ', resp.text)
        return resp.text


if __name__ == '__main__':
    fp = open('../test_images/4.jpg', 'rb').read()
    a = BaiduAPI()
    a.run(access_token='24.96531e7a1ea0c73d8dee1527c1ec13d9.2592000.1561658739.282335-16361601', base64_image=base64.b64encode(fp).decode())
