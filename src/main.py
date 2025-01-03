import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QMenuBar, \
    QFileDialog, QPushButton, QToolBar, QSplitter, QLabel, QVBoxLayout, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import os
import traceback

from object_tree import ObjectTree
from file_tree import FileTree
from property_editor import PropertyEditor
from src.environment_manager import EnvironmentManager
from src.setting import SettingsWidget
from src.window.wnd_parser import WndParser
from log_manager import LogManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GenWND")
        self.setWindowIcon(QIcon('resources/icons/GenWND.ico'))
        self.resize(1200, 800)
        self.default_directory = EnvironmentManager('resources/user_config.json').get('default_directory') or os.path.expanduser("~/Documents")

        # Initialize logging
        self.log_manager = LogManager()

        # Setup exception handling
        sys.excepthook = self.handle_exception

        # Top menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")

        # File menu actions
        open_file_action = QAction("Open File", self)
        open_folder_action = QAction("Open Folder", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save As", self)
        add_file_action = QAction("Add File", self)
        add_folder_action = QAction("Add Folder", self)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addActions([open_file_action, open_folder_action, save_action, add_file_action, add_folder_action])
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(settings_action)

        # Create a stacked widget to hold different widgets
        self.settings_widget = SettingsWidget()
        self.is_modified = False

        # Connect menu actions
        add_file_action.triggered.connect(self.add_file_menu)
        add_folder_action.triggered.connect(self.add_folder_menu)
        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_as_file)

        # File Tree Toggle Button
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        self.toggle_file_tree_button = QPushButton("Toggle Files", self)
        self.toggle_file_tree_button.clicked.connect(self.toggle_file_tree_visibility)
        toolbar.addWidget(self.toggle_file_tree_button)

        # File Tree
        self.file_tree = FileTree(self, main_window=self)  # Pass the reference of MainWindow here
        self.file_tree.setMinimumWidth(250)
        self.file_tree.set_root_path(self.default_directory)

        # Label for displaying root path at the bottom of the file tree
        self.root_path_label = QLabel()
        self.root_path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Connect the file selected signal to the update function
        self.file_tree.file_selected_signal.connect(self.select_file)
        self.file_tree.folder_selected_signal.connect(self.select_folder)

        # Layout for file tree and path label
        file_tree_layout = QVBoxLayout()
        file_tree_layout.addWidget(self.file_tree)
        file_tree_layout.addWidget(self.root_path_label)
        file_tree_widget = QWidget()
        file_tree_widget.setLayout(file_tree_layout)

        # Objects Tree (where wnd file will be choice)
        self.object_tree = ObjectTree(self, main_window=self)
        self.object_tree.tree_view.setHeaderHidden(True)
        self.object_tree.setMinimumWidth(300)

        # Connect the object selected signal to the update function
        self.object_tree.object_selected_signal.connect(self.select_object)

        # Property Editor (for object details)
        self.property_editor = PropertyEditor(self, main_window=self)
        # self.property_editor.setFixedWidth(330)

        # Toggle Buttons for object tree and property editor
        self.toggle_object_tree_button = QPushButton("Toggle Objects", self)
        self.toggle_object_tree_button.clicked.connect(self.toggle_object_tree_visibility)
        toolbar.addWidget(self.toggle_object_tree_button)
        self.toggle_property_editor_button = QPushButton("Toggle Properties", self)
        self.toggle_property_editor_button.clicked.connect(self.toggle_property_editor_visibility)
        toolbar.addWidget(self.toggle_property_editor_button)

        # Splitter for resizable file tree
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(file_tree_widget)
        splitter.addWidget(self.object_tree)
        splitter.addWidget(self.property_editor)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 2)
        splitter.setHandleWidth(10)  # add spacing

        # Division into layout structure
        layout = QHBoxLayout()
        layout.addWidget(splitter)

        # Setting the main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add status bar at the bottom
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.selected_file = None
        self.selected_object = None
        self.parser = None

        self.update_status_bar()

        # Load styles
        self.load_styles()

        # Enable drag and drop
        self.setAcceptDrops(True)
    def select_object(self, window_object):
        """Handles selection of an object from the object tree"""
        self.selected_object = window_object
        self.update_status_bar()
        self.load_object_property()
        # Log the selected object
        if self.selected_object:
            self.log_manager.log(f"Object selected: {window_object.properties.get('WINDOWTYPE')} - {window_object.properties.get('NAME', 'Unnamed')}", level="INFO")

    def select_file(self, file_path):
        """Handles selection of a file from the file tree."""
        if self.is_modified:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Do you want to save before selecting a new file?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                self._select_file(file_path)
            elif reply == QMessageBox.StandardButton.No:
                self._select_file(file_path)
            else:
                return
        else:
            self._select_file(file_path)

    def _select_file(self, file_path):
        """Handles selection of a file from the file tree"""
        self.object_tree.clear()
        self.selected_file = file_path
        self.selected_object = None  # disable to display error in status bar
        self.load_wnd_file(file_path)
        self.update_status_bar()

        # Log the selected file
        self.log_manager.log(f"File selected: {file_path}", level="INFO")

    def select_folder(self, folder_path):
        """Handles folder selection and resets file and object selections."""
        self.selected_file = folder_path
        self.selected_object = None
        self.object_tree.clear()
        self.property_editor.clear()

        self.update_status_bar()  # Update the status bar to reflect that only folder is selected
        self.log_manager.log(f"Folder selected: {folder_path}", level="INFO")

    def save_file(self):
        """Saves the current WND file to the selected file path."""
        if self.selected_file and self.parser:
            try:
                # Save the current WND data to the selected file
                with open(self.selected_file, 'w') as file:
                    file.write(str(self.parser))  # Using __repr__ method of WndParser to get the file content
                self.update_modified_state(False)
                self.log_manager.log(f"File saved: {self.selected_file}", level="INFO")
            except Exception as e:
                self.log_manager.log(f"Error saving file: {e}", level="ERROR")
                self.show_error_message("Save Error", f"An error occurred while saving the file: {e}")
        else:
            self.log_manager.log("No file selected to save", level="ERROR")
            self.show_error_message("Save Error", "No file selected to save.")

    def save_as_file(self):
        """Prompts the user to choose a location and save the WND file under a new name."""
        if self.parser:
            file, _ = QFileDialog.getSaveFileName(self, "Save As", "", "WND Files (*.wnd);;All Files (*)")
            if file:
                try:
                    # Save the WND data to the chosen file path
                    with open(file, 'w') as f:
                        f.write(str(self.parser))  # Using __repr__ method of WndParser to get the file content
                    self.selected_file = file
                    self.update_modified_state(False)
                    self.log_manager.log(f"File saved as: {file}", level="INFO")
                except Exception as e:
                    self.log_manager.log(f"Error saving file as: {e}", level="ERROR")
                    self.show_error_message("Save As Error", f"An error occurred while saving the file as: {e}")
        else:
            self.log_manager.log("No data to save", level="ERROR")
            self.show_error_message("Save As Error", "No data to save.")

    def show_error_message(self, title, message):
        """Displays an error message dialog to the user."""
        QMessageBox.critical(self, title, message)

    def update_status_bar(self):
        """Update the status bar with relevant information."""
        root_path = self.file_tree.model.rootPath()
        file_name = "No file selected"
        object_name = "No object selected"

        if root_path:
            root_path_info = f"Root: {os.path.basename(root_path)}"
        else:
            root_path_info = "Root: Not available"

        # Update the file name and object name if they are selected
        if hasattr(self, 'selected_file') and self.selected_file:
            file_name = f"File: {os.path.basename(self.selected_file)}"
        # elif not self.selected_file:
        #     file_name = f"Folder: {os.path.basename(self.selected_file)}"

        if hasattr(self, 'selected_object') and self.selected_object:
            # Show the name of the selected object in the status bar
            try:
                object_name = f"Object: {self.selected_object.properties.get('WINDOWTYPE')} - {self.selected_object.properties.get('NAME', 'Unnamed')}"
            except AttributeError:
                object_name = f"{str(self.selected_object)}"
        # Combine all information
        status_text = f"{root_path_info} | {file_name} | {object_name}"

        self.status_bar.showMessage(status_text)

    def add_file_menu(self):
        """Handles the 'Add File' action from the menu"""
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_file_action_handler(current_path)

    def add_folder_menu(self):
        """Handles the 'Add Folder' action from the menu"""
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_folder_action_handler(current_path)

    def load_styles(self):
        """Loads the stylesheet from the resources directory"""
        try:
            with open("resources/styles.qss", "r") as style_file:
                self.setStyleSheet(style_file.read())
        except FileNotFoundError:
            self.log_manager.log(f"styles.qss not found in resources directory", level="WARNING")

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
        """Handle opening a file."""
        if self.is_modified:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Do you want to save before opening a new file?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                self._open_file()
            elif reply == QMessageBox.StandardButton.No:
                self._open_file()
            else:
                return
        else:
            self._open_file()


    def _open_file(self):
        """Handle opening a file"""
        file, _ = QFileDialog.getOpenFileName(self, "Open File",  self.default_directory, "WND Files (*.wnd);;All Files (*)")
        if file:
            self.log_manager.log(f"Logged info: File selected: {file}", level="INFO")
            self.current_file = file
            self.selected_object = None
            self.property_editor.clear()
            self.object_tree.clear()
            self.update_status_bar()
            self.load_wnd_file(file)
            self.default_directory = os.path.dirname(file)
            EnvironmentManager('resources/user_config.json').set('default_directory', self.default_directory)

    def load_wnd_file(self, file_path):
        """Loads and parses the WND file, and displays the object tree."""
        try:
            self.selected_file = file_path  # Store the selected file path
            self.selected_object = None  # Reset object selection
            self.property_editor.clear()
            self.parser = WndParser()
            self.parser.parse_file(file_path)  # Parse the WND file
            windows = self.parser.get_windows()  # Retrieve the list of windows (objects)

            # Load the windows into the object tree
            self.object_tree.load_objects(windows)

            self.log_manager.log(f"Loaded objects from file {file_path}", level="INFO")
            self.update_modified_state(False)

        except ValueError as e:
            error_message = f"Error loading file: {e}"
            self.log_manager.log(error_message, level="ERROR")
            self.object_tree.display_error(error_message)
            self.selected_object = error_message
            self.update_status_bar()


    def load_object_property(self):
        """Loads and parses the WND file, and displays the object tree."""
        if self.selected_object:
            try:
                # Load the windows into the object tree
                self.property_editor.load_property(self.selected_object)
                self.log_manager.log(f"Loaded properties from object {self.selected_object.properties.get('WINDOWTYPE')} - {self.selected_object.properties.get('NAME', 'Unnamed')}", level="INFO")

            except ValueError as e:
                error_message = f"Error loading object: {e}"
                self.log_manager.log(error_message, level="ERROR")
                self.property_editor.display_error(error_message)

    def open_folder(self):
        """Handle opening a folder"""
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.default_directory)
        if folder:
            self.log_manager.log(f"Logged info: Folder selected: {folder}", level="INFO")
            self.file_tree.set_root_path(folder)
            self.selected_file = folder
            self.selected_object = None
            self.property_editor.clear()
            self.object_tree.clear()
            self.update_status_bar()
            self.default_directory = folder
            EnvironmentManager('resources/user_config.json').set('default_directory', folder)

    def handle_exception(self, exc_type, exc_value, exc_tb):
        """Handle uncaught exceptions globally"""
        exception_message = f"Uncaught Exception: {exc_value}"
        stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))

        # Log the exception using the log manager
        self.log_manager.log_exception(exc_value)
        self.log_manager.log_exception(stack_trace)

    def dragEnterEvent(self, event):
        """Handles the drag enter event. Checks if the dragged content is a valid file."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handles the drop event and processes the dropped files."""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.endswith(".wnd"):
                self.log_manager.log(f"File dropped: {f}", level="INFO")
                self.load_wnd_file(f)
            else:
                self.log_manager.log(f"Invalid file type dropped: {f}", level="WARNING")
    def open_settings(self):
        """Open the settings widget in the center"""
        self.settings_widget.show()

    def closeEvent(self, event):
        """Handle the close event and warn if the file has been modified."""
        if self.is_modified:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Do you want to save before closing?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def update_modified_state(self, modified):
        self.is_modified = modified
        self.object_tree.update_buttons_state()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())