from PySide import QtCore, QtGui
import numpy as np
import cv2

class Paint(QtGui.QWidget):
    def __init__(self, parent=None, size=(256, 256)):
        super(Paint, self).__init__(parent)
        self.initUI(size=size)
        self.pos_xy = []
        self.drawing = False
        self.callback = None
        self.linewidth = min(size) / 25.

    def initUI(self, size):
        self.setFixedSize(size[0], size[1])
        self.setWindowTitle('Paint')
        self.setMouseTracking(False)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette().Background, QtCore.Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.pos_xy.append((event.pos().x(), event.pos().y()))
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pos_xy.append((-1, -1))
            self.drawing = False
            self.update()
            if self.callback:
                self.callback(self.getImageArray())
        elif event.button() == QtCore.Qt.RightButton:
            self.pos_xy = []
            self.drawing = False
            self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
        elif event.button() == QtCore.Qt.RightButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtCore.Qt.black, self.linewidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        last_pos = (-1, -1)
        for cur_pos in self.pos_xy:
            if last_pos != (-1, -1) and cur_pos != (-1, -1):
                painter.drawLine(last_pos[0], last_pos[1], cur_pos[0], cur_pos[1])
            last_pos = cur_pos

    def getImageArray(self, size=(28, 28), padding=0.2):
        qimage = QtGui.QPixmap.grabWidget(self).toImage()
        qimage = qimage.convertToFormat(QtGui.QImage.Format.Format_RGB888)
        width, height, ptr = qimage.width(), qimage.height(), qimage.constBits()
        image = np.array(ptr).reshape(height, width, 3)
        image = 1. - np.mean(image, axis=2) / 255.
        col_sum, row_sum = np.sum(image, axis=0), np.sum(image, axis=1)
        col_nz, row_nz = np.argwhere(col_sum > 1e-3).reshape(-1), np.argwhere(row_sum > 1e-3).reshape(-1)
        if col_nz.shape[0] == 0 or row_nz.shape[0] == 0:
            return None
        nz_left, nz_right = np.min(col_nz), np.max(col_nz)
        nz_top, nz_bottom = np.min(row_nz), np.max(row_nz)
        sub_image = image[nz_top:nz_bottom, nz_left:nz_right]
        shape = sub_image.shape
        shape_diff = abs(sub_image.shape[1] - sub_image.shape[0])
        if shape[0] < shape[1]:
            sub_image = np.pad(sub_image, ((shape_diff - shape_diff//2, shape_diff//2), (0, 0)), "constant")
        elif shape[0] > shape[1]:
            sub_image = np.pad(sub_image, ((0, 0), (shape_diff - shape_diff//2, shape_diff//2)), "constant")
        pad = int((sub_image.shape[0] * padding) // 2)
        sub_image = np.pad(sub_image, ((pad, pad), (pad, pad)), "constant")
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        sub_image = cv2.morphologyEx(sub_image, cv2.MORPH_CLOSE, kernel)
        sub_image = cv2.GaussianBlur(sub_image, (7, 7), 2.0)
        sub_image = cv2.resize(sub_image, size, interpolation=cv2.INTER_AREA)
        sub_image = cv2.GaussianBlur(sub_image, (3, 3), 0.5)
        sub_image = 1. * (sub_image > .3)
        return sub_image

    def saveImage(self, filename):
        qimage = QtGui.QPixmap.grabWidget(self).toImage()
        qimage.save(filename)
        pass

    def setCallback(self, callback):
        self.callback = callback


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    paint = Paint()
    sys.exit(app.exec_())
