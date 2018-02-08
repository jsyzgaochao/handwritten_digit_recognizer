from PySide import QtCore, QtGui

class ResultLayout(QtGui.QHBoxLayout):
    def __init__(self, parent=None, id=None, text="", has_btn=True):
        super().__init__(parent)
        self.initUI(text, has_btn)
        self.id = id
        self.callback = None

    def initUI(self, text, has_btn):
        self.label = QtGui.QLabel(text)
        self.bar = QtGui.QProgressBar()
        self.bar.valueChanged.connect(self.valueChanged)
        self.addWidget(self.label)
        self.addWidget(self.bar)
        if has_btn:
            self.btn = QtGui.QPushButton()
            self.btn.clicked.connect(self.buttonClicked)
            self.addWidget(self.btn)

    def setText(self, text):
        self.label.setText(text)

    def setValue(self, value):
        self.bar.setValue(value)

    def setTextColor(self, color):
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.WindowText, color)
        self.label.setPalette(pal)

    def valueChanged(self, value):
        rate = 0.67 - 0.67 * value / (self.bar.maximum() - self.bar.minimum())
        DEFAULT_STYLE = """
        QProgressBar{
            border: 0px;
            text-align: center;
            color: black;
            background-color: transparent;
            padding: 2px;
        }

        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 hsva(%d, 255, 255, 255), stop:1 hsva(%d, 255, 255, 150));
            margin: 1px;
        }
        """ % (rate * 360, rate * 360)
        self.bar.setStyleSheet(DEFAULT_STYLE)

    def setCallback(self, callback):
        self.callback = callback

    def buttonClicked(self):
        if self.callback:
            self.callback(self.id)
