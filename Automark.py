import sys
import os
# from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

VERSION_NO = 'v0.0a'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Using main automark widget as central widget
        # self.am = AutomarkWidget()
        # self.setCentralWidget(self.am)

        self.setWindowTitle('Automark ' + VERSION_NO)
        self.setupUi()

    def setupUi(self):
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
        # self.dockFolders = QDockWidget(self)
        self.setupDocks()

        # Widgets
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)


        # Window
        self.resize(800, 600)
        self.show()

    def setupMenuFile(self, menu):
        actionOpenFolder = QAction('&Open Folder', self)
        actionQuit = QAction('&Quit', self)

        # Add menu actions to menu
        menu.addAction(actionOpenFolder)
        menu.addSeparator()
        menu.addAction(actionQuit)

        # Bind signals from actions to slots
        menu.triggered.connect(self.menuFileHandler)
    
    def setupMenuView(self, menu):
        menu.triggered.connect(self.menuViewHandler)

    def setupDocks(self):
        self.setupDockFolders()

    def setupDockFolders(self):
        self.dockFolders = QDockWidget(self)
        self.dockFoldersContent = QWidget()
        vLayout = QVBoxLayout(self.dockFoldersContent)
        testLabel = QLabel(self.dockFoldersContent)
        vLayout.addWidget(testLabel)

        self.dockFolders.setWidget(self.dockFoldersContent)
        self.dockFolders.setWindowTitle('Folders')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFolders)

    def menuFileHandler(self, sender):
        """Handles events of menu items being clicked on"""
        signal = sender.text()
        if signal == '&Open Folder':
            print('Open folder handler here')
        elif signal == '&Quit':
            qApp.quit()
    
    def menuViewHandler(self, sender):
        print(sender.text())

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
