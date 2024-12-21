from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal, QObject


class ObjectTree(QTreeView):
    # Define a new signal to notify MainWindow when an object is selected
    object_selected_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        # Set up signal for item selection
        self.selectionModel().selectionChanged.connect(self.on_item_selected)

    def load_objects(self, windows):
        """
        Load windows into the tree view.
        :param windows: List of Window objects to display in the tree.
        """
        self.model.clear()
        self._populate_tree(windows, self.model)

    def _populate_tree(self, windows, parent_item):
        """
        Recursively populate the tree with windows and their children.
        :param windows: List of Window objects
        :param parent_item: Parent item in the tree to append items
        """
        for window in windows:
            item = QStandardItem(f"{window.options.get('WINDOWTYPE')} - {window.options.get('NAME', 'Unnamed')}")
            parent_item.appendRow(item)
            if window.children:
                self._populate_tree(window.children, item)

    def on_item_selected(self, selected, deselected):
        """
        Handle item selection changes in the object tree.
        """
        selected_indexes = self.selectedIndexes()
        if selected_indexes:
            # Get the selected item and extract its text
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            selected_object_name = selected_item.text()

            # Emit the signal to notify MainWindow of the selected object
            self.object_selected_signal.emit(selected_object_name)
