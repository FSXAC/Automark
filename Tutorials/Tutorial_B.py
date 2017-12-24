import sys
from PyQt5 import QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.button1 = QtWidgets.QPushButton("-")
        self.button2 = QtWidgets.QPushButton("+")
        self.label1 = QtWidgets.QLabel("0")

        h_box = QtWidgets.QHBoxLayout()
        # h_box.addStretch()    # This adds the padding
        h_box.addWidget(self.button1)
        # h_box.addStretch()
        h_box.addWidget(self.button2)
        # h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.label1)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('TB')

        # Connect signals emitted from the button to a slot funcction
        self.button1.clicked.connect(self.button1_click)
        self.button2.clicked.connect(self.button2_click)

        # display window
        self.show()

    def button1_click(self):
        self.label1.setText(str(int(self.label1.text()) - 1))
    
    def button2_click(self):
        self.label1.setText(str(int(self.label1.text()) + 1))

# Run the app
app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())