import os
from PyQt6.QtWidgets import QTreeView, QMenu, QMessageBox, QInputDialog
from PyQt6.QtCore import QDir, QModelIndex
from PyQt6.QtGui import QFileSystemModel, QDrag
from PyQt6.QtCore import Qt, QMimeData, QByteArray
import shutil

class FileTree(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a file system model
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)

        # Filter files: show only .wnd files
        self.model.setNameFilters(["*.wnd"])
        self.model.setNameFilterDisables(False)

        # Filter all files and directories, excluding hidden ones (starting with dot) and .., .
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        # Set the model to the tree view
        self.setModel(self.model)

        # Add the root directory for browsing (initially set to the current directory)
        self.set_root_path(QDir.currentPath())

        # Allow expanding and collapsing of directories
        self.setExpandsOnDoubleClick(True)

        # Enable context menu (right-click)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # Hide headers to only display the directory structure (without file details)
        self.setHeaderHidden(True)
        # self.setColumnWidth(0, 250)  # Limit the width of the file column

        # Limit the width of the file column
        self.setColumnWidth(0, 250)

        # Remove all columns except the first one (name)
        for column in range(1, self.model.columnCount()):
            self.hideColumn(column)

        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.doubleClicked.connect(self.handle_double_click) # Handle double click event

        # Create a validator for file names to block special charcters
        #self.name_validator = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9_.-]+"))


    def set_root_path(self, path):
        """Set the root path for the tree view, filter out '.' and '..' directories"""
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

        # Update the model filter to explicitly hide '.' and '..' directories
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

    def show_context_menu(self, pos):
        """Show context menu for file operations (e.g., add, delete)"""

        index = self.indexAt(pos)
        if index.isValid():
            file_path = self.model.filePath(index)
            is_dir = os.path.isdir(file_path)

            menu = QMenu(self)

            # Add file action
            add_file_action = menu.addAction("Add File")
            add_file_action.triggered.connect(lambda: self.add_file(index))

            # Add folder action
            add_folder_action = menu.addAction("Add Folder")
            add_folder_action.triggered.connect(lambda: self.add_folder(index))

            # Delete action
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_file(index))

            menu.exec(self.mapToGlobal(pos))
        else:
            # handle click on blank space on the treeview
            menu = QMenu(self)
            # add file action
            add_file_action = menu.addAction("Add File")
            add_file_action.triggered.connect(lambda: self.add_file_action_handler())

            # add folder action
            add_folder_action = menu.addAction("Add Folder")
            add_folder_action.triggered.connect(lambda: self.add_folder_action_handler())
            menu.exec(self.mapToGlobal(pos))

    def add_file_action_handler(self,current_path = None):
        """Add file action handler"""
        if current_path:
            self.add_file(self.model.index(current_path))
        else:
             root_index = self.rootIndex()
             self.add_file(root_index)

    def add_folder_action_handler(self, current_path = None):
         """Add folder action handler"""
         if current_path:
             self.add_folder(self.model.index(current_path))
         else:
             root_index = self.rootIndex()
             self.add_folder(root_index)

    def add_file(self, index: QModelIndex):
        """Add a new file to the selected directory or file's directory"""
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            dir_path = os.path.dirname(file_path)
        else:
            dir_path = file_path

        new_file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and new_file_name:
            if not new_file_name.endswith(".wnd"):
                new_file_name += ".wnd"
            new_file_path = os.path.join(dir_path, new_file_name)
            if os.path.exists(new_file_path):
                QMessageBox.warning(self, "Error", "File with this name already exists!")
                return
            try:
                with open(new_file_path, 'w') as _:  # Create empty file
                    pass
                # After creating the file, refresh the model
                self.model.layoutChanged.emit()
                print(f"Created file {new_file_path}")
            except Exception as e:
                print(f"Error creating file {new_file_path}: {e}")

    def add_folder(self, index: QModelIndex):
        """Add a new folder to the selected directory or file's directory"""
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            dir_path = os.path.dirname(file_path)
        else:
            dir_path = file_path

        new_folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and new_folder_name:
            new_folder_path = os.path.join(dir_path, new_folder_name)
            if os.path.exists(new_folder_path):
                QMessageBox.warning(self, "Error", "Folder with this name already exists!")
                return
            try:
                os.makedirs(new_folder_path)
                #self.model.dataChanged(index,index)
                self.model.refresh(index.parent())
                print(f"Created folder {new_folder_path}")
            except Exception as e:
                print(f"Error creating folder {new_folder_path}: {e}")


    def delete_file(self, index: QModelIndex):
        """Delete the selected file or folder after confirmation"""
        file_path = self.model.filePath(index)

        message = f"Are you sure you want to delete:\n{file_path}"
        reply = QMessageBox.question(self, "Confirmation", message,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # If it's a file, delete it
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                # If it's a directory, delete it and all its contents
                elif os.path.isdir(file_path):
                    dir_to_delete = QDir(file_path)
                    if dir_to_delete.removeRecursively():
                        print(f"Deleted directory: {file_path}")
                    else:
                        print(f"Failed to delete directory: {file_path}")
                # Refresh the model layout
                self.model.layoutChanged.emit()
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    def startDrag(self, supportedActions: Qt.DropAction):
       """Start drag operation"""
       index = self.currentIndex()
       if not index.isValid():
           return

       file_path = self.model.filePath(index)
       if os.path.isdir(file_path):
            return # do not allow dragging folder

       mime_data = QMimeData()
       mime_data.setText(file_path)

       drag = QDrag(self)
       drag.setMimeData(mime_data)
       drag.exec(supportedActions)

    def dragEnterEvent(self, event):
        """Handles drag enter event"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
       """Handles drag move event"""
       event.acceptProposedAction()


    def dropEvent(self, event):
        """Handles drop event"""
        if not event.mimeData().hasText():
            return

        source_file_path = event.mimeData().text()
        target_index = self.indexAt(event.position().toPoint())

        if not target_index.isValid(): # drop on blank space
            target_dir = self.model.rootPath()
        else:
           target_file_path = self.model.filePath(target_index)
           if os.path.isfile(target_file_path): # if dropped on a file
               target_dir = os.path.dirname(target_file_path)
           else:
               target_dir = target_file_path



        # Prevent dropping a folder on itself
        if os.path.isdir(source_file_path) :
            QMessageBox.warning(self, "Error", "Cannot move a folder.")
            return

        if os.path.abspath(source_file_path) == os.path.abspath(target_dir):
             return

        if os.path.abspath(source_file_path).startswith(os.path.abspath(target_dir)): #prevent folder to be droped into its self
           return


        try:
            # Check if a file with the same name already exists in the target directory
            target_file_name = os.path.basename(source_file_path)
            new_file_path = os.path.join(target_dir, target_file_name)
            if os.path.exists(new_file_path):
                dialog = QInputDialog(self)
                dialog.setWindowTitle("Name Conflict")
                dialog.setLabelText("Enter new file name:")
                line_edit = dialog.findChild(QLineEdit)
                while True:
                     ok = dialog.exec()
                     if not ok:
                        return # user canceled
                     new_file_name = dialog.textValue()
                     if not new_file_name:
                         line_edit.setStyleSheet("border: 1px solid red;")
                         line_edit.setPlaceholderText("File name cannot be empty!")
                         continue  # retry
                     line_edit.setStyleSheet("")
                     line_edit.setPlaceholderText("")
                     new_file_path = os.path.join(target_dir, new_file_name)
                     if os.path.exists(new_file_path):
                         line_edit.setStyleSheet("border: 1px solid red;")
                         line_edit.setPlaceholderText("File with this name already exists!")
                         continue
                     break
            shutil.move(source_file_path, new_file_path)
            self.model.layoutChanged.emit()  # Refresh view
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to move file: {e}")

    def handle_double_click(self,index):
       """Block the option to edit the file name from the treeview"""
       if index.isValid() and not self.model.isDir(index):
            return
       self.edit(index)