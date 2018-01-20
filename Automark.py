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
from ActionManager import *
from Docked import *
from Project import *

# Global constants
VERSION_NO = 'v0.3'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

        self.project = Project()

    def setupUi(self):
        """Initializes the UI componenets for the main window"""
        # Actions
        self.action_manager = ActionManager(self)

        # Menu bar and status bar
        self.setMenuBar(QMenuBar(self))
        self.setStatusBar(QStatusBar(self))
        self.create_menus()
        self.create_toolbars()

        # Set central widget to textedit with highlighter
        self.text_edit = CodeEdit()
        self.highlighter = Highlighter(self.text_edit.document())
        self.setCentralWidget(self.text_edit)

        # Create docked widgets
        self.create_docked_widgets()

        # Show window
        self.setWindowTitle('Automark ' + VERSION_NO)
        self.resize(1440, 800)
        self.show()

    def create_menus(self):
        """Creates the menus for the main app"""

        # Lambda expression for quickly getting a new menu
        new_menu = lambda name: self.menuBar().addMenu(name)

        # Closure for populating menu with actions
        def populate_menu(menu, action_list, signal_handler):
            """Given a menu, populate the menu with actions and connect to a signal handler"""

            # Iterate through action list and add them to the menus
            for action in action_list:
                if action == '/':
                    # Separator
                    menu.addSeparator()
                else:
                    # Valid action
                    menu.addAction(action)

            # Add a signal handler to the menu
            menu.triggered.connect(signal_handler)

        # Actually go and make the menus
        populate_menu(
            new_menu('&File'),
            self.action_manager.get_file_actions(),
            self.file_menu_handler
        )
        populate_menu(
            new_menu('&View'),
            self.action_manager.get_view_actions(),
            self.view_menu_handler
        )
        populate_menu(
            new_menu('&Run'),
            self.action_manager.get_run_actions(),
            self.run_menu_handler
        )
        populate_menu(
            new_menu('&Marking'),
            self.action_manager.get_marking_actions(),
            self.marking_menu_handler
        )

    def create_toolbars(self):
        """Creates the toolbars for the main app"""

        # Assuming that every action in a tool bar already
        # exists in a menu
        def populate_toolbar(toolbar, action_list):
            """Given a toolbar, popuate it with actions"""

            for action in action_list:
                if action == '/':
                    # Separator
                    toolbar.addSeparator()
                else:
                    toolbar.addAction(action)

            # Apply toolbar style
            toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Make actual toolbars
        populate_toolbar(self.addToolBar('Files'), self.action_manager.get_file_actions())
        populate_toolbar(self.addToolBar('Run'), self.action_manager.get_run_actions())
        populate_toolbar(self.addToolBar('Marking'), self.action_manager.get_marking_actions())

    def create_docked_widgets(self):
        """Make docked widgets"""
        self.summary_dock = SummaryDock(self)
        self.submission_dock = SubmissionDock(self)
        self.note_dock = NoteDock(self)
        self.verdict_dock = VerdictDock(self)

        # Connect dock signals to actions (that need to be updated)
        self.summary_dock.connect_visiblity_action(self.action_manager.act_view_summary.setChecked)
        self.submission_dock.connect_visiblity_action(self.action_manager.act_view_submission.setChecked)
        self.note_dock.connect_visiblity_action(self.action_manager.act_view_note.setChecked)
        self.verdict_dock.connect_visiblity_action(self.action_manager.act_view_verdict.setChecked)

        # Other signals
        self.summary_dock.connect_selected(self.select_submission_handler)

    # HANDLERS AND SLOTS
    def file_menu_handler(self, sender):
        """Handles events from the file menu and its corresponding actions"""
        signal = sender.text()
        if signal == ACT_OPEN_FOLDER:
            # print('Open folder')
            self.open_folder()
        elif signal == ACT_QUIT:
            qApp.quit()

    def view_menu_handler(self, sender):
        """Handles actions related to views"""
        signal = sender.text()
        visible = sender.isChecked()
        if signal == ACT_VIEW_SUMMARY:
            self.summary_dock.set_visible(visible)
        elif signal == ACT_VIEW_SUBMISSION:
            self.submission_dock.set_visible(visible)
        elif signal == ACT_VIEW_NOTE:
            self.note_dock.set_visible(visible)
        elif signal == ACT_VIEW_VERDICT:
            self.verdict_dock.set_visible(visible)

    def run_menu_handler(self, sender):
        """Run menu hander"""
        signal = sender.text()
        if signal == ACT_COMPILE_RUN:
            self.project.compile_and_run()

    def marking_menu_handler(self, sender):
        """Marking menu handler"""
        signal = sender.text()
        if signal == ACT_MARK_LOAD_RUBRIC:
            # self.verdict_dock.clear_rubric()
            self.open_rubric()

    def default_menu_handler(self, sender):
        """Temporary default menu handler"""
        print(sender.text())

    def open_folder(self):
        """Opens a directory to be marked"""
        fdir = QFileDialog.getExistingDirectory(
            self, 'Select Folder', os.getenv('HOME'),
            QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        )

        if fdir == '':
            return

        # Create a new project with that directory
        return_code = self.project.new_project(fdir)
        if return_code == PROJ_EMPTY_PATH:
            self.call_message_box(info=PROJ_EMPTY_PATH)
            return
        elif return_code == PROJ_EMPTY_DIR:
            self.call_message_box(info='No files found in the directory')
            return
        elif return_code == PROJ_VALID:
            print('Project directory loaded')

        # Get submissions
        self.summary_dock.summary_tree_view.load_submissions(self.project.get_submissions())

        # Let the user know
        self.statusBar().showMessage('Opened at ' + fdir)

    def select_submission_handler(self, item):
        """Handler for when a submission in the summary dock is clicked"""
        self.project.set_submission(item)
        self.text_edit.setText(self.project.get_submission_code())
        self.note_dock.set_note(self.project.get_submission_note())

    def open_rubric(self):
        """Opens a file directory dialog to get rubric json"""
        fdir = QFileDialog.getOpenFileName(
            self, 'Select rubric JSON', os.getenv('HOME'),
            'JSON (*.json)'
        )
        fname = fdir[0]
        if fname != '':
            self.project.load_rubric(fname)
            # self.verdict_dock.load_rubric(self.project.get_parsed_rubric())

        self.statusBar().showMessage('Rubric loaded from '+ fname)

    # UTILITY FUNCTIONS
    def call_message_box(
            self,
            txt='Warning',
            info='Something is wrong',
            title='Warning'
        ):
        """Create a message box"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(txt)
        msg.setInformativeText(info)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
