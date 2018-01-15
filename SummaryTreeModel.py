"""
Custom standard item model for the summary tree view
"""
import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

class SummaryTreeModel(QStandardItemModel):
    """Custom standard item model for submissions"""

    # Index enumeration
    SID, STATUS = range(2)

    def __init__(self, col, row, parent=None):
        """Constructor"""
        super().__init__(col, row, parent)

        # Set headers
        self.setHeaderData(self.SID, Qt.Horizontal, 'ID')
        self.setHeaderData(self.STATUS, Qt.Horizontal, 'Status')

    def add_entry(self, sid, status):
        """Add a single item entry to the tree model"""
        self.insertRow(0)
        self.setData(self.model().index(0, self.SID), sid)
        self.setData(self.model().index(0, self.STATUS), status)
        self.item(0, self.SiD).setEditable(False)
        self.item(0, self.STATUS).setEditable(False)
