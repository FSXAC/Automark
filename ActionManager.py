"""
Class that manages all the classes
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

class ActionManager():
    def __init__(self, parent):
        """Constructor"""
        self.parent = parent
        self.make_actions()

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

    def make_actions(self):
        """ Instantiates all the necessary actions required to run the app"""
        
        # File actions
        self.act_open_folder = self.create_action('&Open Folders', icon='hi.png', shortcut='Ctrl+O')
        self.act_quit = self.create_action('&Quit', shortcut='Ctrl+Q')

        # View actions
        self.act_view_summary = self.create_action('Folders', checkable=True, checked=True)
        self.act_view_submission = self.create_action('Submission', checkable=True, checked=True)
        self.act_view_note = self.create_action('Note', checkable=True, checked=True)
        self.act_view_verdict = self.create_action('Verdict', checkable=True, checked=True)

        # Compilation actions
        self.act_compile_run = self.create_action('Compile and Run')
        
