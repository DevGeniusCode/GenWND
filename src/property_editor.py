from PyQt6.QtWidgets import QTabWidget, QTextEdit, QTableView, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt


class PropertyEditor(QWidget):
    """
    A widget that provides a tabbed interface for viewing and editing object properties.

    This widget displays property data in two tabs: a "Text" tab for viewing a text representation
    and an "Edit" tab for viewing and editing individual properties as a table.

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create tabs
        self.tabs = QTabWidget(self)
        self.text_tab = QTextEdit()
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

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.empty_label)  # Add the empty label to the layout
        self.setLayout(layout)

    def load_property(self, properties):
        """Loads the properties of a selected object into the editor."""
        self.clear()  # Clear any previous data

        if not properties:
            self.empty_label.setVisible(True)  # Show the empty label if no properties
            return

        self.empty_label.setVisible(False)  # Hide the empty label if there are properties
        self.tabs.setVisible(True)


        # Text tab
        self.text_tab.setPlainText(repr(properties))

        # Edit tab
        self.property_model.clear()
        self.property_model.setHorizontalHeaderLabels(["Property", "Value"])
        for key, value in properties.items():
            key_item = QStandardItem(key)
            value_item = QStandardItem(str(value))
            self.property_model.appendRow([key_item, value_item])

    def display_error(self, error_message):
        """Displays an error message in the property editor."""

        # Show the error in the text tab
        self.text_tab.setPlainText(f"Error: {error_message}")

        # Clear the edit tab content
        self.property_model.clear()

        # Hide the entire QTabWidget, including all tabs
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)  # Show the empty label with error message
        self.empty_label.setText(f"Error: {error_message}")

    def clear(self):
        """Clears all content in the editor."""
        self.text_tab.clear()
        self.property_model.clear()
        self.tabs.setVisible(False)
        self.empty_label.setVisible(True)
