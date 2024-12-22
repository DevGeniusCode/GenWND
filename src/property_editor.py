from PyQt6.QtWidgets import QTabWidget, QTextEdit, QTableView, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

from src.window.line_iterator import LineIterator
from src.window.window_properties import parse_window_properties


class PropertyEditor(QWidget):
    """
    A widget that provides a tabbed interface for viewing and editing object properties.
    """

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        # Create tabs
        self.tabs = QTabWidget(self)
        self.text_tab = QWidget()
        self.edit_tab = QTableView()
        self.property_model = QStandardItemModel()
        self.edit_tab.setModel(self.property_model)

        # Set headers for the properties table
        self.property_model.setHorizontalHeaderLabels(["Property", "Value"])

        # Add tabs
        self.tabs.addTab(self.edit_tab, "Edit")
        self.tabs.addTab(self.text_tab, "Text")

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select an object to display its properties.", self)
        self.empty_label.setObjectName("emptyLabel")  # Set the class name for QSS styling
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(f"qproperty-alignment: {int(Qt.AlignmentFlag.AlignCenter)};")

        # Initially hide the tabs (when there's no content)
        self.tabs.setVisible(False)

        # Layout for text tab
        text_layout = QVBoxLayout()

        # QTextEdit (text editing area)
        self.text_edit = QTextEdit(self.text_tab)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        text_layout.addWidget(self.text_edit)

        # Layout for buttons inside the text tab
        self.buttons_layout = QHBoxLayout()

        # Save and Reset buttons
        self.save_button = QPushButton("Load", self.text_tab)
        self.reset_button = QPushButton("Reset", self.text_tab)
        self.error_label = QLabel("", self.text_tab)  # To display save error messages
        self.error_label.setObjectName("errorLabel")  # Apply the error label style

        # Connect buttons
        self.save_button.clicked.connect(self.save_properties)
        self.reset_button.clicked.connect(self.reset_text)

        # Add buttons and error label to layout
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.reset_button)

        # Add buttons layout to the text tab layout
        text_layout.addLayout(self.buttons_layout)

        # Layout for error message, placed under the buttons
        self.error_layout = QVBoxLayout()
        self.error_layout.addWidget(self.error_label)  # Error label under buttons
        text_layout.addLayout(self.error_layout)

        # Set layout for text_tab
        self.text_tab.setLayout(text_layout)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.empty_label)
        self.setLayout(layout)

        # Store the original text for reset functionality
        self.original_text = ""

    def load_property(self, properties):
        """Loads the properties of a selected object into the editor."""
        self.clear()  # Clear any previous data

        if not properties:
            self.empty_label.setVisible(True)  # Show the empty label if no properties
            return

        self.empty_label.setVisible(False)  # Hide the empty label if there are properties
        self.tabs.setVisible(True)

        # Text tab
        self.original_text = repr(properties)  # Store the original text
        self.text_edit.setPlainText(self.original_text)

        # Edit tab
        self.property_model.clear()
        self.property_model.setHorizontalHeaderLabels(["Property", "Value"])
        for key, value in properties.items():
            key_item = QStandardItem(key)
            value_item = QStandardItem(str(value))
            self.property_model.appendRow([key_item, value_item])

    def display_error(self, error_message):
        """Displays an error message in the property editor."""
        self.text_edit.setPlainText(f"Error: {error_message}")
        self.property_model.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.empty_label.setText(f"Error: {error_message}")

        # Set the style for the error label to show red text
        self.error_label.setText(f"Error: {error_message}")

    def clear(self):
        """Clears all content in the editor."""
        self.text_edit.clear()
        self.property_model.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
        self.error_label.clear()  # Clear the error label text and styling

    def save_properties(self):
        """Saves the current text into the properties object."""
        text = self.text_edit.toPlainText()

        try:
            window_properties = parse_window_properties(LineIterator(text.splitlines()))

            # If no error occurs, update the properties
            self.error_label.setText("")
            self.main_window.selected_object.properties = window_properties
            self.error_label.setText("Loaded successfully!")
            self.error_label.setStyleSheet("color: green;")
        except Exception as e:
            self.error_label.setText(f"Save failed: {str(e)}")

    def reset_text(self):
        """Resets the text to its original state."""
        self.text_edit.setPlainText(self.original_text)
        self.error_label.clear()
        self.error_label.setObjectName("")
