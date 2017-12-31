# This demonstrates how to use treeView widget
# Model is using standarditemmodel
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class App(QWidget):

    # Enum the index
    FROM, SUBJECT, DATE = range(3)

    def __init__(self):
        super().__init__()

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('TreeView Tutorial')
        self.resize(600, 400)

        # Set data group
        self.treeview = QTreeView()
        self.treeview.setRootIsDecorated(False)
        # self.treeview.setAlternatingRowColors(True)

        # Create and set model
        model = self.createMailModel()
        self.treeview.setModel(model)
        self.treeview.clicked.connect(
            lambda x: self.itemSelected(model, x)
        )

        # Populate the model with some arbitrary data
        self.addMail(model, '1@a.com', 'SUBJECT A', '2017-12-31')
        self.addMail(model, '2@a.com', 'SUBJECT B', '2017-12-31')
        self.addMail(model, '3@a.com', 'SUBJECT C', '2017-12-31')

        # Put things in window
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.treeview)
        self.setLayout(mainLayout)
        self.show()

    def createMailModel(self):
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(self.FROM, Qt.Horizontal, 'From')
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, 'Subject')
        model.setHeaderData(self.DATE, Qt.Horizontal, 'Date')
        return model

    def addMail(self, model, sender, subject, date):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), sender)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.DATE), date)

        model.item(0).setCheckable(True)
        model.item(0, self.FROM).setEditable(False)
        model.item(0, self.SUBJECT).setEditable(False)
        model.item(0, self.DATE).setEditable(False)
        # model.item(0).setChecked(False)

    def itemSelected(self, model, modelIndex):
        # Only care about the first column
        item = model.item(modelIndex.row())

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

        item = model.item(modelIndex.row(), self.SUBJECT)
        item.setText(item.text() + ' (DONE)')


# Run app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = App()
    sys.exit(app.exec_())
