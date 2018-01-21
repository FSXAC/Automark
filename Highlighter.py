"""
Highlighter class for the text editor
"""
import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QPalette, QColor
from PyQt5.QtCore import QRegularExpression

class Highlighter(QSyntaxHighlighter):
    """Highlighter class for the text edit"""
    def __init__(self, text_doc):
        """Constructor"""
        super().__init__(text_doc)

        # This dictionary consists of highlighting rules
        # Where the key is the regular expression (QRegularExpression)
        # and the result is the text char format (QTextCharFormat)
        self.highlighting_rules = {}

        # Text formats
        self.setup_textchar_formats()


    def add_patterns(self, patterns, pattern_format):
        """From a list of patterns, assign a format to them"""
        for pattern in patterns:
            pattern_regex = QRegularExpression(pattern)
            self.highlighting_rules[pattern_regex] = pattern_format

    def setup_textchar_formats(self):
        """Initializes all the text formatting for the syntax"""
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#F92672'))
        keyword_patterns = [
            '\\#\\bdefine\\b', '\\#\\binclude\\b', '\\breturn\\b',
            '\\bconst\\b', '\\bvolatile\\b', '\\bextern\\b',
            '\\bstatic\\b'
        ]
        self.add_patterns(keyword_patterns, keyword_format)

        # C Types
        type_format = QTextCharFormat()
        type_format.setForeground(QColor('#66D9EF'))
        type_format.setFontItalic(True)
        type_patterns = [
            '\\bchar\\b', '\\bint\\b', '\\blong\\b', '\\bshort\\b',
            '\\bsigned\\b', '\\bunsigned\\b', '\\bvoid\\b',
            '\\bstruct\\b', '\\btypedef\\b', '\\bdouble\\b', '\\bfloat\\b'
        ]
        self.add_patterns(type_patterns, type_format)

        # Quotations and include
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor('#E3D859'))
        self.add_patterns(['\".*\"', '\\<.*\\>'], quote_format)

        # Functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor('#A6E22E'))
        self.add_patterns(['\\b[A-Za-z0-9_]+(?=\\()'], function_format)

        # Single line comments
        single_comment_format = QTextCharFormat()
        single_comment_format.setForeground(Qt.gray)
        single_comment_format.setFontItalic(True)
        self.add_patterns(['\/\/[^\n]*'], single_comment_format)
    
    def highlightBlock(self, text):
        """Overrides the highlight block function in Qt"""
        for rule in self.highlighting_rules:
            match_format = self.highlighting_rules[rule]
            match_iter = rule.globalMatch(text)

            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    match_format
                )
