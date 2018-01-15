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
from Highlighter import *
from CodeEdit import *
# import SummaryTreeModel
# import SummaryTreeView
# import ActionManager

# Global constants
VERSION_NO = 'v0.2'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Initializes the UI componenets for the main window"""

        # Menu bar and status bar
        self.setMenuBar(QMenuBar(self))
        self.setStatusBar(QStatusBar(self))

        # Set central widget to textedit with highlighter
        self.text_edit = CodeEdit()
        self.highlighter = Highlighter(self.text_edit.document())
        self.setCentralWidget(self.text_edit)

        # Show window
        self.resize(1440, 800)
        self.show()

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())