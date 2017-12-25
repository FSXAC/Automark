import sys
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
        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        quit_action = QAction('&Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        find_action = QAction('&Find', self)
        find_action.setShortcut('Ctrl+F')
        replace_action = QAction('&Replace', self)
        replace_action.setShortcut('Ctrl+H')

        # Bind actions to menus
        menu_file.addAction(new_action)
        menu_file.addAction(save_action)
        menu_file.addAction(quit_action)
        menu_edit.addAction(find_action)
        menu_edit.addAction(replace_action)

        # Bind events from actions signals to slots
        quit_action.triggered.connect(self.quit_trigger)
        menu_file.triggered.connect(self.selected)

        # Finalize window
        self.setWindowTitle('Menu Test')
        self.resize(600, 400)
        self.show()

    def quit_trigger(self):
        qApp.quit()

    def selected(self, q):
        print(q.text() + 'selected')

# Run the app
app = QApplication(sys.argv)
menus = MenuDemo()
sys.exit(app.exec_())
