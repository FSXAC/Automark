"""
Class that manages all the classes
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

# Constants
ACT_OPEN_FOLDER = '&Open Folder'
ACT_FILE_SAVE = 'Save File'
ACT_QUIT = '&Quit'

ACT_VIEW_SUMMARY = 'Summary'
ACT_VIEW_SUBMISSION = 'Submission'
ACT_VIEW_NOTE = 'Note'
ACT_VIEW_VERDICT = 'Verdict'

ACT_COMPILE_CLEAN = 'Clean'
ACT_COMPILE_RUN = 'Run'
ACT_COMPILE_ALL = 'Compile All'

ACT_MARK_LOAD_RUBRIC = 'Load Rubric'


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
        self.act_save_document = self.create_action(ACT_FILE_SAVE, shortcut='Ctrl+S')
        self.act_quit = self.create_action(ACT_QUIT, shortcut='Ctrl+Q')

        # View actions
        self.act_view_summary = self.create_action('Summary', checkable=True, checked=True)
        self.act_view_submission = self.create_action('Submission', checkable=True, checked=True)
        self.act_view_note = self.create_action('Note', checkable=True, checked=True)
        self.act_view_verdict = self.create_action('Verdict', checkable=True, checked=True)

        # Compilation actions
        self.act_compile_clean = self.create_action(ACT_COMPILE_CLEAN, shortcut='Ctrl+0')
        self.act_compile_run = self.create_action(ACT_COMPILE_RUN, shortcut='Ctrl+R')
        self.act_compile_all = self.create_action(ACT_COMPILE_ALL, shortcut='Ctrl+Shift+R')
        self.act_compile_all.setEnabled(False)  #TODO: WIP

        # Marking actions
        self.act_mark_load_rubric = self.create_action(ACT_MARK_LOAD_RUBRIC)


    def get_file_actions(self):
        """Returns a set of actions that needs to be populated in the File menu"""
        return_list = [
            self.act_open_folder,
            self.act_save_document,
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
            self.act_compile_clean,
            self.act_compile_all,
            self.act_compile_run
        ]
        return return_list

    def get_marking_actions(self):
        """Returns actions related to marking"""
        return_list = [
            self.act_mark_load_rubric
        ]
        return return_list