import sys
from PyQt5 import QtWidgets, QtGui

def window():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setGeometry(100, 100, 500, 300)

    # labels
    label1 = QtWidgets.QLabel(window)
    label1.setText("Automark version 0.0")
    # label1.move(50, 50)

    # labels with pixmaps
    # label2 = QtWidgets.QLabel(window)
    # label2.setPixmap(QtGui.QPixmap('hi.png'))

    # pushbuttons
    button1 = QtWidgets.QPushButton(window)
    button1.setText("Button 1")
    # button1.move(50, 100)

    # Box layouts
    h_box = QtWidgets.QHBoxLayout()
    h_box.addStretch()
    h_box.addWidget(label1)
    h_box.addStretch()
    v_box = QtWidgets.QVBoxLayout()
    v_box.addLayout(h_box)
    v_box.addWidget(button1)

    window.setLayout(v_box)
    window.setWindowTitle("Automark (v0.0)")
    window.show()
    sys.exit(app.exec_())

window()
