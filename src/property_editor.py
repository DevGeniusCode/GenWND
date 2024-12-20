from PyQt6.QtWidgets import QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class PropertyEditor(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Property", "Value"])

    def load_properties(self, properties):
        """
        Load properties into the table view.
        :param properties: Dictionary of object properties.
        """
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Property", "Value"])
        for key, value in properties.items():
            key_item = QStandardItem(key)
            value_item = QStandardItem(str(value))
            self.model.appendRow([key_item, value_item])
