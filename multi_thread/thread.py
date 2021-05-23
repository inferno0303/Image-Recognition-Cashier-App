from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import *
import numpy as np
import cv2
import json
from core_lib import AliyunDataplus
from core_lib import BaiduAPI
import requests


class MyThread(QThread):
    capture_signal = pyqtSignal(object)
    preview_signal = pyqtSignal(object)
    key_signal = pyqtSignal(object)
    trigger_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.working = True
        self.background = None

    def run(self):
        # 拍摄一张图片作为背景图
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()
        frame = cv2.flip(frame, flipCode=1)
        self.background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        while self.working:
            ret, frame = capture.read()
            frame = cv2.flip(frame, flipCode=1)
            # time.sleep(0.5)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            diff_gray = cv2.absdiff(frame_gray, self.background)
            ret, diff_bin = cv2.threshold(diff_gray, 50, 255, cv2.THRESH_BINARY)
            diff_pix_num = np.sum(diff_bin == 255)

            # 转换QImage
            ui_image = QImage(frame_rgb, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888).scaledToWidth(500)
            # 发送到预览
            self.preview_signal.emit(ui_image)
            # 判断是否需要抓拍
            trigger = round(diff_pix_num / diff_bin.size, 4)
            self.trigger_signal.emit(trigger)
            if trigger > 0.2:
                self.capture_signal.emit(ui_image)
                self.key_signal.emit(cv2.imencode('.jpg', frame_rgb)[1])  # 编码并发送到槽函数


# TODO ALIYUNDATAPLUS
class MyThread2(QThread):
    detect_ok = pyqtSignal(object)

    def __init__(self):
        super().__init__(parent=None)
        self.inst = AliyunDataplus.AliyunDataplus(ak_id='LTAIxFnjake9oXA1', ak_secret='5Bbnfh0hr5wBvc3KpMHLNcfaCDRxAn')
        self.base64_image = None

    def run(self) -> None:
        if self.base64_image is not None:
            api_resp = self.inst.run(type=1, image=self.base64_image)
            self.detect_ok.emit(str(api_resp))

    def get_base64_image(self, base64_image):
        self.base64_image = base64_image


# TODO FUCK BAIDU API
class MyThread2_BD(QThread):
    detect_ok = pyqtSignal(object)

    def __init__(self):
        super(MyThread2_BD, self).__init__(parent=None)
        self.base64_image = None
        self.inst = BaiduAPI.BaiduAPI()

    def run(self) -> None:
        if self.base64_image is not None:
            api_resp = self.inst.run(access_token='24.96531e7a1ea0c73d8dee1527c1ec13d9.2592000.1561658739.282335-16361601', base64_image=self.base64_image)
            self.detect_ok.emit(str(api_resp))

    def get_base64_image(self, base64_image):
        self.base64_image = base64_image


class MyThread3(QThread):
    query_ok = pyqtSignal(object)

    def __init__(self):
        super().__init__(parent=None)
        self.keyword = None

    def get_keyword(self, keyword):
        self.keyword = keyword

    def run(self) -> None:
        base_url = 'http://lsy.imyx.top:81/service/query_price_info?keyword=' + str(self.keyword)
        resp = requests.get(url=base_url)
        if resp.status_code == 200:
            ret = resp.content.decode('unicode_escape')
            print('[DEBUG2] ', ret)
            self.query_ok.emit(json.loads(ret))
        else:
            print('线程3网络问题', resp.status_code)
