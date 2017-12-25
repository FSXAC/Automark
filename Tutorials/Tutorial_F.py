import sys
import os
import csv
from PyQt5.QtWidgets import *

class Table(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_range = True
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()

    def c_current(self):
        if self.check_range:
            row = self.currentRow()
            col = self.currentColumn()
            if row < 0 or col < 0:
                return None

            value = self.item(row, col)
            print('(' + str(row) + ', ' + str(col) + ')')
            value = value.text()
            print('(' + str(row) + ', ' + str(col) + '): ' + value)
    
    def open_sheet(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as f:
                self.setRowCount(0)     # ???
                self.setColumnCount(10) # ???
                file = csv.reader(f, dialect='excel')
                for row_data in file:
                    row = self.rowCount()
                    self.insertRow(row)

                    # Re-set the column size (default is 10)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))

                    # Populate the table
                    for column, data in enumerate(row_data):
                        item = QTableWidgetItem(data)
                        self.setItem(row, column, item)
        self.check_change = True

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as f:
                writer = csv.writer(f, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create instance of table with 10x10 size as default
        self.table = Table(10, 10)
        columnHeaders = [a for a in 'ABCDEFGHIJ']
        self.table.setHorizontalHeaderLabels(columnHeaders)

        self.setCentralWidget(self.table)
        self.setWindowTitle('FakeNews 2.0')

        # Set up menu
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')

        # Menu actions
        newAction = QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        quitAction = QAction('Quit', self)
        quitAction.setShortcut('Ctrl+Q')

        # Add menu actions
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(quitAction)

        # Bind signals
        # newAction.triggered.connect(self.unbinded)
        openAction.triggered.connect(self.table.open_sheet)
        saveAction.triggered.connect(self.table.save_sheet)
        quitAction.triggered.connect(self.quitHandler)
        
        # Open window
        self.resize(700, 400)
        self.show()

    def quitHandler(self):
        qApp.quit()

# Run the app
app = QApplication(sys.argv)
sheet = Sheet()
sys.exit(app.exec_())
