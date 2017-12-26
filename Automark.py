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
        self.resize(800, 600)
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
