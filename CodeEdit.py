"""
Main text editor docked window
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtGui import QPalette, QColor

class CodeEdit(QTextEdit):
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Initialzes UI elements"""
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor('#333'))
        palette.setColor(QPalette.Text, Qt.white)
        self.setPalette(palette)

        font = QFont()
        font.setFamily('Consolas')
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)

        # Set tab spacing to another value
        font_metrics = QFontMetrics(font)
        self.setTabStopWidth(4 * font_metrics.width(' '))

        # Line wrapping
        self.setLineWrapMode(QTextEdit.NoWrap)

        # Set as readonly
        # TODO: Make savable and recompilable
        # self.setReadOnly(True)

    def set_text_changed_handler(self, handler):
        """Configures what happens when the text in the editor changes"""
        self.textChanged.connect(handler)