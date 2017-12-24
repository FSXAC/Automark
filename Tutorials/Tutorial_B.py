import sys
from PyQt5 import QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.button1 = QtWidgets.QPushButton("-")
        self.button2 = QtWidgets.QPushButton("+")
        self.button3 = QtWidgets.QPushButton("OK")
        self.label1 = QtWidgets.QLabel("0")

        # Line edit
        self.lineEdit = QtWidgets.QLineEdit()

        h_box = QtWidgets.QHBoxLayout()
        # h_box.addStretch()    # This adds the padding
        h_box.addWidget(self.button1)
        # h_box.addStretch()
        h_box.addWidget(self.button2)
        # h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.label1)
        v_box.addLayout(h_box)
        
        # Line edit layout
        h_box_le = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.lineEdit)
        h_box.addWidget(self.button3)
        v_box.addChildLayout(h_box_le)
        

        self.setLayout(v_box)
        self.setWindowTitle('TB')

        # Connect signals emitted from the button to a slot funcction
        self.button1.clicked.connect(self.button1_click)
        self.button2.clicked.connect(self.button2_click)

        # Connect line edit signals and slots
        self.button3.clicked.connect(self.le_submit)
        self.lineEdit.returnPressed.connect(self.le_submit)
        self.lineEdit.cursorPositionChanged.connect(self.le_cursorChanged)

        # display window
        self.show()

    def button1_click(self):
        self.label1.setText(str(int(self.label1.text()) - 1))
    
    def button2_click(self):
        self.label1.setText(str(int(self.label1.text()) + 1))

    def le_submit(self):
        # sender is the origin of the signal
        sender = self.sender()
        if (sender.text() == 'OK'):
            print(self.lineEdit.text())
        else:
            self.lineEdit.clear()
        
    
    def le_cursorChanged(self, old, new):
        self.label1.setText(str(new))


# Run the app
app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())