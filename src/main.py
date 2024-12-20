import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QTreeView, QTableView, QMenuBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from file_tree import FileTree

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WND Editor")
        self.resize(1200, 800)

        # Initialize layout
        self.layout = QHBoxLayout()

        # File tree (on the left)
        self.file_tree = FileTree(self)
        self.layout.addWidget(self.file_tree)

        # Set main widget
        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        # Top menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        open_file_action = QAction("Open File", self)
        open_folder_action = QAction("Open Folder", self)
        save_action = QAction("Save", self)
        file_menu.addActions([open_file_action, open_folder_action, save_action])

        # File tree & Connect actions
        self.file_tree = QTreeView()
        self.file_tree.setHeaderHidden(True)
        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)

        # Objects tree
        self.object_tree = QTreeView()
        self.object_tree.setHeaderHidden(True)

        # property editor
        self.property_editor = QTableView()

        # Division into layout structure
        layout = QHBoxLayout()
        layout.addWidget(self.file_tree, 2)
        layout.addWidget(self.object_tree, 3)
        layout.addWidget(self.property_editor, 3)

        # Setting the main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # load styles
        self.load_styles()

    def load_styles(self):
        with open("resources/styles.qss", "r") as style_file:
            self.setStyleSheet(style_file.read())

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
            self.file_tree.setRootPath(folder)
            print(f"Folder selected: {folder}")
            # Implement folder opening logic here (e.g., show contents)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
