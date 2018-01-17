"""
Docked windows wrapper
"""

import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from SummaryTree import *

class CustomDock():
    def __init__(self, parent):
        self.parent = parent
        self.dock = QDockWidget(parent)
        self.content = QWidget()
        self.setupUi()
        self.add_to_parent()

    def setupUi(self):
        """UI setup"""
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Custom Dock')

    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

class SummaryDock(CustomDock):
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        cd_label = QLabel(self.content)
        cd_label.setText('Current Directory')
        cd_url = QLineEdit(self.content)
        cd_url.setReadOnly(True)
        cd_container = QHBoxLayout()
        cd_container.addWidget(cd_label)
        cd_container.addWidget(cd_url)
        v_layout = QVBoxLayout(self.content)
        v_layout.addLayout(cd_container)

        self.summary_tree_view = SummaryTree()
        self.summary_tree_view.selected.connect(
            lambda x: print(x)
        )
        v_layout.addWidget(self.summary_tree_view)

        # self.summary_tree_view = SummaryTreeView()
        # self.summary_tree_model = SummaryTreeModel(2, 0, self.summary_tree_view)

        # self.summary_tree_view.setModel(self.summary_tree_model)
        # self.summary_tree_view.selected.connect(
        #     lambda x: print(x)
        # )
        # v_layout.addWidget(self.summary_tree_view)


        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Submissions Summary')

    def add_to_parent(self):
        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

class SubmissionDock(CustomDock):
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        """Sets up the shows submission details"""
        l_name = QLabel(self.content)
        l_email = QLabel(self.content)
        l_id = QLabel(self.content)
        l_csid = QLabel(self.content)
        l_date = QLabel(self.content)
        l_name.setText('Name')
        l_email.setText('Email')
        l_id.setText('ID')
        l_csid.setText('CSID')
        l_date.setText('Date')

        t_name = QLineEdit(self.content)
        t_email = QLineEdit(self.content)
        t_id = QLineEdit(self.content)
        t_csid = QLineEdit(self.content)
        t_date = QLineEdit(self.content)
        t_name.setReadOnly(True)
        t_email.setReadOnly(True)
        t_id.setReadOnly(True)
        t_csid.setReadOnly(True)
        t_date.setReadOnly(True)

        # Add to grid layout
        layout = QGridLayout(self.content)
        layout.addWidget(l_name, 0, 0, 1, 1)
        layout.addWidget(t_name, 0, 1, 1, 1)
        layout.addWidget(l_email, 1, 0, 1, 1)
        layout.addWidget(t_email, 1, 1, 1, 1)
        layout.addWidget(l_id, 2, 0, 1, 1)
        layout.addWidget(t_id, 2, 1, 1, 1)
        layout.addWidget(l_csid, 3, 0, 1, 1)
        layout.addWidget(t_csid, 3, 1, 1, 1)
        layout.addWidget(l_date, 4, 0, 1, 1)
        layout.addWidget(t_date, 4, 1, 1, 1)

        # Self properties
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Submission Details')

    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        # self.dock.visibilityChanged.connect(
        #     lambda vis: self.parent.docked_visibility(
        #     )
        # )
        # TODO: Some kind of signal management

class VerdictDock(CustomDock):
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        """Setup UI"""
        l_mark = QLabel(self.content)
        l_mark.setText('Mark')
        sl_mark = QSlider(self.content)
        sl_mark.setMaximum(5)
        sl_mark.setOrientation(Qt.Horizontal)
        sl_mark.setTickPosition(QSlider.TicksBelow)
        sb_mark = QSpinBox(self.content)
        sb_mark.setMinimum(0)
        sb_mark.setMaximum(5)

        # Connect local signals between the slider and spinbox
        sl_mark.valueChanged.connect(
            lambda x: sb_mark.setValue(sl_mark.value()))
        sb_mark.valueChanged.connect(
            lambda x: sl_mark.setValue(sb_mark.value()))

        # Put all into grid
        layout = QGridLayout(self.content)
        layout.addWidget(l_mark, 0, 0, 1, 1)
        layout.addWidget(sl_mark, 0, 1, 1, 1)
        layout.addWidget(sb_mark, 0, 2, 1, 1)

        # Add to window
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Verdict')
    
    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock)
