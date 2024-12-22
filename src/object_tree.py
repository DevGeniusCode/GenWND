from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal, QObject


class ObjectTree(QTreeView):
    # Signal to notify when an object is selected
    object_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        # Set up signal for item selection
        self.selectionModel().selectionChanged.connect(self.on_item_selected)

    def load_objects(self, windows):
        """Load the windows into the tree view."""
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
        selected_indexes = self.selectedIndexes()
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
        self.expandAll()
