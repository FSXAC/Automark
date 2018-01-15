"""
Auto-grading program for APSC 160
"""

import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

# Importing custom classes
import Highlighter
import CodeEdit
import SummaryTreeModel
import SummaryTreeView
import ActionManager

# Global constants
VERSION_NO = 'v0.2'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Initializes the UI componenets for the main window"""
        