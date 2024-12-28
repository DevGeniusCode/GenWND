from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QGroupBox, QSpinBox, QLabel, QPushButton, QColorDialog, QHBoxLayout
from PyQt6.QtGui import QColor

class ColorPickerApp(QWidget):
    def __init__(self, color_data=None):
        super().__init__()

        self.color_data = color_data if color_data else {
            "default": {"color": "#ff0000", "shadow": "#000000"}
        }

        self.layout = QVBoxLayout(self)

        if len(self.color_data) == 1:
            self.create_color_controls(list(self.color_data.keys())[0])
        else:
            self.text_color_tabs = QTabWidget(self)
            self.layout.addWidget(self.text_color_tabs)

            for tab_name in self.color_data:
                self.create_tab(tab_name, self.text_color_tabs)

        self.update_buttons_from_color_data()

    def create_tab(self, tab_name, tab_widget):
        """
        Creates a tab with color and shadow controls for the given tab_name.

        Args:
            tab_name (str): The name of the tab.
            tab_widget (QTabWidget): The tab widget where the tab will be added.
        """
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # Color and Shadow Buttons
        color_button = QPushButton(f"Select Main Color ({tab_name.capitalize()})", tab)
        color_button.clicked.connect(lambda: self.open_color_dialog(tab_name, "color"))
        shadow_button = QPushButton(f"Select Shadow Color ({tab_name.capitalize()})", tab)
        shadow_button.clicked.connect(lambda: self.open_color_dialog(tab_name, "shadow"))

        # SpinBox for Alpha channel of Color
        color_alpha_spinbox = QSpinBox(self)
        color_alpha_spinbox.setRange(0, 255)
        color_alpha_spinbox.setValue(QColor(self.color_data[tab_name]["color"]).alpha())

        shadow_alpha_spinbox = QSpinBox(self)
        shadow_alpha_spinbox.setRange(0, 255)
        shadow_alpha_spinbox.setValue(QColor(self.color_data[tab_name]["shadow"]).alpha())

        color_button.setStyleSheet(f"background-color: {QColor(self.color_data[tab_name]['color']).name()};")
        shadow_button.setStyleSheet(f"background-color: {QColor(self.color_data[tab_name]['shadow']).name()};")

        # Layout for the tab
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        color_layout.addWidget(color_button)
        color_layout.addWidget(QLabel("α:"))
        color_layout.addWidget(color_alpha_spinbox)

        shadow_layout = QHBoxLayout()
        shadow_layout.addWidget(QLabel("Shadow:"))
        shadow_layout.addWidget(shadow_button)
        shadow_layout.addWidget(QLabel("α:"))
        shadow_layout.addWidget(shadow_alpha_spinbox)

        tab_layout.addLayout(color_layout)
        tab_layout.addLayout(shadow_layout)

        tab_widget.addTab(tab, tab_name.capitalize())

        self.color_data[tab_name]["color_button"] = color_button
        self.color_data[tab_name]["shadow_button"] = shadow_button
        self.color_data[tab_name]["color_alpha_spinbox"] = color_alpha_spinbox
        self.color_data[tab_name]["shadow_alpha_spinbox"] = shadow_alpha_spinbox

    def create_color_controls(self, tab_name):
        """
        Creates color and shadow controls when there is only one color state.

        Args:
            tab_name (str): The name of the color state.
        """
        color_button = QPushButton(f"Select Main Color ({tab_name.capitalize()})", self)
        color_button.clicked.connect(lambda: self.open_color_dialog(tab_name, "color"))
        shadow_button = QPushButton(f"Select Shadow Color ({tab_name.capitalize()})", self)
        shadow_button.clicked.connect(lambda: self.open_color_dialog(tab_name, "shadow"))

        color_alpha_spinbox = QSpinBox(self)
        color_alpha_spinbox.setRange(0, 255)
        color_alpha_spinbox.setValue(QColor(self.color_data[tab_name]["color"]).alpha())

        shadow_alpha_spinbox = QSpinBox(self)
        shadow_alpha_spinbox.setRange(0, 255)
        shadow_alpha_spinbox.setValue(QColor(self.color_data[tab_name]["shadow"]).alpha())

        color_button.setStyleSheet(f"background-color: {QColor(self.color_data[tab_name]['color']).name()};")
        shadow_button.setStyleSheet(f"background-color: {QColor(self.color_data[tab_name]['shadow']).name()};")

        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setObjectName("colorLabel")
        color_layout.addWidget(color_label)
        color_layout.addWidget(color_button)
        color_layout.addWidget(QLabel("α:"))
        color_layout.addWidget(color_alpha_spinbox)

        shadow_layout = QHBoxLayout()
        shadow_label = QLabel("Shadow:")
        shadow_label.setObjectName("shadowLabel")
        shadow_layout.addWidget(shadow_label)
        shadow_layout.addWidget(shadow_button)
        shadow_layout.addWidget(QLabel("α:"))
        shadow_layout.addWidget(shadow_alpha_spinbox)

        self.layout.addLayout(color_layout)
        self.layout.addLayout(shadow_layout)

        self.color_data[tab_name]["color_button"] = color_button
        self.color_data[tab_name]["shadow_button"] = shadow_button
        self.color_data[tab_name]["color_alpha_spinbox"] = color_alpha_spinbox
        self.color_data[tab_name]["shadow_alpha_spinbox"] = shadow_alpha_spinbox

    def update_buttons_from_color_data(self):
        """
        Updates the button styles and texts based on the current color data.
        """
        for tab_name in self.color_data:
            color = QColor(self.color_data[tab_name]["color"])
            shadow = QColor(self.color_data[tab_name]["shadow"])
            text_color = self.get_contrasting_text_color(color)
            self.color_data[tab_name]["color_button"].setStyleSheet(f"background-color: {color.name()}; color: {text_color.name()};")
            self.color_data[tab_name]["color_button"].setText(f"RGB: {color.red()}, {color.green()}, {color.blue()}")
            text_shadow_color = self.get_contrasting_text_color(shadow)
            self.color_data[tab_name]["shadow_button"].setStyleSheet(f"background-color: {shadow.name()}; color: {text_shadow_color.name()};")
            self.color_data[tab_name]["shadow_button"].setText(f"RGB: {shadow.red()}, {shadow.green()}, {shadow.blue()}")

    def get_contrasting_text_color(self, background_color):
        brightness = self.calculate_brightness(background_color)
        return QColor(255, 255, 255) if brightness < 128 else QColor(0, 0, 0)

    def calculate_brightness(self, color):
        rgb = color.getRgb()
        return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

    def open_color_dialog(self, tab_name, color_type):
        current_color = QColor(self.color_data[tab_name][color_type])
        color = QColorDialog.getColor(current_color, self)
        if color.isValid():
            alpha_value = self.color_data[tab_name][f"{color_type}_alpha_spinbox"].value()
            self.color_data[tab_name][color_type] = color
            button = self.color_data[tab_name][f"{color_type}_button"]
            button.setStyleSheet(f"background-color: {color.name()};")
            button.setText(f"RGB: {color.red()}, {color.green()}, {color.blue()}")