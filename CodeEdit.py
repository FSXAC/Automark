"""
Main text editor docked window
"""

import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

class CodeEdit(QTextEdit):
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Initialzes UI elements"""
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor('#333'))
        palette.setColor(QPalette.Text, Qt.white)
        self.setPalette(palette)

        font = QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)