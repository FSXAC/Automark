import sys
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

VERSION_NO = 'v0.0'

class AutomarkWidget(QWidget):
    def __init__(self):
        super(AutomarkWidget, self).__init__()
        
        self.setupUi()
    
    def setupUi(self):
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)
        self.show()

    def openFolder(self):
        """Opens a dialog window to get file directory"""
        fname = QFileDialog.getExistingDirectory(
            self, 'Open folder', os.getenv('HOME')
        )

        #TODO: verify that the folder contains the right stuff
        #TODO: then populate backend

        return fname

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Using main automark widget as central widget
        self.am = AutomarkWidget()
        self.setCentralWidget(self.am)

        self.setWindowTitle('Automark ' + VERSION_NO)
        self.setupUi()


    def setupUi(self):
        # menuBar = self.menuBar()
        # Make instance of menu and status bar
        menubar = QMenuBar(self)

        # Add root menus to menubar 
        menuFile = menubar.addMenu('File')
        menuEdit = menubar.addMenu('Edit')

        # Setup menu actions
        self.setupMenuFile(menuFile)
        self.setupMenuEdit(menuEdit)

        # Add menu bar to main window
        self.setMenuBar(menubar)

        self.resize(600, 400)
        self.show()

    def setupMenuFile(self, menu):
        actNew = QAction('&New', self)
        actNew.setShortcut('Ctrl+N')
        actOpen = QAction('&Open folder', self)
        actOpen.setShortcut('Ctrl+O')
        actSave = QAction('&Save', self)
        actSave.setShortcut('Ctrl+S')
        actQuit = QAction('&Quit', self)
        actQuit.setShortcut('Ctrl+Q')

        # Add menu actions to menu
        menu.addAction(actNew)
        menu.addAction(actOpen)
        menu.addAction(actSave)
        menu.addAction(actQuit)

        # Bind signals from actions to slots
        menu.triggered.connect(self.menuFileHandler)
    
    def setupMenuEdit(self, menu):
        """Nothing here yet"""

    def menuFileHandler(self, sender):
        """Handles events of menu items being clicked on"""
        signal = sender.text()
        if signal == '&New':
            print('New handler here')
        elif signal == '&Open folder':
            directory = self.am.openFolder()
            print(directory)
        elif signal == '&Save':
            print('save')
        elif signal == '&Quit':
            qApp.quit()

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
