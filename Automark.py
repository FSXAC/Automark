"""This is an auto grader program hopefully by used for APSC 160"""

import sys
import os
import subprocess
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

# Global constants
VERSION_NO = 'v0.1'

class Highlighter(QSyntaxHighlighter):
    def __init__(self, textDocument):
        super().__init__(textDocument)

        # This dictionary consists of highlighting rules
        # Where the key is the regular expression (QRegularExpression)
        # and the result is the text char format (QTextCharFormat)
        self.highlightingRules = {}

        # Text formats
        self.setupTextCharFormats()

    def setupTextCharFormats(self):
        # Keywords
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor('#F92672'))
        keywordPatterns = [
            '\\#\\bdefine\\b', '\\#\\binclude\\b', '\\breturn\\b',
            '\\bconst\\b', '\\bvolatile\\b', '\\bextern\\b',
            '\\bstatic\\b'
        ]
        for pattern in keywordPatterns:
            patternRegex = QRegularExpression(pattern)
            self.highlightingRules[patternRegex] = keywordFormat

        # Types
        typeFormat = QTextCharFormat()
        typeFormat.setForeground(QColor('#66D9EF'))
        typeFormat.setFontItalic(True)
        typePatterns = [
            '\\bchar\\b', '\\bint\\b', '\\blong\\b', '\\bshort\\b', 
            '\\bsigned\\b', '\\bunsigned\\b', '\\bvoid\\b',
            '\\bstruct\\b', '\\btypedef\\b'
        ]
        for pattern in typePatterns:
            regex = QRegularExpression(pattern)
            self.highlightingRules[regex] = typeFormat

        # Quotations
        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor('#E3D859'))
        quotationRegex = QRegularExpression('\".*\"')
        self.highlightingRules[quotationRegex] = quotationFormat

        # Includes
        includeRegex = QRegularExpression('\\<.*\\>')
        self.highlightingRules[includeRegex] = quotationFormat

        # Functions
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor('#A6E22E'))
        functionRegex = QRegularExpression('\\b[A-Za-z0-9_]+(?=\\()')
        self.highlightingRules[functionRegex] = functionFormat

        # Single line comments
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.gray)
        singleLineCommentRegex = QRegularExpression('\/\/[^\n]*')
        self.highlightingRules[singleLineCommentRegex] = singleLineCommentFormat
        
        # Multi line comments
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.gray)
        self.multiLineCommentStartRegex = QRegularExpression('\/\\*')
        self.multiLineCommentEndRegex = QRegularExpression('\\*/')
    
    def highlightBlock(self, text):
        """Override highlight block function"""

        for rule in self.highlightingRules:
            matchFormat = self.highlightingRules[rule]
            matchIterator = rule.globalMatch(text)

            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), matchFormat)

        # Highlight multiline comments

        # Set current block state to 0
        # where 0 is outside a block comment and 1 is inside
        # self.setCurrentBlockState(0)

        # startIndex = 0
        # if self.previousBlockState() != 1:
        #     # startIndex = text.index(self.multiLineCommentStartRegex)

        #     matchIterator = self.multiLineCommentStartRegex.globalMatch(text)
        #     if matchIterator.hasNext():
        #         match = matchIterator.next()
        #         startIndex = match.capturedStart()

        # while startIndex > 0:
        #     match = self.multiLineCommentEndRegex.match(text, startIndex)
        #     endIndex = match.capturedStart()
        #     commentLength = 0
        #     if endIndex == -1:
        #         self.setCurrentBlockState(1)
        #         commentLength = text.length() - startIndex
        #     else:
        #         commentLength = endIndex - startIndex + match.capturedLength()
        
        #     # set format for block
        #     self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
        #     startIndex = text.index(self.multiLineCommentStartRegex, startIndex + commentLength)


class CodeEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # self.setTextBackgroundColor(Qt.darkGray)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor('#333'))
        palette.setColor(QPalette.Text, Qt.white)
        self.setPalette(palette)

        font = QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.setFont(font)

class SummaryTree(QTreeView):
    SID, STATUS = range(2)

    # Signals
    summarySelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setModel(self.createSummaryModel())
        self.clicked.connect(self.itemSelected)

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
        self.setModel(self.createSummaryModel())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentDirectory = ''
        self.currentFile = ''
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
        menuRun = self.menubar.addMenu('Run')
        self.setupMenuFile(menuFile)
        self.setupMenuView(menuView)
        self.setupMenuOptions(menuOptions)
        self.setupMenuRun(menuRun)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)

        # Toolbar
        self.setupToolbar()

        # Docks
        self.setupDocks()

        # Central widget
        self.textedit = CodeEdit()
        self.highlighter = Highlighter(self.textedit.document())
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

        # Compile actions
        self.actionRun = QAction(QIcon('res/compile_one.png'), 'Run', self)
        self.actionRunAll = QAction(QIcon('res/compile_all.png'), 'Run All', self)

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

    def setupMenuRun(self, menu):
        """Setup menu run"""
        menu.addAction(self.actionRun);
        menu.addAction(self.actionRunAll)
        menu.triggered.connect(self.menuRunHandler)

    def setupMenuOptions(self, menu):
        menu.addAction(self.actionSummaryMode)
        menu.triggered.connect(self.menuOptionsHandler)

    def setupToolbar(self):
        """Setup the tool bar"""
        self.tbFiles = self.addToolBar('Files')
        self.tbFiles.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbFiles.addAction(self.actionOpenFolder)
        self.tbFiles.addAction(self.actionQuit)

        self.tbRun = self.addToolBar('Run')
        self.tbRun.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbRun.addAction(self.actionRun)
        self.tbRun.addAction(self.actionRunAll)

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
        self.outputProgramText = QPlainTextEdit(self.dockOutputContents)
        layout = QVBoxLayout(self.dockOutputContents)
        layout.addWidget(self.outputProgramText)
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

    def menuRunHandler(self, sender):
        signal = sender.text()
        if signal == 'Run':
            if self.currentFile == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('No file found')
                msg.setInformativeText('Open a file first')
                msg.setWindowTitle('No file found')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return False
            
            programOut = self.runProgram(self.currentFile)
            self.outputProgramText.setPlainText(programOut)

        elif signal == 'Run All':
            print('run all')

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
            print(txtFile.read()) # TODO:
            txtFile.close()

            cFile = open(cFileDir, 'r')
            self.textedit.setText(cFile.read())
            cFile.close()

            self.currentFile = cFileDir

        except Exception as e:
            print(e)

    def runProgram(self, cFile):
        tempdir = './temp/'
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        
        # Compile the file first
        subprocess.run('gcc ' + cFile + ' -o ./temp/out.exe')

        # Get program output
        process = subprocess.Popen(
            ['temp\\out.exe'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # TODO: hack
        sleep(0.5)
        input_data = "Muchen\n".encode('utf-8')
        out_data = process.communicate(input=input_data)[0]

        sleep(0.5)
        input_data = "\n".encode('utf-8')
        out_data += process.communicate(input=input_data)[0]
        return str(out_data)


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
