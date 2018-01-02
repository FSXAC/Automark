"""This is an auto grader program hopefully by used for APSC 160"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel

# Global constants
VERSION_NO = 'v0.0b'

class SummaryTree(QTreeView):
    SID, STATUS = range(2)

    # Signals
    summarySelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setModel(self.createSummaryModel())
        # self.reset()
        self.clicked.connect(self.itemSelected)

        # Populate with some dummy data
        self.addEntry('p5h0b', 'Unmarked')

    def createSummaryModel(self):
        # Create standard model with 0 rows, and 2 columns
        # and self as parent
        model = QStandardItemModel(0, 2, self)
        model.setHeaderData(self.SID, Qt.Horizontal, 'ID')
        model.setHeaderData(self.STATUS, Qt.Horizontal, 'Status')
        return model

    def itemSelected(self, modelIndex):
        item = self.model().item(modelIndex.row())
        print(item.text())
        self.summarySelected.emit(item.text())

    def addEntry(self, sid, status):
        self.model().insertRow(0)
        self.model().setData(self.model().index(0, self.SID), sid)
        self.model().setData(self.model().index(0, self.STATUS), status)
        self.model().item(0, self.SID).setEditable(False)
        self.model().item(0, self.STATUS).setEditable(False)

    def clearAll(self):
        # self.setModel(self.createSummaryModel())
        # print('reset')
        self.setModel(self.createSummaryModel())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentDirectory = ''
        self.setWindowTitle('Automark ' + VERSION_NO)
        self.setupUi()

    def setupUi(self):
        """Sets up nearly all of the front-end components"""
        # Make actions
        self.setupActions()

        # Menu and status bar
        self.menubar = QMenuBar(self)
        self.statusbar = QStatusBar(self)
        menuFile = self.menubar.addMenu('File')
        menuView = self.menubar.addMenu('View')
        menuOptions = self.menubar.addMenu('Options')
        self.setupMenuFile(menuFile)
        self.setupMenuView(menuView)
        self.setupMenuOptions(menuOptions)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)

        # Toolbar
        self.setupToolbar()

        # Docks
        self.setupDocks()

        # Central widget
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)

        # Window
        self.resize(1440, 800)
        self.show()

    def setupActions(self):
        """Creates a bunch of public actions for the app"""

        # File actions
        self.actionOpenFolder = QAction(QIcon('hi.png'), '&Open Folder', self)
        self.actionQuit = QAction(QIcon('hi.png'), '&Quit', self)

        # View actions
        self.actionDockFolders = QAction('Folders', self)
        self.actionDockFolders.setCheckable(True)
        self.actionDockFolders.setChecked(True)

        self.actionDockFiles = QAction('Files', self)
        self.actionDockFiles.setCheckable(True)
        self.actionDockFiles.setChecked(True)

        self.actionDockSubmission = QAction('Submission', self)
        self.actionDockSubmission.setCheckable(True)
        self.actionDockSubmission.setChecked(True)

        self.actionDockOutput = QAction('Output', self)
        self.actionDockOutput.setCheckable(True)
        self.actionDockOutput.setChecked(True)

        self.actionDockVerdict = QAction('Verdict', self)
        self.actionDockVerdict.setCheckable(True)
        self.actionDockVerdict.setChecked(True)

        self.actionDockSummarized = QAction('Summarized', self)
        self.actionDockSummarized.setCheckable(True)
        self.actionDockSummarized.setEnabled(False)

        # Option actions
        self.actionSummaryMode = QAction('Summary Mode', self)
        self.actionSummaryMode.setCheckable(True)
        self.actionSummaryMode.setShortcut('Ctrl+M')

    def setupMenuFile(self, menu):
        """Setup a particular set of actions and its menus"""
        # Add menu actions to menu
        menu.addAction(self.actionOpenFolder)
        menu.addSeparator()
        menu.addAction(self.actionQuit)

        # Bind signals from actions to slots
        menu.triggered.connect(self.menuFileHandler)
    
    def setupMenuView(self, menu):
        """Setup view related actions and menu items"""
        menu.addAction(self.actionDockFolders)
        menu.addAction(self.actionDockFiles)
        menu.addAction(self.actionDockSubmission)
        menu.addAction(self.actionDockOutput)
        menu.addAction(self.actionDockVerdict)

        menu.addSeparator()
        menu.addAction(self.actionDockSummarized)

        menu.triggered.connect(self.menuViewHandler)

    def setupMenuOptions(self, menu):
        menu.addAction(self.actionSummaryMode)
        menu.triggered.connect(self.menuOptionsHandler)

    def setupToolbar(self):
        """Setup the tool bar"""
        self.tbFiles = self.addToolBar('Files')
        self.tbFiles.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbFiles.addAction(self.actionOpenFolder)
        self.tbFiles.addAction(self.actionQuit)

    def setupDocks(self):
        """Setup dockable widgets"""
        self.setupDockFolders()
        self.setupDockFiles()
        self.setupDockSummarized()
        self.setupDockSubmission()
        self.setupDockOutput()
        self.setupDockVerdict()

    def setupDockFolders(self):
        """Setup docking widget that shows all the folders"""
        self.dockFolders = QDockWidget(self)
        self.dockFoldersContent = QWidget()
        
        # Directory indicator at the top
        modeLabel = QLabel(self.dockFoldersContent)
        modeLabel.setText('Legacy Mode')
        cdLabel = QLabel(self.dockFoldersContent)
        cdLabel.setText('Current Directory')
        cdURL = QLineEdit(self.dockFoldersContent)
        cdURL.setReadOnly(True)
        cdContainer = QHBoxLayout()
        cdContainer.addWidget(cdLabel)
        cdContainer.addWidget(cdURL)

        # List view
        self.foldersList = QListView(self.dockFoldersContent)

        # Add everything together in a vertical layout
        vLayout = QVBoxLayout(self.dockFoldersContent)
        vLayout.addWidget(modeLabel)
        vLayout.addLayout(cdContainer)
        vLayout.addWidget(self.foldersList)

        # Add dock widget to main window
        self.dockFolders.setWidget(self.dockFoldersContent)
        self.dockFolders.setWindowTitle('Folders')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFolders)

        # Connect signals relevant to this dock
        self.dockFolders.visibilityChanged.connect(lambda x: self.actionDockFolders.setChecked(x))

    def setupDockFiles(self):
        """Setup dokcing widget that shows files in the folder selected"""
        self.dockFiles = QDockWidget(self)
        self.dockFilesContents = QWidget()

        # List view
        filesList = QListView(self.dockFilesContents)

        # Add to layout
        layout = QVBoxLayout(self.dockFilesContents)
        layout.addWidget(filesList)
        self.dockFiles.setWidget(self.dockFilesContents)
        self.dockFiles.setWindowTitle('Files')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFiles)
        self.dockFiles.visibilityChanged.connect(lambda x: self.actionDockFiles.setChecked(x))

    def setupDockSummarized(self):
        """Setup navigation menu for summarized mode"""
        self.dockSummarized = QDockWidget(self)
        self.dockSummarizedContent = QWidget()
        # TODO: Reduce repetitive code
        modeLabel = QLabel(self.dockSummarizedContent)
        modeLabel.setText('Summary Mode')
        cdLabel = QLabel(self.dockSummarizedContent)
        cdLabel.setText('Current Directory')
        cdURL = QLineEdit(self.dockSummarizedContent)
        cdURL.setReadOnly(True)
        cdContainer = QHBoxLayout()
        cdContainer.addWidget(cdLabel)
        cdContainer.addWidget(cdURL)
        vLayout = QVBoxLayout(self.dockSummarizedContent)
        vLayout.addWidget(modeLabel)
        vLayout.addLayout(cdContainer)
        # self.summaryTree = QTreeView()
        # vLayout.addWidget(self.summaryTree)

        self.summaryTree = SummaryTree()
        self.summaryTree.summarySelected.connect(self.summaryOpenHandler)
        vLayout.addWidget(self.summaryTree)


        self.dockSummarized.setWidget(self.dockSummarizedContent)
        self.dockSummarized.setWindowTitle('Submissions Summary')
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockSummarized)
        self.dockSummarized.setVisible(False)

        self.dockSummarized.visibilityChanged.connect(lambda x: self.actionDockSummarized.setChecked(x))

    def setupDockSubmission(self):
        """Setup dock that shows student information"""
        self.dockSubmission = QDockWidget(self)
        self.dockSubmissionContents = QWidget()

        # Labels
        l_name = QLabel(self.dockSubmissionContents)
        l_email = QLabel(self.dockSubmissionContents)
        l_id = QLabel(self.dockSubmissionContents)
        l_csid = QLabel(self.dockSubmissionContents)
        l_date = QLabel(self.dockSubmissionContents)
        l_name.setText('Name')
        l_email.setText('Email')
        l_id.setText('ID')
        l_csid.setText('CSID')
        l_date.setText('Date')

        # Text fields
        t_name = QLineEdit(self.dockSubmissionContents)
        t_email = QLineEdit(self.dockSubmissionContents)
        t_id = QLineEdit(self.dockSubmissionContents)
        t_csid = QLineEdit(self.dockSubmissionContents)
        t_date = QLineEdit(self.dockSubmissionContents)
        t_name.setReadOnly(True)
        t_email.setReadOnly(True)
        t_id.setReadOnly(True)
        t_csid.setReadOnly(True)
        t_date.setReadOnly(True)

        # Add to grid
        layout = QGridLayout(self.dockSubmissionContents)
        layout.addWidget(l_name, 0, 0, 1, 1)
        layout.addWidget(t_name, 0, 1, 1, 1)
        layout.addWidget(l_email, 1, 0, 1, 1)
        layout.addWidget(t_email, 1, 1, 1, 1)
        layout.addWidget(l_id, 2, 0, 1, 1)
        layout.addWidget(t_id, 2, 1, 1, 1)
        layout.addWidget(l_csid, 3, 0, 1, 1)
        layout.addWidget(t_csid, 3, 1, 1, 1)
        layout.addWidget(l_date, 4, 0, 1, 1)
        layout.addWidget(t_date, 4, 1, 1, 1)
        
        # Add to widget
        self.dockSubmission.setWidget(self.dockSubmissionContents)
        self.dockSubmission.setWindowTitle('Submission')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockSubmission)
        self.dockSubmission.visibilityChanged.connect(lambda x: self.actionDockSubmission.setChecked(x))

    def setupDockOutput(self):
        self.dockOutput = QDockWidget(self)
        self.dockOutputContents = QWidget()
        text = QPlainTextEdit(self.dockOutputContents)
        layout = QVBoxLayout(self.dockOutputContents)
        layout.addWidget(text)
        self.dockOutput.setWidget(self.dockOutputContents)
        self.dockOutput.setWindowTitle('Output')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockOutput)
        self.dockOutput.visibilityChanged.connect(lambda x: self.actionDockOutput.setChecked(x))
    
    def setupDockVerdict(self):
        self.dockVerdict = QDockWidget(self)
        self.dockVerdictContent = QWidget()

        l_mark = QLabel(self.dockVerdictContent)
        l_mark.setText('Mark')
        sl_mark = QSlider(self.dockVerdictContent)
        sl_mark.setMaximum(5)
        sl_mark.setOrientation(Qt.Horizontal)
        sl_mark.setTickPosition(QSlider.TicksBelow)
        sb_mark = QSpinBox(self.dockVerdictContent)
        sb_mark.setMinimum(0)
        sb_mark.setMaximum(5)

        # Connect local signals between the slider and spinbox
        sl_mark.valueChanged.connect(lambda x: sb_mark.setValue(sl_mark.value()))
        sb_mark.valueChanged.connect(lambda x: sl_mark.setValue(sb_mark.value()))

        # Put all into grid
        layout = QGridLayout(self.dockVerdictContent)
        layout.addWidget(l_mark, 0, 0, 1, 1)
        layout.addWidget(sl_mark, 0, 1, 1, 1)
        layout.addWidget(sb_mark, 0, 2, 1, 1)

        # Add to window
        self.dockVerdict.setWidget(self.dockVerdictContent)
        self.dockVerdict.setWindowTitle('Verdict')
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockVerdict)
        self.dockVerdict.visibilityChanged.connect(lambda x: self.actionDockVerdict.setChecked(x))

    def menuFileHandler(self, sender):
        """Handles events of menu items being clicked on"""
        signal = sender.text()
        if signal == '&Open Folder':
            self.openFolder()
        elif signal == '&Quit':
            qApp.quit()
    
    def menuViewHandler(self, sender):
        """Handles any event from the view menu actions"""
        signal = sender.text()
        vis = sender.isChecked()
        if signal == 'Folders':
            self.dockFolders.setVisible(vis)
        elif signal == 'Files':
            self.dockFiles.setVisible(vis)
        elif signal == 'Submission':
            self.dockSubmission.setVisible(vis)
        elif signal == 'Output':
            self.dockOutput.setVisible(vis)
        elif signal == 'Verdict':
            self.dockVerdict.setVisible(vis)
        elif signal == 'Summarized':
            self.dockSummarized.setVisible(vis)

    def menuOptionsHandler(self, sender):
        signal = sender.text()
        if signal == 'Summary Mode':
            self.setMarkingSummaryMode(sender.isChecked())

    def openFolder(self):
        """Start a marking project"""
        # Get existing directory
        fdir = QFileDialog.getExistingDirectory(
            self, 'Select Folder', os.getenv('HOME'),
            QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        )

        if fdir == '': return
        
        self.validator = Validator(self.actionSummaryMode.isChecked())
        if not self.validator.validate(fdir): return

        # Parse the contents in the directory
        # subs = self.validator.parseSubmission()
        # self.foldersList.
        # TODO: make the folder list a separate class
        # https://www.pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/

        if self.actionSummaryMode.isChecked():
            self.loadSummary(self.validator.parseSummary())
            
            # Let user know the folder is opened and set current directory
            self.setCurrentDirectory(fdir)
            self.statusbar.showMessage('Opened summary folder at ' + fdir)
        else:
            self.loadSubmissions()

    def setCurrentDirectory(self, fdir):
        self.currentDirectory = fdir

    def setMarkingSummaryMode(self, summary):
        self.actionDockFiles.setChecked(not summary)
        self.actionDockFiles.setEnabled(not summary)
        self.actionDockFolders.setChecked(not summary)
        self.actionDockFolders.setEnabled(not summary)
        self.dockFolders.setVisible(not summary)
        self.dockFiles.setVisible(not summary)
        self.actionDockSummarized.setEnabled(summary)
        self.dockSummarized.setVisible(summary)

    def loadSummary(self, summaryList):
        # first clear all items in the summary tree
        # then add all entries
        self.summaryTree.clearAll()
        for submission in summaryList:
            self.summaryTree.addEntry(submission, 'Unmarked')

    def loadSubmissions(self):
        """WIP"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Only Summary Mode is supported at this time')
        msg.setInformativeText('Please switch to Summary Mode in the Options menu')
        msg.setWindowTitle('Not supported')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def summaryOpenHandler(self, sid):
        txtFileDir = self.currentDirectory + '/' + sid + '.txt'
        cFileDir = self.currentDirectory + '/' + sid + '.c'
        try:
            txtFile = open(txtFileDir, 'r')
            print(txtFile.read())
            txtFile.close()

            cFile = open(cFileDir, 'r')
            self.textedit.setText(cFile.read())
            cFile.close()

        except Exception as e:
            print(e)

class Validator:
    """This class is instantiated to check if current directory contains the right files"""
    def __init__(self, summaryMode):
        self.summaryMode = summaryMode
        self.path = ''

    def validate(self, path):
        self.path = path
        if self.summaryMode:
            for file in os.listdir(path):
                fname, fext = os.path.splitext(file)
                # Find something that is odd then return false
        return True

    def parseSummary(self):
        if self.path == None or self.path == '':
            print('Make sure to validate first before parsing submissions')
            return False

        items = []
        for file in os.listdir(self.path):
            fname, fext = os.path.splitext(file)
            if fname not in items: items.append(fname)
        return items

# Run the app
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
