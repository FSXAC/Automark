import sys
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

VERSION_NO = 'v0.0'

class AutomarkWidget(QWidget):
    def __init__(self):
        super(AutomarkWidget, self).__init__()
        
        self.setupUi()
    
    def setupUi(self):
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Using main automark widget as central widget
        self.am = AutomarkWidget()
        self.setCentralWidget(self.am)
        self.setWindowTitle('Automark ' + VERSION_NO)
        self.setupUi()

    def setupUi(self):
        # menuBar = self.menuBar()
        self.resize(600, 400)
        self.show()

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
