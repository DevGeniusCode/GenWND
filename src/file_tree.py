from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt

class FileTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a file system model
        self.model = QFileSystemModel()

        # Set root path (start with current directory)
        self.model.setRootPath(QDir.rootPath())

        # Filter files: only show .wnd files
        self.model.setNameFilters(["*.wnd"])
        self.model.setNameFilterDisables(False)

        # Set the model to the tree view
        self.setModel(self.model)

        # Add the root directory for browsing (initially set to the current directory)
        self.setRootIndex(self.model.index(QDir.currentPath()))

        # Allow expanding and collapsing of directories
        self.setExpandsOnDoubleClick(True)

        # Enable context menu (right-click)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        """Show context menu for file operations (e.g., add, delete)"""
        index = self.indexAt(pos)
        if not index.isValid():
            return

        menu = self.createStandardContextMenu()

        # Optionally, add more custom actions (e.g., Add File, Delete File)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_file(index))

        menu.exec(self.mapToGlobal(pos))

    def delete_file(self, index):
        """Delete the selected file or folder"""
        file_path = self.model.filePath(index)
        if QDir(file_path).removeRecursively():  # Removes directory and contents
            print(f"Deleted {file_path}")
        else:
            print(f"Failed to delete {file_path}")
