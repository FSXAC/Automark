"""This is an auto grader program hopefully by used for APSC 160"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Global constants
VERSION_NO = 'v0.0a'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Automark ' + VERSION_NO)
        self.setupUi()

    def setupUi(self):
        """Sets up nearly all of the front-end components"""
        # Menu and status bar
        self.menubar = QMenuBar(self)
        self.statusbar = QStatusBar(self)
        menuFile = self.menubar.addMenu('File')
        menuView = self.menubar.addMenu('View')
        self.setupMenuFile(menuFile)
        self.setupMenuView(menuView)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)

        # Toolbar
        self.toolbar = self.addToolBar('Files')

        # Docks
        self.setupDocks()

        # Central widget
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)

        # Window
        self.resize(1440, 800)
        self.show()

    def setupMenuFile(self, menu):
        """Setup a particular set of actions and its menus"""
        self.actionOpenFolder = QAction('&Open Folder', self)
        self.actionQuit = QAction('&Quit', self)

        # Add menu actions to menu
        menu.addAction(self.actionOpenFolder)
        menu.addSeparator()
        menu.addAction(self.actionQuit)

        # Bind signals from actions to slots
        menu.triggered.connect(self.menuFileHandler)
    
    def setupMenuView(self, menu):
        """Setup view related actions and menu items"""
        menu.triggered.connect(self.menuViewHandler)

    def setupDocks(self):
        """Setup dockable widgets"""
        self.setupDockFolders()
        self.setupDockFiles()
        self.setupDockSubmission()
        self.setupDockOutput()
        self.setupDockVerdict()

    def setupDockFolders(self):
        """Setup docking widget that shows all the folders"""
        self.dockFolders = QDockWidget(self)
        self.dockFoldersContent = QWidget()
        
        # Directory indicator at the top
        cdLabel = QLabel(self.dockFoldersContent)
        cdLabel.setText('Current Directory')
        cdURL = QLineEdit(self.dockFoldersContent)
        cdURL.setReadOnly(True)
        cdContainer = QHBoxLayout()
        cdContainer.addWidget(cdLabel)
        cdContainer.addWidget(cdURL)

        # List view
        foldersList = QListView(self.dockFoldersContent)

        # Add everything together in a vertical layout
        vLayout = QVBoxLayout(self.dockFoldersContent)
        vLayout.addLayout(cdContainer)
        vLayout.addWidget(foldersList)

        # Add dock widget to main window
        self.dockFolders.setWidget(self.dockFoldersContent)
        self.dockFolders.setWindowTitle('Folders')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFolders)

    def setupDockFiles(self):
        """Setup dokcing widget that shows files in the folder selected"""
        self.dockFiles = QDockWidget(self)
        self.dockFilesContents = QWidget()

        # List view
        filesList = QListView(self.dockFilesContents)

        # Add to layout
        layout = QVBoxLayout(self.dockFilesContents)
        layout.addWidget(filesList)
        self.dockFiles.setWidget(self.dockFilesContents)
        self.dockFiles.setWindowTitle('Files')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFiles)

    def setupDockSubmission(self):
        """Setup dock that shows student information"""
        self.dockSubmission = QDockWidget(self)
        self.dockSubmissionContents = QWidget()

        # Labels
        l_name = QLabel(self.dockSubmissionContents)
        l_email = QLabel(self.dockSubmissionContents)
        l_id = QLabel(self.dockSubmissionContents)
        l_csid = QLabel(self.dockSubmissionContents)
        l_date = QLabel(self.dockSubmissionContents)
        l_name.setText('Name')
        l_email.setText('Email')
        l_id.setText('ID')
        l_csid.setText('CSID')
        l_date.setText('Date')

        # Text fields
        t_name = QLineEdit(self.dockSubmissionContents)
        t_email = QLineEdit(self.dockSubmissionContents)
        t_id = QLineEdit(self.dockSubmissionContents)
        t_csid = QLineEdit(self.dockSubmissionContents)
        t_date = QLineEdit(self.dockSubmissionContents)
        t_name.setReadOnly(True)
        t_email.setReadOnly(True)
        t_id.setReadOnly(True)
        t_csid.setReadOnly(True)
        t_date.setReadOnly(True)

        # Add to grid
        layout = QGridLayout(self.dockSubmissionContents)
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
        
        # Add to widget
        self.dockSubmission.setWidget(self.dockSubmissionContents)
        self.dockSubmission.setWindowTitle('Submission')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockSubmission)

    def setupDockOutput(self):
        self.dockOutput = QDockWidget(self)
        self.dockOutputContents = QWidget()
        text = QPlainTextEdit(self.dockOutputContents)
        layout = QVBoxLayout(self.dockOutputContents)
        layout.addWidget(text)
        self.dockOutput.setWidget(self.dockOutputContents)
        self.dockOutput.setWindowTitle('Output')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockOutput)
    
    def setupDockVerdict(self):
        self.dockVerdict = QDockWidget(self)
        self.dockVerdictContent = QWidget()

        l_mark = QLabel(self.dockVerdictContent)
        l_mark.setText('Mark')
        sl_mark = QSlider(self.dockVerdictContent)
        sl_mark.setMaximum(5)
        sl_mark.setOrientation(Qt.Horizontal)
        sl_mark.setTickPosition(QSlider.TicksBelow)
        sb_mark = QSpinBox(self.dockVerdictContent)
        sb_mark.setMinimum(0)
        sb_mark.setMaximum(5)

        # Connect local signals between the slider and spinbox
        sl_mark.valueChanged.connect(lambda x: sb_mark.setValue(sl_mark.value()))
        sb_mark.valueChanged.connect(lambda x: sl_mark.setValue(sb_mark.value()))

        # Put all into grid
        layout = QGridLayout(self.dockVerdictContent)
        layout.addWidget(l_mark, 0, 0, 1, 1)
        layout.addWidget(sl_mark, 0, 1, 1, 1)
        layout.addWidget(sb_mark, 0, 2, 1, 1)

        # Add to window
        self.dockVerdict.setWidget(self.dockVerdictContent)
        self.dockVerdict.setWindowTitle('Verdict')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockVerdict)

        
    def menuFileHandler(self, sender):
        """Handles events of menu items being clicked on"""
        signal = sender.text()
        if signal == '&Open Folder':
            print('Open folder handler here')
        elif signal == '&Quit':
            qApp.quit()
    
    def menuViewHandler(self, sender):
        """Handles any event from the view menu actions"""
        print(sender.text())

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
