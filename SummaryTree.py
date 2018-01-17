"""
Custom standard item model for the summary tree view
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

class SummaryTree(QTreeView):
    SID, STATUS = range(2)

    # Signals
    selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.add_entry('p5h0b', 'not done')

    def setupUi(self):
        self.setModel(self.create_summary_model())
        self.clicked.connect(self.item_select_event)

    def create_summary_model(self):
        model = QStandardItemModel(0, 2, self)
        model.setHeaderData(self.SID, Qt.Horizontal, 'ID')
        model.setHeaderData(self.STATUS, Qt.Horizontal, 'Status')
        return model

    def item_select_event(self, model_index):
        item = self.model().item(model_index.row())
        print(item.text())
        self.selected.emit(item.text())
    
    def add_entry(self, sid, status):
        self.model().insertRow(0)
        self.model().setData(self.model().index(0, self.SID), sid)
        self.model().setData(self.model().index(0, self.STATUS), status)
        self.model().item(0, self.SID).setEditable(False)
        self.model().item(0, self.STATUS).setEditable(False)

    def reset_model(self):
        self.setModel(self.create_summary_model())
