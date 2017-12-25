import sys
import os
from PyQt5.QtWidgets import *

class Notepad(QWidget):
    def __init__(self):
        super(Notepad, self).__init__()
        self.textEdit = QTextEdit(self)
        self.clearBtn = QPushButton('Clear')
        self.saveBtn = QPushButton('Save')
        self.openBtn = QPushButton('Open')

        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        h_layout.addWidget(self.openBtn)
        h_layout.addWidget(self.saveBtn)
        h_layout.addWidget(self.clearBtn)

        v_layout.addWidget(self.textEdit)
        v_layout.addLayout(h_layout)

        # Connect signals to slots
        self.saveBtn.clicked.connect(self.saveText)
        self.openBtn.clicked.connect(self.openText)
        self.clearBtn.clicked.connect(self.clearText)

        # Finalize window
        self.setLayout(v_layout)
        self.setWindowTitle("Tutorial E")
        self.show()

    def saveText(self):
        # Open QT dialog
        # with dialog title 'Save file' and at $HOME$ starting directory
        # File extension specified in the third parameter
        fname = QFileDialog.getSaveFileName(self, 'Save file', os.getenv(
            'HOME'), 'Text Files (*.txt)')
        if fname[0] != '':
            with open(fname[0], 'w') as f:
                text = self.textEdit.toPlainText()
                f.write(text)

    def openText(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', os.getenv('HOME'), 'Text Files (*.txt)')
        if fname[0] != '':
            with open(fname[0], 'r') as f:
                text = f.read()
                self.textEdit.setText(text)

    def clearText(self):
        self.textEdit.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Using the notepad as the central widget 
        self.notepad = Notepad()
        self.setCentralWidget(self.notepad)

        self.init_ui()
        
        
    def init_ui(self):
        # create menu bar
        menuBar = self.menuBar()

        # root menus
        menu_file = menuBar.addMenu('File')
        menu_edit = menuBar.addMenu('Edit')

        # actions for menus
        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        quit_action = QAction('&Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        find_action = QAction('&Find', self)
        find_action.setShortcut('Ctrl+F')
        replace_action = QAction('&Replace', self)
        replace_action.setShortcut('Ctrl+H')

        # Bind actions to menus
        menu_file.addAction(new_action)
        menu_file.addAction(open_action)
        menu_file.addAction(save_action)
        menu_file.addAction(quit_action)
        menu_edit.addAction(find_action)
        menu_edit.addAction(replace_action)

        # Bind events from actions signals to slots
        menu_file.triggered.connect(self.fileMenuHandler)
        menu_edit.triggered.connect(self.editMenuHandler)

        self.show()

    def fileMenuHandler(self, sender):
        signal = sender.text()
        if signal == '&New':
            self.notepad.clearText()
        elif signal == '&Open':
            self.notepad.openText()
        elif signal == '&Save':
            self.notepad.saveText()
        elif signal == '&Quit':
            qApp.quit()
    
    def editMenuHandler(self, sender):
        print('WIP')

# Run the app
app = QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
