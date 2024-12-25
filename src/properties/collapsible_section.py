from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QGroupBox, QScrollArea, QSizePolicy


class CollapsibleSection(QFrame):
    sectionToggled = pyqtSignal()

    def __init__(self, title, parent=None, section_manager=None):
        super().__init__(parent)
        self._is_collapsed = True
        self.section_manager = section_manager
        self.section_manager.add_section(self)

        self._title_frame = self.TitleFrame(title, self._is_collapsed)
        self._content_group = QGroupBox(self)
        self._content_layout = QVBoxLayout(self._content_group)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._content_group)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._title_frame)
        self.layout().addWidget(self._scroll_area)
        self._scroll_area.setVisible(not self._is_collapsed)

        self._title_frame.clicked.connect(self.toggle_collapsed)

        # Scroll indicators
        self._scroll_up_indicator = QLabel("▲", self._scroll_area)
        self._scroll_down_indicator = QLabel("▼", self._scroll_area)
        self._scroll_up_indicator.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._scroll_down_indicator.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._scroll_up_indicator.setVisible(False)
        self._scroll_down_indicator.setVisible(False)

        self._scroll_area.verticalScrollBar().valueChanged.connect(self.update_scroll_indicators)

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def setMaximumWidth(self, width):
        super().setMaximumWidth(width)
        self._content_group.setMaximumWidth(width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content_group.setMaximumWidth(self.width())

    def toggle_collapsed(self):
        self.section_manager.close_all_sections_except(self)
        self._is_collapsed = not self._is_collapsed
        self._scroll_area.setVisible(not self._is_collapsed)
        self._title_frame.setArrow(self._is_collapsed)
        self._title_frame.setProperty("expanded", not self._is_collapsed)
        self._title_frame.style().unpolish(self._title_frame)
        self._title_frame.style().polish(self._title_frame)
        self.update_scroll_indicators()

    def update_scroll_indicators(self):
        scroll_bar = self._scroll_area.verticalScrollBar()
        self._scroll_up_indicator.setVisible(scroll_bar.value() > 0)
        self._scroll_down_indicator.setVisible(scroll_bar.value() < scroll_bar.maximum())

    class TitleFrame(QFrame):
        clicked = pyqtSignal()

        def __init__(self, title, collapsed, parent=None):
            super().__init__(parent)
            self.setObjectName("TitleFrame")
            self._hlayout = QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._arrow = self.Arrow(collapsed)
            self._title = QLabel(title)

            self._hlayout.addWidget(self._arrow)
            self._hlayout.addWidget(self._title)

            self.setMinimumHeight(24)

        def mousePressEvent(self, event):
            self.clicked.emit()

        def setArrow(self, collapsed):
            self._arrow.setArrow(collapsed)

        class Arrow(QFrame):
            def __init__(self, collapsed, parent=None):
                super().__init__(parent)
                self.setMaximumSize(24, 24)
                self._arrow = None
                self.setArrow(collapsed)

            def setArrow(self, collapsed):
                if not collapsed:
                    self._arrow = [QPoint(7, 8), QPoint(17, 8), QPoint(12, 13)]
                else:
                    self._arrow = [QPoint(8, 7), QPoint(13, 12), QPoint(8, 17)]

            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setBrush(QColor(192, 192, 192))
                painter.setPen(QColor(64, 64, 64))
                painter.drawPolygon(*self._arrow)
                painter.end()


class SectionManager:
    def __init__(self):
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def close_all_sections_except(self, opened_section):
        for section in self.sections:
            if section != opened_section and not section._is_collapsed:
                section.toggle_collapsed()