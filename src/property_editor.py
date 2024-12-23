from PyQt6.QtWidgets import QTabWidget, QTextEdit, QTableView, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

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

        # Create tabs
        self.tabs = QTabWidget(self)

        # Initialize general and raw tabs
        self.create_general_tab()
        self.create_raw_tab()

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select an object to display its properties.", self)
        self.empty_label.setObjectName("emptyLabel")  # Set the class name for QSS styling
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(f"qproperty-alignment: {int(Qt.AlignmentFlag.AlignCenter)};")

        # Initially hide the tabs (when there's no content)
        self.tabs.setVisible(False)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.empty_label)
        self.setLayout(layout)

        # Store the original raw for reset functionality
        self.original_raw = ""

    def create_general_tab(self):
        """Creates the General tab and its components."""
        self.general_tab = QWidget()
        self.general_properties = GeneralForm(self, self.properties)
        general_layout = QVBoxLayout(self.general_tab)  # Layout for the general tab
        general_layout.addWidget(self.general_properties)
        self.tabs.addTab(self.general_tab, "General Properties")

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
        self.reset_button.clicked.connect(self.reset_raw)

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

    def load_property(self, properties):
        """Loads the properties of a selected object into the editor."""
        self.clear()  # Clear any previous data

        if not properties:
            self.empty_label.setVisible(True)  # Show the empty label if no properties
            return

        self.properties = properties
        self.empty_label.setVisible(False)  # Hide the empty label if there are properties
        self.tabs.setVisible(True)

        # Raw tab
        self.original_raw = repr(self.properties)
        self.raw_edit.setPlainText(self.original_raw)

        # General tab
        # Populate the general_properties fields with the property values
        self.general_properties.general_data = self.properties

        # Set NAME value
        self.general_properties.name_entry.setText(self.properties.get('NAME', ''))

        # Set SCREENRECT values (we expect it to be a list of dictionaries)
        screen_rect = self.properties.get('SCREENRECT', [])

        creation_resolution = screen_rect.get('CREATIONRESOLUTION', [800, 600])
        self.general_properties.update_resolution(creation_resolution[0], creation_resolution[1])

        upper_left = screen_rect.get('UPPERLEFT', [0, 0])
        self.general_properties.upper_left_x_spinbox.setValue(upper_left[0])
        self.general_properties.upper_left_y_spinbox.setValue(upper_left[1])

        bottom_right = screen_rect.get('BOTTOMRIGHT', [0, 0])
        self.general_properties.bottom_right_x_spinbox.setValue(bottom_right[0])
        self.general_properties.bottom_right_y_spinbox.setValue(bottom_right[1])

        # # Set STATUS values (checkboxes for each status)
        # status_values = self.properties.get('STATUS', [])
        # for idx, checkbox in enumerate(self.general_properties.status_checkboxes):
        #     if idx < len(status_values):
        #         checkbox.setChecked(status_values[idx] == 'ENABLED')
        #
        # # Set STYLE values (checkboxes for each style)
        # style_values = self.properties.get('STYLE', [])
        # for idx, checkbox in enumerate(self.general_properties.style_checkboxes):
        #     if idx < len(style_values):
        #         checkbox.setChecked(style_values[idx] == 'SCROLLLISTBOX')
        #
        # # Set FONT values (NAME, SIZE, BOLD)
        # font_data = self.properties.get('FONT', [])
        # self.general_properties.font_name_entry.setText(font_data[0].get('NAME', ''))
        # self.general_properties.font_size_spinbox.setValue(font_data[1].get('SIZE', 10))
        # self.general_properties.bold_checkbox.setChecked(font_data[2].get('BOLD', 0) == 1)
        #
        # # Set TOOLTIP value
        # self.general_properties.tooltip_delay_spinbox.setValue(self.properties.get('TOOLTIPDELAY', -1))
        #
        # # Set TEXTCOLOR values (color pickers for ENABLED, DISABLED, HILITE)
        # text_color_data = self.properties.get('TEXTCOLOR', [])
        # self.general_properties.text_color_tabs.set_color('enabled', text_color_data[0].get('ENABLED', [0, 0, 0, 0]))
        # self.general_properties.text_color_tabs.set_color('disabled', text_color_data[2].get('DISABLED', [0, 0, 0, 0]))
        # self.general_properties.text_color_tabs.set_color('highlight', text_color_data[4].get('HILITE', [0, 0, 0, 0]))

    def display_error(self, error_message):
        """Displays an error message in the property editor."""
        self.raw_edit.setPlainText(f"Error: {error_message}")
        # self.property_model.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.empty_label.setText(f"Error: {error_message}")

        # Set the style for the error label to show red text
        self.error_label.setText(f"Error: {error_message}")

    def clear(self):
        """Clears all content in the editor."""
        self.raw_edit.clear()
        # self.property_model.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.error_label.clear()  # Clear the error label text and styling

    def save_raw_properties(self):
        """Saves the current raw into the properties object."""
        raw = self.raw_edit.toPlainText()

        try:
            window_properties = parse_window_properties(LineIterator(raw.splitlines()))

            # If no error occurs, update the properties
            self.error_label.setText("")
            self.main_window.selected_object.properties = window_properties
            self.error_label.setText("Loaded successfully!")
            self.error_label.setStyleSheet("color: green;")
        except Exception as e:
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText(f"Save failed: {str(e)}")

    def reset_raw(self):
        """Resets the raw to its original state."""
        self.raw_edit.setPlainText(self.original_raw)
        self.error_label.clear()
        self.error_label.setObjectName("")
