"""
Docked windows wrapper
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from SummaryTree import *

class CustomDock():
    def __init__(self, parent):
        self.parent = parent
        self.dock = QDockWidget(parent)
        self.content = QWidget()
        self.setupUi()
        self.add_to_parent()

    def setupUi(self):
        """UI setup"""
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Custom Dock')

    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

    def set_visible(self, visibility):
        """Sets visiblity of the custom dock"""
        self.dock.setVisible(visibility)

    def connect_visiblity_action(self, action_slot):
        """Connect the visible event to view action"""
        self.dock.visibilityChanged.connect(action_slot)

class SummaryDock(CustomDock):
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        cd_label = QLabel(self.content)
        cd_label.setText('Current Directory')
        cd_url = QLineEdit(self.content)
        cd_url.setReadOnly(True)
        cd_container = QHBoxLayout()
        cd_container.addWidget(cd_label)
        cd_container.addWidget(cd_url)
        v_layout = QVBoxLayout(self.content)
        v_layout.addLayout(cd_container)

        self.summary_tree_view = SummaryTree()
        v_layout.addWidget(self.summary_tree_view)

        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Submissions Summary')

    def add_to_parent(self):
        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

    def connect_selected(self, handler):
        """Connect the signal to the slot"""
        if self.summary_tree_view is None:
            return

        self.summary_tree_view.selected.connect(handler)

class SubmissionDock(CustomDock):
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        """Sets up the shows submission details"""
        l_name = QLabel(self.content)
        l_email = QLabel(self.content)
        l_id = QLabel(self.content)
        l_csid = QLabel(self.content)
        l_date = QLabel(self.content)
        l_name.setText('Name')
        l_email.setText('Email')
        l_id.setText('ID')
        l_csid.setText('CSID')
        l_date.setText('Date')

        t_name = QLineEdit(self.content)
        t_email = QLineEdit(self.content)
        t_id = QLineEdit(self.content)
        t_csid = QLineEdit(self.content)
        t_date = QLineEdit(self.content)
        t_name.setReadOnly(True)
        t_email.setReadOnly(True)
        t_id.setReadOnly(True)
        t_csid.setReadOnly(True)
        t_date.setReadOnly(True)

        # Add to grid layout
        layout = QGridLayout(self.content)
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

        # Self properties
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Submission Details')

    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock)

class NoteDock(CustomDock):
    """Dock that shows a textbox of info.txt"""
    def __init__(self, parent):
        super().__init__(parent)

    def setupUi(self):
        layout = QVBoxLayout(self.content)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText('Submission\'s "info.txt" will be displayed here')

        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(8)
        self.text_edit.setFont(font)

        layout.addWidget(self.text_edit)
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Notes')

    def add_to_parent(self):
        """Add current docked window to main window"""
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def set_note(self, note):
        """Set the text of the text_edit that is suppose to be notes"""
        self.text_edit.setText(note)


class VerdictDock(CustomDock):
    """Docking class widget for entering marks"""
    def __init__(self, parent):
        super().__init__(parent)
        self.rubric = None

    def setupUi(self):
        """Setup UI"""
        l_mark = QLabel(self.content)
        l_mark.setText('Mark')
        sl_mark = QSlider(self.content)
        sl_mark.setMaximum(5)
        sl_mark.setOrientation(Qt.Horizontal)
        sl_mark.setTickPosition(QSlider.TicksBelow)
        sb_mark = QSpinBox(self.content)
        sb_mark.setMinimum(0)
        sb_mark.setMaximum(5)

        # Connect local signals between the slider and spinbox
        sl_mark.valueChanged.connect(
            lambda x: sb_mark.setValue(sl_mark.value()))
        sb_mark.valueChanged.connect(
            lambda x: sl_mark.setValue(sb_mark.value()))

        # Put all into grid
        self.layout = QGridLayout(self.content)
        self.layout.addWidget(l_mark, 0, 0, 1, 1)
        self.layout.addWidget(sl_mark, 0, 1, 1, 1)
        self.layout.addWidget(sb_mark, 0, 2, 1, 1)

        # Add to window
        self.dock.setWidget(self.content)
        self.dock.setWindowTitle('Verdict')

    def add_to_parent(self):
        """Add the current docked widget to the main window"""
        self.parent.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def clear_rubric(self):
        """Clears all the widget in the verdict"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_rubric(self, rubric):
        """Loads a rubric template from JSON parsed obj"""
        self.rubric = rubric
        self.clear_rubric()

        index = 0

        # Label will act as a key
        labels = {}
        sliders = {}
        values = {}
        for criteria, markings in rubric.items():
            label = QLabel(self.content)
            label.setText(criteria)
            slider = QSlider(self.content)
            slider.setMinimum(0)
            slider.setMaximum(len(markings) - 1)
            slider.setOrientation(Qt.Horizontal)
            slider.setTickPosition(QSlider.TicksBelow)
            value = QLabel(self.content)
            value.setText('0')

            # Add to grid
            self.layout.addWidget(label, index, 0, 1, 1)
            self.layout.addWidget(slider, index, 1, 1, 1)
            self.layout.addWidget(value, index, 2, 1, 1)

            # Make reference via dictionary
            labels[index] = label
            sliders[index] = slider
            values[index] = value

            # Increment grid index
            index = index + 1

        for i in range(len(rubric.items())):
            sliders[i].valueChanged.connect(
                lambda x, i=i: values[i].setText(str(self.rubric[labels[i].text()][x]))
            )
