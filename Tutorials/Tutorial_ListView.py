import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# Create a Qt application
app = QApplication(sys.argv)

# Our main window will be a QListView
list = QListView()
list.setWindowTitle('Honey-Do List')
list.setMinimumSize(600, 400)

# Create an empty model for the list's data
model = QStandardItemModel(list)

# Add some textual items
foods = [
    'Cookie dough',  # Must be store-bought
    'Hummus',  # Must be homemade
    'Spaghetti',  # Must be saucy
    'Dal makhani',  # Must be spicy
    'Chocolate whipped cream'  # Must be plentiful
]

for food in foods:
    # Create an item with a caption
    item = QStandardItem(food)

    # Add a checkbox to it
    item.setCheckable(True)

    # Other
    item.setEditable(False)

    # Add the item to the model
    model.appendRow(item)

def onItemClicked(modelIndex):
    print(modelIndex.row(), modelIndex.column())

    item = model.item(modelIndex.row())
    if item.checkState() == Qt.Checked:
        item.setCheckState(Qt.Unchecked)
    else:
        item.setCheckState(Qt.Checked)

# Apply the model to the list view
list.setModel(model)
list.clicked.connect(onItemClicked)

# Show the window and run the app
list.show()
app.exec_()
