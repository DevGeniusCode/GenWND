from PyQt6.QtWidgets import QTabWidget, QTextEdit, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import copy

from src.properties.control_properties import ControlForm
from src.window.line_iterator import LineIterator
from src.window.window_properties import parse_window_properties
from src.properties.general_properties import GeneralForm

class PropertyEditor(QWidget):
    """
    A widget that provides a tabbed interface for viewing and editing object properties.
    """

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.properties = {}
        self.control_object = None

        # Create tabs
        self.tabs = QTabWidget(self)
        self.create_general_tab()
        self.create_control_tab()
        self.create_raw_tab()

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select an object to display its properties.", self)
        self.empty_label.setObjectName("emptyLabel")  # Set the class name for QSS styling
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(f"qproperty-alignment: {int(Qt.AlignmentFlag.AlignCenter)};")

        # Initially hide the tabs (when there's no content)
        self.tabs.setVisible(False)
        self.tabs.currentChanged.connect(self.tab_changed)


        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.empty_label)
        self.setLayout(layout)
        self.original_properties = ''

    def create_general_tab(self):
        """Creates the General tab and its components."""
        self.general_tab = QWidget()
        self.general_properties = GeneralForm(self, general_data=self.properties, main_window=self.main_window)
        general_layout = QVBoxLayout(self.general_tab)
        general_layout.addWidget(self.general_properties)
        self.tabs.addTab(self.general_tab, "General Properties")

    def create_control_tab(self):
        """Creates the Control tab and its components."""
        self.control_tab = QWidget()
        # self.control_properties = QWidget()
        # control_layout = QVBoxLayout(self.control_tab)
        # control_layout.addWidget(self.control_properties)
        self.tabs.addTab(self.control_tab, "Control Properties")

    def create_raw_tab(self):
        """Creates the Raw tab and its components."""
        raw_layout = QVBoxLayout()
        self.raw_tab = QWidget()
        self.tabs.addTab(self.raw_tab, "Raw Text")

        # QTextEdit (raw editing area)
        self.raw_edit = QTextEdit(self.raw_tab)
        self.raw_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        raw_layout.addWidget(self.raw_edit)

        # Layout for buttons inside the raw tab
        self.buttons_layout = QHBoxLayout()

        # Save and Reset buttons
        self.save_button = QPushButton("Load", self.raw_tab)
        self.reset_button = QPushButton("Reset", self.raw_tab)
        self.error_label = QLabel("", self.raw_tab)  # To display save error messages
        self.error_label.setObjectName("errorLabel")  # Apply the error label style

        # Connect buttons
        self.save_button.clicked.connect(self.save_raw_properties)
        self.reset_button.clicked.connect(self.reset)

        # Add buttons and error label to layout
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.reset_button)

        # Add buttons layout to the raw tab layout
        raw_layout.addLayout(self.buttons_layout)

        # Layout for error message, placed under the buttons
        self.error_layout = QVBoxLayout()
        self.error_layout.addWidget(self.error_label)  # Error label under buttons
        raw_layout.addLayout(self.error_layout)

        # Set layout for raw_tab
        self.raw_tab.setLayout(raw_layout)

    def load_property(self, control):
        """Loads the properties of a selected object into the editor."""
        status = self.main_window.is_modified
        self.clear()  # Clear any previous data
        properties = control.properties
        if not properties:
            self.empty_label.setVisible(True)  # Show the empty label if no properties
            return

        self.original_properties = copy.deepcopy(properties)
        self.properties = control.properties
        self.control_object = control
        self.empty_label.setVisible(False)
        self.tabs.setVisible(True)

        # Load the tabs
        self.load_general_properties()
        self.load_control_properties()
        self.load_raw_properties()

        self.main_window.update_modified_state(status)

    def load_control_properties(self, properties=None):
        """Loads the control properties into the editor."""
        if not properties:
            properties = self.properties

        # Ensure the control tab has a layout
        if self.control_tab.layout() is None:
            self.control_tab.setLayout(QVBoxLayout())

        # Clear the layout of the control tab
        for i in reversed(range(self.control_tab.layout().count())):
            widget = self.control_tab.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.control_properties = ControlForm(self, control_attributes=properties)
        self.control_tab.layout().addWidget(self.control_properties)
        self.control_properties.update_modified_state = self.main_window.update_modified_state

        # self.control_properties.type = properties.get('WINDOWTYPE', 'No type')
        # self.control_properties.type_label.setText(f"Type: {self.control_properties.type}")

    def load_general_properties(self, properties=None):
        """Loads the general properties into the editor."""

        if not properties:
            properties = self.properties
        # General tab
        self.general_properties.general_data = properties
        self.general_properties.type = properties.get('WINDOWTYPE', 'USER')

        # Set NAME value
        self.general_properties.name_entry.setText(properties.get('NAME', ''))

        # Set SCREENRECT values
        screen_rect = properties.get('SCREENRECT', [])

        creation_resolution = screen_rect.get('CREATIONRESOLUTION', [800, 600])
        self.general_properties.update_resolution(creation_resolution[0], creation_resolution[1])

        upper_left = screen_rect.get('UPPERLEFT', [0, 0])
        self.general_properties.upper_left_x_spinbox.setValue(upper_left[0])
        self.general_properties.upper_left_y_spinbox.setValue(upper_left[1])

        bottom_right = screen_rect.get('BOTTOMRIGHT', [0, 0])
        self.general_properties.bottom_right_x_spinbox.setValue(bottom_right[0])
        self.general_properties.bottom_right_y_spinbox.setValue(bottom_right[1])

        # Set STATUS values (checkboxes for each status)
        status_values = properties.get('STATUS', [])
        status_dict = {
            self.general_properties.status_enable: "ENABLED",
            self.general_properties.status_hidden: "HIDDEN",
            self.general_properties.status_see_thru: "SEE_THRU",
            self.general_properties.status_image: "IMAGE",
            self.general_properties.status_border: "BORDER",
            self.general_properties.status_no_input: "NOINPUT",
            self.general_properties.status_no_focus: "NOFOCUS",
            self.general_properties.status_draggable: "DRAGABLE",
            self.general_properties.status_wrap_centered: "WRAP_CENTERED",
            self.general_properties.status_on_mouse_down: "ON_MOUSE_DOWN",
            self.general_properties.status_hotkey_text: "HOTKEY_TEXT",
            self.general_properties.status_right_click: "RIGHT_CLICK",
            self.general_properties.status_check_like: "CHECK_LIKE",
            self.general_properties.status_tabstop: "TABSTOP"
        }

        # Iterate over the status_dict and check the checkboxes based on status_values
        for checkbox, status_key in status_dict.items():
            if status_key in status_values:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

        # Set FONT values and TEMPLATE
        font_data = properties.get('FONT', [])
        font_name = font_data.get('name')
        if font_name not in [self.general_properties.font_list.itemText(i) for i in range(self.general_properties.font_list.count())]:
            self.general_properties.font_list.addItem(font_name)
        self.general_properties.font_list.setCurrentText(font_name)
        self.general_properties.bold_checkbox.setChecked(font_data['bold'] == 1)

        template_name = properties.get('HEADERTEMPLATE', '')
        if template_name not in [self.general_properties.template_list.itemText(i) for i in range(self.general_properties.template_list.count())]:
            self.general_properties.template_list.addItem(template_name)
        self.general_properties.template_list.setCurrentText(template_name)

        # Set TEXT and TOOLTIP value
        self.general_properties.text_entry.setText(properties.get('TEXT', ''))
        self.general_properties.tooltip_entry.setText(properties.get('TOOLTIPTEXT', ''))

        # Set TEXTCOLOR values
        text_color_data = properties.get('TEXTCOLOR', {})
        enable_color = text_color_data.get('ENABLED', "#ff0000")
        enable_shadow = text_color_data.get('ENABLEDBORDER', "#000000")
        disable_color = text_color_data.get('DISABLED', "#00ff00")
        disable_shadow = text_color_data.get('DISABLEDBORDER', "#000000")
        highlight_color = text_color_data.get('HILITE', "#0000ff")
        highlight_shadow = text_color_data.get('HILITEBORDER', "#000000")

        # Now pass these values to the ColorPickerApp widget
        self.general_properties.text_color_tabs.color_data['enable']['color'] = \
            QColor(enable_color[0], enable_color[1], enable_color[2], enable_color[3])
        self.general_properties.text_color_tabs.color_data['enable']['shadow'] = \
            QColor(enable_shadow[0], enable_shadow[1], enable_shadow[2], enable_shadow[3])
        self.general_properties.text_color_tabs.color_data['disable']['color'] = \
            QColor(disable_color[0], disable_color[1], disable_color[2], disable_color[3])
        self.general_properties.text_color_tabs.color_data['disable']['shadow'] = \
            QColor(disable_shadow[0], disable_shadow[1], disable_shadow[2], disable_shadow[3])
        self.general_properties.text_color_tabs.color_data['highlight']['color'] = \
            QColor(highlight_color[0], highlight_color[1], highlight_color[2], highlight_color[3])
        self.general_properties.text_color_tabs.color_data['highlight']['shadow'] = \
            QColor(highlight_shadow[0], highlight_shadow[1], highlight_shadow[2], highlight_shadow[3])
        self.general_properties.text_color_tabs.update_buttons_from_color_data()

    def load_raw_properties(self):
        """Loads the raw properties into the raw editor."""
        self.raw_edit.setPlainText(repr(self.control_object))

    def display_error(self, error_message):
        """Displays an error message in the property editor."""
        self.raw_edit.setPlainText(f"Error: {error_message}")
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.empty_label.setText(f"Error: {error_message}")

        # Set the style for the error label to show red text
        self.error_label.setText(f"Error: {error_message}")

    def clear(self):
        """Clears all content in the editor."""
        self.raw_edit.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.error_label.clear()  # Clear the error label text and styling

    def save_raw_properties(self):
        """Saves the current raw into the properties object."""
        raw = self.raw_edit.toPlainText()

        try:
            self.control_object = parse_window_properties(LineIterator(raw.splitlines()),
                                                      window_uuid=self.control_object.window_uuid,
                                                      file_name=self.control_object.file_name)

            # If no error occurs, update the properties
            self.properties = self.control_object.properties
            self.error_label.setText("")
            self.main_window.selected_object.properties = self.properties
            self.load_general_properties()
            self.main_window.update_modified_state(True)
            self.error_label.setText("Loaded successfully!")
            self.error_label.setStyleSheet("color: green;")
        except Exception as e:
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText(f"Save failed: {str(e)}")

    def reset(self):
        """Resets the raw to its original state."""
        self.main_window.selected_object.properties = copy.deepcopy(self.original_properties)
        self.properties = self.main_window.selected_object.properties
        self.load_raw_properties()
        self.load_general_properties()
        self.load_control_properties()
        self.error_label.clear()
        self.error_label.setObjectName("")
        self.error_label.setText("Reset successfully!")
        self.error_label.setStyleSheet("color: green;")

    def tab_changed(self, index):
        if index == 2:
            self.load_raw_properties()
        elif index == 1:
            self.load_control_properties()