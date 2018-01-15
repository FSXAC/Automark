"""
Class that manages all the classes
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

class ActionManager():
    def __init__(self, parent):
        """Constructor"""
        self.openFolder = self.create_action('&Open Folder')
        self.parent = parent

    def create_action(
        self, 
        name, 
        checkable=False, 
        checked=False, 
        enabled=True,
        shortcut='',
        icon=''
        ):
        """Returns a QAction instance with ActionManager as parent"""
        new_action = QAction(name, self.parent)
        new_action.setCheckable(checkable)
        new_action.setChecked(checked)
        new_action.setEnabled(enabled)
        if shortcut != '':
            new_action.setShortcut(shortcut)
        if icon != '':
            action_icon = QIcon(icon)
            new_action.seticon(action_icon)
        return new_action
