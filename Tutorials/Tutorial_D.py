import os
import sys
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
        self.setWindowTitle("Tutorial D - Text editor")
        self.setGeometry(100, 100, 600, 400)
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
    
# Run app
app = QApplication(sys.argv)
writer = Notepad()
sys.exit(app.exec_())
