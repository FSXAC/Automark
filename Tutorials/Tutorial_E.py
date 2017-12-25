import sys
import os
from PyQt5.QtWidgets import *

class MenuDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        
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
        new_action.triggered.connect(self.new_trigger)
        open_action.triggered.connect(self.open_trigger)
        save_action.triggered.connect(self.save_trigger)
        quit_action.triggered.connect(self.quit_trigger)

        find_action.triggered.connect(self.unbinded)
        replace_action.triggered.connect(self.unbinded)
    
        # Finalize window
        self.setWindowTitle('Menu Test')
        self.resize(600, 400)
        self.show()

    # Slots for menu actions
    def new_trigger(self):
        """This should clear everything in the workspace"""
        # TODO:

    def open_trigger(self):
        """Opens a dialog to select the file"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'), 'Text files (*.txt)')
        if fname[0] != '':
            with open(fname[0], 'r') as f:
                text = f.read()
                print(text)
                # TODO: do something with the text

    def save_trigger(self):
        """Opens a dialog to save the file"""
        fname = QFileDialog.getSaveFileName(self, 'Open file', os.getenv('HOME'), 'Text files (*.txt)')
        if fname[0] != '':
            with open(fname[0], 'w') as f:
                text = "Lorem ipsum" #TODO:
                f.write(text)
                # TODO: do something with the text

    def quit_trigger(self):
        """Exit the app"""
        qApp.quit()

    def unbinded(self):
        """Placeholder for unbinded signals"""
        print("WIP")


# Run the app
app = QApplication(sys.argv)
menus = MenuDemo()
sys.exit(app.exec_())
