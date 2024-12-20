import sys
from PyQt6.QtWidgets import QApplication, QTreeView, QMainWindow, QHBoxLayout, QWidget, QTableView, QMenuBar, \
    QFileDialog, QPushButton, QToolBar, QMessageBox, QSplitter
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize
import os

from file_tree import FileTree

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WND Editor")
        self.resize(1200, 800)

        # Top menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")

        # File menu actions
        open_file_action = QAction("Open File", self)
        open_folder_action = QAction("Open Folder", self)
        save_action = QAction("Save", self)
        add_file_action = QAction("Add File", self)
        add_folder_action = QAction("Add Folder", self)
        file_menu.addActions([open_file_action, open_folder_action, save_action, add_file_action, add_folder_action])

        # Connect menu actions
        add_file_action.triggered.connect(self.add_file_menu)
        add_folder_action.triggered.connect(self.add_folder_menu)
        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)

        # File Tree Toggle Button (vertical orientation when on the sides)
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        self.toggle_file_tree_button = QPushButton("Toggle Files", self)
        self.toggle_file_tree_button.clicked.connect(self.toggle_file_tree_visibility)
        toolbar.addWidget(self.toggle_file_tree_button)

        # File Tree
        self.file_tree = FileTree(self)
        self.file_tree.setMinimumWidth(250)

        # Objects tree
        self.object_tree = QTreeView()
        self.object_tree.setHeaderHidden(True)
        self.object_tree.setMinimumWidth(300)

        # property editor
        self.property_editor = QTableView()
        self.property_editor.setMinimumWidth(300)

        # Toggle Buttons for object tree and property editor
        self.toggle_object_tree_button = QPushButton("Toggle Objects", self)
        self.toggle_object_tree_button.clicked.connect(self.toggle_object_tree_visibility)
        toolbar.addWidget(self.toggle_object_tree_button)
        self.toggle_property_editor_button = QPushButton("Toggle Properties", self)
        self.toggle_property_editor_button.clicked.connect(self.toggle_property_editor_visibility)
        toolbar.addWidget(self.toggle_property_editor_button)

        # Splitter for resizable file tree
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.file_tree)
        splitter.addWidget(self.object_tree)
        splitter.addWidget(self.property_editor)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 2)
        splitter.setHandleWidth(10) # add spacing

        # Division into layout structure
        layout = QHBoxLayout()
        layout.addWidget(splitter)

        # layout.addWidget(self.file_tree, 1) # Make tree view flexible width
        # layout.addWidget(self.object_tree, 3)
        # layout.addWidget(self.property_editor, 3)
        # layout.setStretch(1, 2)

        # Setting the main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.file_tree.setVisible(True)
        self.object_tree.setVisible(True)
        self.property_editor.setVisible(True)

        # load styles
        self.load_styles()

    def add_file_menu(self):
        """Handles the 'Add File' action from the menu"""
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_file_action_handler(current_path)

    def add_folder_menu(self):
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_folder_action_handler(current_path)

    def load_styles(self):
        """Loads the stylesheet from the resources directory"""
        try:
            with open("resources/styles.qss", "r") as style_file:
                self.setStyleSheet(style_file.read())
        except FileNotFoundError:
            print("Error: styles.qss not found in resources directory")

    def toggle_file_tree_visibility(self):
         """Toggles the visibility of the file tree panel"""
         self.file_tree.setVisible(not self.file_tree.isVisible())

    def toggle_object_tree_visibility(self):
         """Toggles the visibility of the object tree panel"""
         self.object_tree.setVisible(not self.object_tree.isVisible())

    def toggle_property_editor_visibility(self):
          """Toggles the visibility of the property editor panel"""
          self.property_editor.setVisible(not self.property_editor.isVisible())

    def open_file(self):
        """Handle opening a file"""
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "WND Files (*.wnd);;All Files (*)")
        if file:
            print(f"File selected: {file}")
            # Implement file opening logic here (e.g., read content)

    def open_folder(self):
        """Handle opening a folder"""
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            self.file_tree.set_root_path(folder)
            print(f"Folder selected: {folder}")
            # Implement folder opening logic here (e.g., show contents)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())