from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class ObjectTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

    def load_objects(self, object_data):
        """
        Load objects into the tree view.
        :param object_data: Hierarchical data of objects.
        """
        self.model.clear()
        self._populate_tree(object_data, self.model)

    def _populate_tree(self, objects, parent_item):
        for obj in objects:
            item = QStandardItem(obj['type'])
            parent_item.appendRow(item)
            if 'children' in obj:
                self._populate_tree(obj['children'], item)
