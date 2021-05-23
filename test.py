import cv2
import numpy as np

# Laplace锐化核
kernel = np.array([[0, -1.5, 0], [-1.5, 7, -1.5], [0, -1.5, 0]], np.float)


capture = cv2.VideoCapture(0)
ret, frame = capture.read()
frame = cv2.flip(frame, flipCode=1)
background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, ksize=(3, 3), sigmaX=0, sigmaY=0)
background = cv2.filter2D(src=background, ddepth=cv2.CV_16S, kernel=kernel)
background = cv2.convertScaleAbs(background)
print('背景已储存')

while True:
    # 读图像帧
    ret, frame = capture.read()
    # 镜像（我是前置摄像头，所以需要镜像（滑稽））
    frame = cv2.flip(frame, flipCode=1)
    # 帧转灰度
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, ksize=(3, 3), sigmaX=0, sigmaY=0)
    frame_gray = cv2.filter2D(src=frame_gray, ddepth=cv2.CV_16S, kernel=kernel)
    frame_gray = cv2.convertScaleAbs(frame_gray)

    # 计算残差图像
    diff_gray = cv2.absdiff(frame_gray, background)
    # diff_gray = cv2.GaussianBlur(diff_gray, ksize=(3, 3), sigmaX=0, sigmaY=0)
    # diff_gray = cv2.filter2D(src=diff_gray, ddepth=cv2.CV_16S, kernel=kernel)
    # diff_gray = cv2.convertScaleAbs(diff_gray)
    # 阈值化
    ret, diff_bin = cv2.threshold(diff_gray, 50, 255, cv2.THRESH_BINARY)
    # 计算阈值化后，白点数
    diff_pix_num = np.sum(diff_bin == 255)
    # 判断是否需要抓拍（计算阈值）
    trigger = round(diff_pix_num / diff_bin.size, 4)
    # 打印一下
    print('差异百分比', trigger)
    # 预览
    cv2.imshow('background', background)
    cv2.imshow('current frame', frame_gray)
    cv2.imshow('diff gray', diff_gray)
    cv2.imshow('diff bin', diff_bin)
    cv2.waitKey(1)
