"""
Class that manages all the classes
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

# Constants
ACT_OPEN_FOLDER = '&Open Folder'
ACT_QUIT = '&Quit'

ACT_VIEW_SUMMARY = 'Summary'
ACT_VIEW_SUBMISSION = 'Submission'
ACT_VIEW_NOTE = 'Note'
ACT_VIEW_VERDICT = 'Verdict'

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
            new_action.setIcon(action_icon)
        return new_action

    def make_actions(self):
        """Instantiates all the necessary actions required to run the app"""

        # File actions
        self.act_open_folder = self.create_action(ACT_OPEN_FOLDER, icon='hi.png', shortcut='Ctrl+O')
        self.act_quit = self.create_action(ACT_QUIT, shortcut='Ctrl+Q')

        # View actions
        self.act_view_summary = self.create_action('Summary', checkable=True, checked=True)
        self.act_view_submission = self.create_action('Submission', checkable=True, checked=True)
        self.act_view_note = self.create_action('Note', checkable=True, checked=True)
        self.act_view_verdict = self.create_action('Verdict', checkable=True, checked=True)

        # Compilation actions
        self.act_compile_run = self.create_action('Compile and Run')

    def get_file_actions(self):
        """Returns a set of actions that needs to be populated in the File menu"""
        return_list = [
            self.act_open_folder,
            '/',
            self.act_quit
        ]
        return return_list

    def get_view_actions(self):
        """Returns a set of actions that needs to be populated in the View menu"""
        return_list = [
            self.act_view_summary,
            self.act_view_submission,
            self.act_view_note,
            self.act_view_verdict
        ]
        return return_list

    def get_run_actions(self):
        """Returns a set of actions that needs to be populated in the Run menu"""
        return_list = [
            self.act_compile_run
        ]
        return return_list