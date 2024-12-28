from PyQt6.QtWidgets import QTreeView, QLabel, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor

class ObjectTree(QWidget):
    # Signal to notify when an object is selected
    object_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        # Create the tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # Set up signal for item selection
        self.tree_view.selectionModel().selectionChanged.connect(self.on_item_selected)
        self.tree_view.setVisible(False)

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select a file to display its Windows.", self)
        self.empty_label.setObjectName("emptyLabel")  # Set the class name for QSS styling
        self.empty_label.setWordWrap(True)
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create buttons for saving and resetting
        self.save_button = QPushButton("Save to file")
        self.reset_button = QPushButton("Reset from file")
        self.save_button.setVisible(False)  # Disable until a file is selected
        self.reset_button.setVisible(False)

        # Create the button layout at the bottom
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)

        # Create the tree layout
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree_view)
        self.tree_layout.addLayout(self.button_layout)

        # Create the main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.tree_layout)
        self.layout.setStretch(0,1)

        # Connect buttons to their functions
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.update_buttons_state()


    def load_objects(self, windows):
        """Load the windows into the tree view."""
        if not windows:
            raise ValueError("Empty or invalid file")

        # Hide the empty label and show the buttons if there are file windows
        self.empty_label.setVisible(False)
        self.save_button.setVisible(True)
        self.reset_button.setVisible(True)
        self.tree_view.setVisible(True)

        self.model.clear()
        self._populate_tree(windows, self.model)

    def _populate_tree(self, windows, parent_item):
        """
        Recursively populate the tree with windows and their children.
        :param windows: List of Window objects
        :param parent_item: Parent item in the tree to append items
        """
        for window in windows:
            item = QStandardItem(f"{window.properties.get('WINDOWTYPE')} - {window.properties.get('NAME', 'Unnamed')}")
            item.setData(window)
            parent_item.appendRow(item)
            if window.children:
                self._populate_tree(window.children, item)

    def on_item_selected(self, selected, deselected):
        """
        Handle item selection changes in the object tree.
        """
        selected_indexes = self.tree_view.selectedIndexes()
        if selected_indexes:
            # Get the selected item
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            selected_object = selected_item.data()
            self.object_selected_signal.emit(selected_object)

    def display_error(self, error_message):
        """
        Display an error message in the object tree.
        :param error_message: The error message to display.
        """
        # Clear the model to ensure no old data is left
        self.model.clear()
        self.empty_label.setVisible(False)
        self.tree_view.setVisible(True)

        # Create an error item to show in the tree
        error_item = QStandardItem("Error")
        error_item.setForeground(QColor("red"))
        error_item.setEditable(False)

        # Add the error message as a child item
        error_message_item = QStandardItem(error_message)
        error_message_item.setEditable(False)
        error_item.appendRow(error_message_item)

        # Add the error item as the root item of the model
        self.model.appendRow(error_item)

        # Optionally expand the error item so it's visible
        self.tree_view.expandAll()

    def clear(self):
        self.model.clear()
        self.empty_label.setVisible(True)
        self.save_button.setVisible(False)
        self.reset_button.setVisible(False)
        self.tree_view.setVisible(False)

    def on_save_button_clicked(self):
        """
        Handle save button click event. Calls the save_file function from the main window.
        """
        self.main_window.save_file()

    def on_reset_button_clicked(self):
        """
        Handle reset button click event. Calls the load_wnd_file function from the main window.
        """
        selected_file = self.main_window.selected_file
        self.main_window.load_wnd_file(selected_file)

    def update_buttons_state(self):
        """
        Update the state of the save and reset buttons based on the is_modified flag.
        """
        is_modified = getattr(self.main_window, "is_modified", False)
        if is_modified:
            self.save_button.setEnabled(True)
            self.reset_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
            self.reset_button.setEnabled(False)
