"""
Customized tree view to view all files in summary
"""

import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

class SummaryTreeView(QTreeView):
    """Tree view used to show all submissions in summary mode"""

    # Signals
    selected = pyQtsignal(str)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Initializes UI elements"""
        self.clicked.connect(self.onClicked)

    def onClicked(self, item_index):
        """Event handler for when something is clicked"""
        if self.model() is None:
            return

        item = self.model().item(item_index.row())
        print(item.text())
        self.selected.emit(item.text())

    def add_entry(self, sid, status):
        """Add a single entry to the tree model"""
        if self.model() is not SummaryTreeModel:
            return

        self.model().add_entry(sid, status)

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
        self.insertRow(0)
        self.setData(self.model().index(0, self.SID), sid)
        self.setData(self.model().index(0, self.STATUS), status)
        self.item(0, self.SiD).setEditable(False)
        self.item(0, self.STATUS).setEditable(False)
