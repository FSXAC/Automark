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

# Global constants
VERSION_NO = 'v0.2'