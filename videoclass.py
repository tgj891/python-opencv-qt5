import numpy as np
import cv2, threading
import sys, time, shutil
from PyQt5 import QtCore, QtGui, QtWidgets
#页面
#视屏
class VideoQt:
    def __init__(self, name):
        self.name = name
        self.stop = 0 #关闭摄像头
        self.videodo = 0 #录像
        self.facedo = 0 #人脸识别
        self.index = 0
        # 获取训练好的人脸参数数据
        self.face_cascade = cv2.CascadeClassifier(r'D:\MySoft\Anaconda3\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        self.videojpg = "video.jpg"
        self.camerajpg = "camera.jpg"
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 设置编码
    #-----------------人脸检测---------------------------#
    def facecheck(self):
        if self.facedo == 1:

            #图片转换成灰度图片
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            #探测图片中的人脸
            faces = self.face_cascade.detectMultiScale(
                gray,
                1.5,
                3
            )
            for (x, y, w, h) in faces:
                self.index += 1
                cv2.imwrite("./face%i.jpg"%self.index, self.frame[y:y+h,x:x+w]) #保存识别到的人脸
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
                #cv2.circle(self.frame, (int((x + x + w) / 2), int((y + y + h) / 2)), int(w / 2), (0, 255, 0), 2)

    # ----------------视频------------------------#
    def lu_video(self):#录像中
        if self.videodo == 1:
            # videoframe = cv2.flip(frame, 0) #视频翻转 0flipCode==0垂直翻转（沿X轴翻转），flipCode>0水平翻转（沿Y轴翻转），flipCode<0水平垂直翻转（先沿X轴翻转，再沿Y轴翻转，等价于旋转180°）
            self.out.write(self.frame)

    def videoing(self):#线程处理函数
        #self.cap = cv2.VideoCapture(r"E:\360Downloads\test.mp4")
        self.cap = cv2.VideoCapture(0) #打开摄像头0,1依次；可以是视屏地址
        while True:
            if self.cap.isOpened() != True:
                self.cap.open(0)
            # Capture frame-by-frame
            ret, self.frame = self.cap.read()
            if ret == True:
                self.lu_video() #录像
                self.facecheck() #人脸识别
                #gray = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                # Display the resulting frame
                #cv2.imshow('frame', gray)
                #设置图片缩放
                cv2.imwrite(self.videojpg, self.frame)
                pixmap = QtGui.QPixmap(self.videojpg)
                scaredPixmap = pixmap.scaled(640, 480, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.videolabel.setPixmap(scaredPixmap)
            else:
                continue

            cv2.waitKey(1)
            if self.stop == 1: #关闭视频
                break

    def open_video(self):#视频采集线程
        self.stop = 0
        thread = threading.Thread(target=self.videoing, name="video")
        thread.start()
        self.thread = thread

    def threadjoin(self):
        self.thread.join()

    def close_video(self):#关闭视频
        self.stop = 1
        self.cap.release()
        cv2.destroyAllWindows()
    #照相
    def camera_do(self):
        cv2.imwrite(self.camerajpg, self.frame)
        pixmapcamera = QtGui.QPixmap(self.camerajpg)
        scaredpix = pixmapcamera.scaled(259, 262, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaredpix)

    #开始录像
    def start_video(self):
        if self.videodo == 0:
            self.out = cv2.VideoWriter('output.avi', self.fourcc, 25.0, (640, 480))
            self.videoButton.setText(self._translate("Form", "停止录像"))
            self.videodo = 1
        else:
            self.videoButton.setText(self._translate("Form", "开始录像"))
            self.videodo = 0
            self.out.release()
    #人脸识别
    def start_facecheck(self):
        if self.facedo == 0:
            self.faceButton.setText(self._translate("Form", "关闭人脸识别"))
            self.facedo = 1
        else:
            self.faceButton.setText(self._translate("Form", "开始人脸识别"))
            self.facedo = 0

    #---------------qt页面-------------------------#
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(923, 500)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 640, 480))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videolabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.videolabel.setAutoFillBackground(True)
        self.videolabel.setGeometry(0, 0, 640, 480)
        self.videolabel.setScaledContents(False)
        self.videolabel.setObjectName("videolabel")
        self.horizontalLayout.addWidget(self.videolabel)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(650, 10, 261, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAutoFillBackground(True)
        self.label.setGeometry(0, 0, 259, 262)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.openButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(self.open_video)
        self.verticalLayout.addWidget(self.openButton)
        self.closeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close_video)
        self.verticalLayout.addWidget(self.closeButton)
        self.cameraButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cameraButton.setObjectName("cameraButton")
        self.cameraButton.clicked.connect(self.camera_do)
        self.verticalLayout.addWidget(self.cameraButton)
        self.videoButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.videoButton.setObjectName("videoButton")
        self.videoButton.clicked.connect(self.start_video)
        self.verticalLayout.addWidget(self.videoButton)
        self.faceButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.faceButton.setObjectName("faceButton")
        self.faceButton.clicked.connect(self.start_facecheck)
        self.verticalLayout.addWidget(self.faceButton)
        self.quitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.quitButton.setObjectName("quitButton")
        self.verticalLayout.addWidget(self.quitButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        self._translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(self._translate("Form", "视频采集"))
        self.videolabel.setText(self._translate("Form", "摄像区"))
        self.label.setText(self._translate("Form", "照相区"))
        self.openButton.setText(self._translate("Form", "打开摄像头"))
        self.closeButton.setText(self._translate("Form", "关闭摄像头"))
        self.cameraButton.setText(self._translate("Form", "照相"))
        self.videoButton.setText(self._translate("Form", "开始录像"))
        self.faceButton.setText(self._translate("Form", "开始人脸识别"))
        self.quitButton.setText(self._translate("Form", "退出"))
