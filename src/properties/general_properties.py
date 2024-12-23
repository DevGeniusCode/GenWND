from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QGroupBox, QLabel, QLineEdit, QSpinBox,
    QTabWidget, QWidget, QVBoxLayout, QGridLayout
)

from PyQt6.QtGui import QColor
from src.properties.text_color import ColorPickerApp
from src.window.window_properties import WindowProperties


class GeneralForm(QWidget):
    def __init__(self, parent=None, general_data=None):
        super().__init__(parent)
        self.general_data = general_data

        # Form layout for Edit tab
        formLayout = QVBoxLayout(self)

        # Internal reference input
        self.name_label = QLabel("Internal reference identification", self)
        self.name_entry = QLineEdit(self)
        self.name_entry.setObjectName("name_entry")
        formLayout.addWidget(self.name_label)
        formLayout.addWidget(self.name_entry)
        self.name_entry.textChanged.connect(lambda: self.update_key_property('NAME', self.name_entry.text()))

        # Position GroupBox
        self.creation_resolution_width = 100
        self.creation_resolution_height = 100

        self.position_group = QGroupBox("Position", self)
        position_layout = QGridLayout(self.position_group)

        self.upper_left_label = QLabel("Upper Left", self.position_group)
        self.upper_left_x_label = QLabel("X", self.position_group)
        self.upper_left_x_spinbox = QSpinBox(self.position_group)
        self.upper_left_y_label = QLabel("Y", self.position_group)
        self.upper_left_y_spinbox = QSpinBox(self.position_group)

        self.bottom_right_label = QLabel("Bottom Right", self.position_group)
        self.bottom_right_x_label = QLabel("X", self.position_group)
        self.bottom_right_x_spinbox = QSpinBox(self.position_group)
        self.bottom_right_y_label = QLabel("Y", self.position_group)
        self.bottom_right_y_spinbox = QSpinBox(self.position_group)

        self.upper_left_x_spinbox.setMaximum(self.creation_resolution_width)
        self.upper_left_y_spinbox.setMaximum(self.creation_resolution_height)
        self.bottom_right_x_spinbox.setMaximum(self.creation_resolution_width)
        self.bottom_right_y_spinbox.setMaximum(self.creation_resolution_height)

        self.upper_left_x_spinbox.valueChanged.connect(
            lambda value: self.update_sub_property('SCREENRECT', 'UPPERLEFT', [value, self.upper_left_y_spinbox.value()]))
        self.upper_left_y_spinbox.valueChanged.connect(
            lambda value: self.update_sub_property('SCREENRECT', 'UPPERLEFT', [self.upper_left_x_spinbox.value(), value]))
        self.bottom_right_x_spinbox.valueChanged.connect(
            lambda value: self.update_sub_property('SCREENRECT', 'BOTTOMRIGHT', [value, self.bottom_right_y_spinbox.value()]))
        self.bottom_right_y_spinbox.valueChanged.connect(
            lambda value: self.update_sub_property('SCREENRECT', 'BOTTOMRIGHT', [self.bottom_right_x_spinbox.value(), value]))

        position_layout.addWidget(self.upper_left_label, 0, 0)
        position_layout.addWidget(self.upper_left_x_label, 0, 1)
        position_layout.addWidget(self.upper_left_x_spinbox, 0, 2)
        position_layout.addWidget(self.upper_left_y_label, 0, 3)
        position_layout.addWidget(self.upper_left_y_spinbox, 0, 4)

        position_layout.addWidget(self.bottom_right_label, 1, 0)
        position_layout.addWidget(self.bottom_right_x_label, 1, 1)
        position_layout.addWidget(self.bottom_right_x_spinbox, 1, 2)
        position_layout.addWidget(self.bottom_right_y_label, 1, 3)
        position_layout.addWidget(self.bottom_right_y_spinbox, 1, 4)

        self.position_group.setLayout(position_layout)
        formLayout.addWidget(self.position_group)

        # Status GroupBox
        self.status_group = QGroupBox("Status", self)
        status_layout = QVBoxLayout(self.status_group)

        self.status_checkBox_1 = QCheckBox("Status Check 1", self.status_group)
        self.status_checkBox_2 = QCheckBox("Status Check 2", self.status_group)
        self.status_checkBox_3 = QCheckBox("Status Check 3", self.status_group)

        status_layout.addWidget(self.status_checkBox_1)
        status_layout.addWidget(self.status_checkBox_2)
        status_layout.addWidget(self.status_checkBox_3)

        self.status_group.setLayout(status_layout)
        formLayout.addWidget(self.status_group)

        # Style Group
        self.style_group = QGroupBox("Style", self)
        style_layout = QVBoxLayout(self.style_group)

        self.style_checkBox_1 = QCheckBox("Style CheckBox 1", self.style_group)
        self.style_checkBox_2 = QCheckBox("Style CheckBox 2", self.style_group)
        self.style_checkBox_3 = QCheckBox("Style CheckBox 3", self.style_group)

        style_layout.addWidget(self.style_checkBox_1)
        style_layout.addWidget(self.style_checkBox_2)
        style_layout.addWidget(self.style_checkBox_3)

        self.style_group.setLayout(style_layout)
        formLayout.addWidget(self.style_group)

        # Text GroupBox (Style Settings)
        self.text_group = QGroupBox("Text", self)
        text_layout = QVBoxLayout(self.text_group)

        self.text_label = QLabel("Text", self.text_group)
        self.text_entry = QLineEdit(self.text_group)

        self.tooltip_label = QLabel("Tooltip", self.text_group)
        self.tooltip_entry = QLineEdit(self.text_group)

        text_layout.addWidget(self.text_label)
        text_layout.addWidget(self.text_entry)
        text_layout.addWidget(self.tooltip_label)
        text_layout.addWidget(self.tooltip_entry)

        self.text_group.setLayout(text_layout)
        formLayout.addWidget(self.text_group)

        # Font Style
        self.font_group = QGroupBox("Font Style", self)
        font_layout = QVBoxLayout(self.font_group)

        self.bold_checkBox = QCheckBox("Bold", self.font_group)
        self.font_list = QComboBox(self.font_group)
        self.template_label = QLabel("Template", self.font_group)
        self.template_list = QComboBox(self.font_group)

        font_layout.addWidget(self.bold_checkBox)
        font_layout.addWidget(self.font_list)
        font_layout.addWidget(self.template_label)
        font_layout.addWidget(self.template_list)

        self.font_group.setLayout(font_layout)
        formLayout.addWidget(self.font_group)

        # Text Color GroupBox with Tabs for Enable, Disable, Highlight
        self.text_color_group = QGroupBox("Text Color", self)
        color_layout = QVBoxLayout(self.text_color_group)

        # Data for the colors, to pass to the ColorPickerApp
        # color_data = {
        #     "enable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
        #     "disable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
        #     "highlight": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)}
        # }

        # color_data = general_form.text_color
        # self.text_color_tabs = ColorPickerApp(color_data)
        #
        # # Add the tab widget (containing the 3 tabs) to the layout of the group
        # color_layout.addWidget(self.text_color_tabs)

        # Set the layout for the text color group
        self.text_color_group.setLayout(color_layout)

        # Add the text color group to the main form layout
        formLayout.addWidget(self.text_color_group)

    def update_resolution(self, width, height):
        self.creation_resolution_width = width
        self.creation_resolution_height = height
        self.upper_left_x_spinbox.setMaximum(self.creation_resolution_width)
        self.upper_left_y_spinbox.setMaximum(self.creation_resolution_height)
        self.bottom_right_x_spinbox.setMaximum(self.creation_resolution_width)
        self.bottom_right_y_spinbox.setMaximum(self.creation_resolution_height)

    def update_key_property(self, main_key, value=None):
        setattr(self.general_data, main_key, value)

    def update_sub_property(self, main_key, sub_key, value=None):
        attr = getattr(self.general_data, main_key)
        if isinstance(attr, dict):
            if sub_key in attr:
                attr[sub_key] = value
