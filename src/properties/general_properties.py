from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QGroupBox, QLabel, QLineEdit, QSpinBox,
    QTabWidget, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout
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
        self.type = 'USER'

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
        self.tab_widget = QTabWidget(self)

        # First tab
        self.tab1 = QWidget()
        self.tab1_layout = QGridLayout(self.tab1)
        self.status_enable = QCheckBox("Enabled", self.tab1)
        self.status_hidden = QCheckBox("Hidden", self.tab1)
        self.status_see_thru = QCheckBox("See Thru", self.tab1)
        self.status_image = QCheckBox("Image", self.tab1)
        self.status_border = QCheckBox("Border", self.tab1)
        self.status_no_input = QCheckBox("No Input", self.tab1)
        self.tab1_layout.addWidget(self.status_enable, 0, 0)
        self.tab1_layout.addWidget(self.status_hidden, 0, 1)
        self.tab1_layout.addWidget(self.status_see_thru, 1, 0)
        self.tab1_layout.addWidget(self.status_image, 1, 1)
        self.tab1_layout.addWidget(self.status_border, 2, 0)
        self.tab1_layout.addWidget(self.status_no_input, 2, 1)
        self.tab1.setLayout(self.tab1_layout)

        # Second tab
        self.tab2 = QWidget()
        self.tab2_layout = QGridLayout(self.tab2)
        self.status_no_focus = QCheckBox("No Focus", self.tab2)
        self.status_draggable = QCheckBox("Draggable", self.tab2)
        self.status_wrap_centered = QCheckBox("Wrap Centered", self.tab2)
        self.status_on_mouse_down = QCheckBox("On Mouse Down", self.tab2)
        self.status_hotkey_text = QCheckBox("Hotkey Text", self.tab2)
        self.status_right_click = QCheckBox("Right Click", self.tab2)
        self.tab2_layout.addWidget(self.status_no_focus, 0, 0)
        self.tab2_layout.addWidget(self.status_draggable, 0, 1)
        self.tab2_layout.addWidget(self.status_wrap_centered, 1, 0)
        self.tab2_layout.addWidget(self.status_on_mouse_down, 1, 1)
        self.tab2_layout.addWidget(self.status_hotkey_text, 2, 0)
        self.tab2_layout.addWidget(self.status_right_click, 2, 1)
        self.tab2.setLayout(self.tab2_layout)

        # Third tab
        self.tab3 = QWidget()
        self.tab3_layout = QGridLayout(self.tab3)
        self.status_check_like = QCheckBox("Check Like", self.tab3)
        self.status_tabstop = QCheckBox("Tab Stop", self.tab3)
        self.tab3_layout.addWidget(self.status_check_like, 0, 0)
        self.tab3_layout.addWidget(self.status_tabstop, 1, 0)
        self.tab3_layout.setRowStretch(0, 1)
        self.tab3_layout.setRowStretch(1, 1)
        self.tab3_layout.setRowStretch(2, 1)
        self.tab3.setLayout(self.tab3_layout)

        # Add the tabs to the Status
        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")
        status_layout.addWidget(self.tab_widget)
        self.status_group.setLayout(status_layout)
        formLayout.addWidget(self.status_group)

        # # Style Group
        # self.style_group = QGroupBox("Style", self)
        # style_layout = QVBoxLayout(self.style_group)
        #
        # self.style_checkBox_1 = QCheckBox("Style CheckBox 1", self.style_group)
        # self.style_checkBox_2 = QCheckBox("Style CheckBox 2", self.style_group)
        # self.style_checkBox_3 = QCheckBox("Style CheckBox 3", self.style_group)
        #
        # style_layout.addWidget(self.style_checkBox_1)
        # style_layout.addWidget(self.style_checkBox_2)
        # style_layout.addWidget(self.style_checkBox_3)
        #
        # self.style_group.setLayout(style_layout)
        # formLayout.addWidget(self.style_group)

        # Text GroupBox (Style Settings)
        self.text_group = QGroupBox("Text", self)
        text_layout = QVBoxLayout(self.text_group)

        grid_layout = QGridLayout()
        self.text_label = QLabel("Text", self.text_group)
        self.text_entry = QLineEdit(self.text_group)

        self.tooltip_label = QLabel("Tooltip", self.text_group)
        self.tooltip_entry = QLineEdit(self.text_group)

        grid_layout.addWidget(self.text_label, 0, 0)
        grid_layout.addWidget(self.text_entry, 0, 1)
        grid_layout.addWidget(self.tooltip_label, 1, 0)
        grid_layout.addWidget(self.tooltip_entry, 1, 1)

        text_layout.addLayout(grid_layout)

        self.text_group.setLayout(text_layout)
        formLayout.addWidget(self.text_group)

        self.text_entry.textChanged.connect(lambda: self.update_key_property('TEXT', self.text_entry.text()))
        self.tooltip_entry.textChanged.connect(lambda: self.update_key_property('TOOLTIPTEXT', self.tooltip_entry.text()))

        # Font Style
        self.font_group = QGroupBox("Font Style", self)
        font_layout = QVBoxLayout(self.font_group)

        font_h_layout = QHBoxLayout()
        self.bold_checkbox = QCheckBox("Bold", self.font_group)
        self.font_list = QComboBox(self.font_group)

        template_h_layout = QHBoxLayout()
        self.template_label = QLabel("Template", self.font_group)
        self.template_list = QComboBox(self.font_group)

        font_h_layout.addWidget(self.bold_checkbox)
        font_h_layout.addWidget(self.font_list)
        template_h_layout.addWidget(self.template_label)
        template_h_layout.addWidget(self.template_list)

        font_layout.addLayout(font_h_layout)
        font_layout.addLayout(template_h_layout)

        self.font_group.setLayout(font_layout)
        formLayout.addWidget(self.font_group)

        font_list_items = ["Arial", "Times New Roman", "Courier New", "Verdana"]
        template_list_items = ["Template 1", "Template 2", "Template 3"]

        self.font_list.addItems(font_list_items)
        self.template_list.addItems(template_list_items)

        self.font_list.setCurrentText(font_list_items[0])
        self.template_list.setCurrentText(template_list_items[0])

        self.bold_checkbox.toggled.connect(lambda: self.update_sub_property('FONT','name', self.font_list.currentText()))
        self.font_list.currentTextChanged.connect(lambda: self.update_sub_property('FONT', 'bold', self.bold_checkbox.isChecked()))
        self.template_list.currentTextChanged.connect(lambda: self.update_key_property('HEADERTEMPLATE', self.template_list.currentText()))

        # Text Color GroupBox with Tabs for Enable, Disable, Highlight
        self.text_color_group = QGroupBox("Text Color", self)

        # Default colors
        default_color_data = {
            "enable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
            "disable": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)},
            "highlight": {"color": QColor(0, 140, 105, 255), "shadow": QColor(0, 0, 0, 50)}
        }

        # Create ColorPickerApp with color data
        self.text_color_tabs = ColorPickerApp(color_data=default_color_data)
        color_layout = QVBoxLayout(self.text_color_group)
        color_layout.addWidget(self.text_color_tabs)
        color_layout.setContentsMargins(0, 0, 0, 0)
        self.text_color_group.setLayout(color_layout)
        formLayout.addWidget(self.text_color_group)

        # Connecting the color change events to update the properties
        def update_text_color():
            enable_color = self.text_color_tabs.color_data['enable']['color']
            enable_shadow = self.text_color_tabs.color_data['enable']['shadow']
            disable_color = self.text_color_tabs.color_data['disable']['color']
            disable_shadow = self.text_color_tabs.color_data['disable']['shadow']
            highlight_color = self.text_color_tabs.color_data['highlight']['color']
            highlight_shadow = self.text_color_tabs.color_data['highlight']['shadow']

            self.update_sub_property('TEXTCOLOR', 'ENABLED', (
            enable_color.red(), enable_color.green(), enable_color.blue(), enable_color.alpha()))
            self.update_sub_property('TEXTCOLOR', 'ENABLEDBORDER', (
            enable_shadow.red(), enable_shadow.green(), enable_shadow.blue(), enable_shadow.alpha()))
            self.update_sub_property('TEXTCOLOR', 'DISABLED', (
            disable_color.red(), disable_color.green(), disable_color.blue(), disable_color.alpha()))
            self.update_sub_property('TEXTCOLOR', 'DISABLEDBORDER', (
            disable_shadow.red(), disable_shadow.green(), disable_shadow.blue(), disable_shadow.alpha()))
            self.update_sub_property('TEXTCOLOR', 'HILITE', (
            highlight_color.red(), highlight_color.green(), highlight_color.blue(), highlight_color.alpha()))
            self.update_sub_property('TEXTCOLOR', 'HILITEBORDER', (
            highlight_shadow.red(), highlight_shadow.green(), highlight_shadow.blue(), highlight_shadow.alpha()))

        self.text_color_tabs.color_data['enable']['color_button'].clicked.connect(update_text_color)
        self.text_color_tabs.color_data['enable']['shadow_button'].clicked.connect(update_text_color)
        self.text_color_tabs.color_data['disable']['color_button'].clicked.connect(update_text_color)
        self.text_color_tabs.color_data['disable']['shadow_button'].clicked.connect(update_text_color)
        self.text_color_tabs.color_data['highlight']['color_button'].clicked.connect(update_text_color)
        self.text_color_tabs.color_data['highlight']['shadow_button'].clicked.connect(update_text_color)


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
