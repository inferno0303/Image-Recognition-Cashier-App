from ui_xml import ui_main_window
from multi_thread import thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# 插件
import cv2
import json
import base64
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.ui = ui_main_window.Ui_Form()
        self.ui.setupUi(self)
        # 变量
        self.cv_srcImage = None
        self.lastTime = None
        # 线程相关
        self.MyThread_ = None
        self.MyThread2_ = None
        self.MyThread3_ = thread.MyThread3()
        self.MyThread3_.query_ok.connect(self._show_price)
        # 价格计算相关
        self.single_price = 0
        self.total_price = 0
        self.ui_init()

    def ui_init(self):
        self.ui.pushButton_open_file.clicked.connect(self.open_file)
        self.ui.pushButton_video_cap.clicked.connect(self.video_cap)
        self.ui.pushButton_calc.clicked.connect(self.add_price)
        self.ui.pushButton_cancel.clicked.connect(self.cancel_price)
        self.lastTime = time.time()
        self.setWindowIcon(QIcon('icon.png'))

    # TODO 使用图片检测
    def open_file(self):
        file_path, file_type = QFileDialog.getOpenFileName(QFileDialog(), '选择图片', '', '图像文件(*.jpg *.bmp *.png)')
        ui_image = QImage(file_path)
        if ui_image.width() < ui_image.height():
            ui_image = ui_image.scaledToWidth(self.ui.label_image_preview.width())
        else:
            ui_image = ui_image.scaledToHeight(self.ui.label_image_preview.height())
        self.ui.label_image_preview.setPixmap(QPixmap.fromImage(ui_image))
        # 静态识别
        self.ui.label_status.setText('状态：正在识别中')
        jpg_image = cv2.imread(file_path)
        jpg_image = cv2.imencode('.jpg', jpg_image)[1]
        base64_image = self._image_to_base64(jpg_image=jpg_image)
        self.MyThread2_ = thread.MyThread2_BD()
        self.MyThread2_.detect_ok.connect(self._query_price)
        self.MyThread2_.get_base64_image(base64_image=base64_image)
        self.MyThread2_.start()

    # TODO 使用视频检测
    def video_cap(self):
        self.MyThread_ = thread.MyThread()
        # TODO 连接槽函数
        self.MyThread_.preview_signal.connect(self._update_image_to_preview_label)
        self.MyThread_.capture_signal.connect(self._update_image_to_capture_label)
        self.MyThread_.key_signal.connect(self._trigger_detect)
        self.MyThread_.trigger_signal.connect(self._show_trigger_to_label)
        self.MyThread_.start()

    # TODO 计价
    def add_price(self):
        self.total_price += self.single_price
        self.ui.label_price.setText('总价：' + str(self.total_price) + '元')

    # TODO 取消计价
    def cancel_price(self):
        self.total_price = 0
        self.ui.label_price.setText('总价：' + str(self.total_price) + '元')

    # TODO 线程1的槽函数
    def _update_image_to_preview_label(self, ui_image):
        self.ui.label_image_preview.setPixmap(QPixmap.fromImage(ui_image))

    def _update_image_to_capture_label(self, ui_image):
        self.ui.label_image_capture.setPixmap(QPixmap.fromImage(ui_image))

    def _trigger_detect(self, jpg_image):
        now_time = time.time()
        if now_time - self.lastTime > 5:
            self.ui.label_status.setText('正在识别中...')
            base64_image = self._image_to_base64(jpg_image=jpg_image)
            self.MyThread2_ = thread.MyThread2_BD()
            self.MyThread2_.detect_ok.connect(self._query_price)
            self.MyThread2_.get_base64_image(base64_image=base64_image)
            self.MyThread2_.start()
            self.lastTime = now_time
        else:
            pass

    def _show_trigger_to_label(self, trigger_value):
        self.ui.label_trigger_value.setText('触发阈值：' + str(trigger_value * 100)[0:4] + '%')

    # TODO 线程2的槽函数
    def _query_price(self, api_resp):
        try:
            result = json.loads(api_resp)['result']
            # 阿里云api调试输出
            text = ''
            for i in result:
                text += i['keyword'] + ', ' + i['root'] + '，' + str(i['score']) + '\n'
            self.ui.textBrowser_debug.setText(text)
            # 查询价格
            keyword = result[0]['keyword']
            self.MyThread3_.get_keyword(keyword=keyword)
            self.MyThread3_.start()
        except Exception as e:
            print(e)
            self.ui.textBrowser_debug.setText('出错')

    # TODO 线程3的槽函数
    def _show_price(self, ret):
        self.ui.label_status.setText('')
        if ret['code'] == 0:
            msg = ret['msg']
            text = '品牌：' + msg['brand'] + '\n'\
                   + '商品名：' + msg['good_name'] + '\n'\
                   + '单价：' + str(msg['price']) + '\n'\
                   + '库存：' + str(msg['count']) + '\n'\
                   + '别名：' + msg['other_name'] + '\n'
            self.ui.label_good_info.setText(text)
            self.single_price = int(msg['price'])
        else:
            self.ui.label_good_info.setText('未识别到该商品')

    # TODO 封装的类方法
    @classmethod
    def _image_to_base64(cls, jpg_image=None):
        return base64.b64encode(jpg_image).decode()

