from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class ObjectTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

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
