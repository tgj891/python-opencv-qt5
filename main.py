import videoclass, sys
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    #初始化视屏和页面
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    video = videoclass.VideoQt("video")
    video.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
