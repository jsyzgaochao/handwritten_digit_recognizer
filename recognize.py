from PySide import QtCore, QtGui
from paint import Paint
from result_layout import ResultLayout
from tf_predict import TfPredict
import numpy as np
import os
import sys
import time
import hashlib

class PaintApp(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PaintApp, self).__init__(parent)
        self.initUI()
        self.tf = TfPredict()

    def initUI(self):
        self.setFixedSize(520, 280)
        self.setWindowTitle("Handwritten Digit Recognizer")
        self.mainLayout = QtGui.QHBoxLayout()
        self.paint = Paint()
        self.resultLayout = QtGui.QVBoxLayout()
        self.resultLayout.setContentsMargins(10,0,0,0)
        self.subResultLayouts = []

        for i in range(10):
            curResultLayout = ResultLayout(id=i, text=str(i)+":")
            curResultLayout.setValue(0)
            self.resultLayout.addLayout(curResultLayout)
            self.subResultLayouts.append(curResultLayout)

        self.mainLayout.addWidget(self.paint)
        self.mainLayout.addLayout(self.resultLayout)

        self.setLayout(self.mainLayout)
        self.show()

    def setPaintCallback(self, callback):
        self.paint.setCallback(callback)

    def setResultCallback(self, callback):
        for i in range(10):
            curResultLayout = self.subResultLayouts[i]
            curResultLayout.setCallback(callback)

if __name__ == '__main__':
    def paintCallback(image):
        if image is None:
            return
        image = np.reshape(image, (1, 784))
        result = paintapp.tf.predict(image)
        result = np.reshape(result, (-1,))
        res_max = np.argmax(result)
        for i in range(len(paintapp.subResultLayouts)):
            curResultLayout = paintapp.subResultLayouts[i]
            curResultLayout.setValue(result[i] * 100)
            color = QtCore.Qt.red if i == res_max else QtCore.Qt.black
            curResultLayout.setTextColor(color)

    def resultCallback(id):
        path = "img/%d/"%id
        if not os.path.exists("img/"):
            os.mkdir("img/")
        if not os.path.exists(path):
            os.mkdir(path)
        md5 = hashlib.md5()
        md5.update(str(time.time()).encode("utf8"))
        filename = md5.hexdigest()
        paintapp.paint.saveImage(path+filename+".png")

    app = QtGui.QApplication(sys.argv)
    paintapp = PaintApp()
    paintapp.setPaintCallback(paintCallback)
    paintapp.setResultCallback(resultCallback)
    sys.exit(app.exec_())
