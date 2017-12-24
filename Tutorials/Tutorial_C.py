import sys
from PyQt5 import QtWidgets

class Notepad(QtWidgets.QWidget):
    def __init__(self):
        super(Notepad, self).__init__()
        self.text = QtWidgets.QTextEdit(self)
        self.clearButton = QtWidgets.QPushButton('Save')

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.clearButton)
        
        # Connect signals
        self.clearButton.clicked.connect(self.saveText)

        # Finish window
        self.setLayout(layout)
        self.setWindowTitle("TC - edit")
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def saveText(self):
        with open('test.txt', 'w') as f:
            newText = self.text.toPlainText()
            f.write(newText)
            print(newText)

# Run the app
app = QtWidgets.QApplication(sys.argv)
writer = Notepad()
sys.exit(app.exec_())