import sys
import os
import traceback

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QWidget, QMenuBar, QFileDialog,
    QPushButton, QToolBar, QSplitter, QLabel, QVBoxLayout, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QAction, QIcon, QUndoStack
from PyQt6.QtCore import Qt

from commands import CommandChangeGeometry
from object_tree import ObjectTree
from file_tree import FileTree
from property_editor import PropertyEditor
from src.environment_manager import EnvironmentManager
from src.setting import SettingsWidget
from src.window.wnd_parser import WndParser
from log_manager import LogManager
from visual_preview import VisualPreview


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GenWND")
        self.setWindowIcon(QIcon('resources/icons/GenWND.ico'))
        self.resize(1200, 800)

        # Environment & State
        self.default_directory = EnvironmentManager('resources/user_config.json').get(
            'default_directory') or os.path.expanduser("~/Documents")
        self.log_manager = LogManager()
        self.settings_widget = SettingsWidget()

        self.selected_file = None
        self.selected_object = None
        self.parser = None
        self.is_modified = False
        self.show_labels = True

        # Setup exception handling globally
        sys.excepthook = self.handle_exception

        # Initialize Undo Stack
        self.undo_stack = QUndoStack(self)

        # Enable Drag & Drop
        self.setAcceptDrops(True)

        # Build UI Components
        self._setup_menus()
        self._setup_toolbars()
        self._setup_ui_layout()
        self._connect_signals()

        # Load styles
        self.load_styles()

    def _setup_menus(self):
        """Initializes the top File and Edit menus."""
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # File Menu
        file_menu = menu_bar.addMenu("File")

        open_file_action = QAction("Open File", self)
        open_folder_action = QAction("Open Folder", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save As", self)
        add_file_action = QAction("Add File", self)
        add_folder_action = QAction("Add Folder", self)
        settings_action = QAction("Settings", self)

        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_as_file)
        add_file_action.triggered.connect(self.add_file_menu)
        add_folder_action.triggered.connect(self.add_folder_menu)
        settings_action.triggered.connect(self.open_settings)

        file_menu.addActions([open_file_action, open_folder_action, save_action, save_as_action])
        file_menu.addSeparator()
        file_menu.addActions([add_file_action, add_folder_action])
        file_menu.addSeparator()
        file_menu.addAction(settings_action)

        # Edit Menu (Undo/Redo)
        edit_menu = menu_bar.addMenu("Edit")
        self.undo_action = self.undo_stack.createUndoAction(self, "Undo")
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

        self.redo_action = self.undo_stack.createRedoAction(self, "Redo")
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        self.addAction(self.undo_action)
        self.addAction(self.redo_action)

    def _setup_toolbars(self):
        """Initializes the top toolbar containing panel toggle buttons."""
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.toggle_file_tree_button = QPushButton("Toggle Files", self)
        self.toggle_file_tree_button.clicked.connect(self.toggle_file_tree_visibility)
        self.toolbar.addWidget(self.toggle_file_tree_button)

        self.toggle_object_tree_button = QPushButton("Toggle Objects", self)
        self.toggle_object_tree_button.clicked.connect(self.toggle_object_tree_visibility)
        self.toolbar.addWidget(self.toggle_object_tree_button)

        self.toggle_property_editor_button = QPushButton("Toggle Properties", self)
        self.toggle_property_editor_button.clicked.connect(self.toggle_property_editor_visibility)
        self.toolbar.addWidget(self.toggle_property_editor_button)

        self.toolbar.addSeparator()

        self.export_screenshot_action = QAction(QIcon.fromTheme("camera-photo"), "Export Screenshot", self)
        self.export_screenshot_action.triggered.connect(self.export_canvas_screenshot)
        self.toolbar.addAction(self.export_screenshot_action)

    def _setup_ui_layout(self):
        """Creates and arranges the main layout splitters and panels."""
        # File Tree Panel
        self.file_tree = FileTree(self, main_window=self)
        self.file_tree.setMinimumWidth(250)
        self.file_tree.set_root_path(self.default_directory)

        self.root_path_label = QLabel()
        self.root_path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        file_tree_layout = QVBoxLayout()
        file_tree_layout.addWidget(self.file_tree)
        file_tree_layout.addWidget(self.root_path_label)

        file_tree_widget = QWidget()
        file_tree_widget.setLayout(file_tree_layout)

        # Object Tree Panel
        self.object_tree = ObjectTree(self, main_window=self)
        self.object_tree.tree_view.setHeaderHidden(True)
        self.object_tree.setMinimumWidth(300)

        # Property Editor Panel
        self.property_editor = PropertyEditor(self, main_window=self)

        # Ensure property editor hierarchy also receives the global shortcuts
        self.property_editor.addAction(self.undo_action)
        self.property_editor.addAction(self.redo_action)

        # Visual Preview (Canvas)
        self.visual_preview = VisualPreview(self)
        self.visual_preview.setMinimumWidth(300)

        # Main Splitter setup
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(file_tree_widget)  # Index 0
        splitter.addWidget(self.object_tree)  # Index 1
        splitter.addWidget(self.visual_preview)  # Index 2
        splitter.addWidget(self.property_editor)  # Index 3

        # Default widths in pixels
        splitter.setSizes([180, 180, 800, 350])

        # Stretch factors (1 = expand to fill space, 0 = keep compact)
        splitter.setStretchFactor(0, 0)  # File Tree (No stretch)
        splitter.setStretchFactor(1, 0)  # Object Tree (No stretch)
        splitter.setStretchFactor(2, 1)  # Visual Preview (Expands!)
        splitter.setStretchFactor(3, 0)  # Property Editor (No stretch)
        splitter.setHandleWidth(10)

        # Central Widget Layout
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_bar.setStyleSheet("QStatusBar { padding-left: 8px; }")  # <-- Added Padding
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

    def export_canvas_screenshot(self):
        """Export the current canvas scene as an image."""
        if hasattr(self, "visual_preview"):
            # Default uses canvas-colored background.
            # Change to True if you want transparent PNG by default.
            self.visual_preview.export_scene_image(transparent_background=False)

    def _connect_signals(self):
        """Centralized location for connecting component signals to main window slots."""
        # Panel Selection Signals
        self.file_tree.file_selected_signal.connect(self.select_file)
        self.file_tree.folder_selected_signal.connect(self.select_folder)
        self.object_tree.objects_selected_signal.connect(self.select_objects_from_tree)

        # Canvas <-> Data Sync Signals
        self.object_tree.visibility_changed_signal.connect(self.visual_preview.set_item_visibility)
        self.visual_preview.selection_changed_signal.connect(self.select_objects_from_canvas)
        self.visual_preview.item_moved_signal.connect(self.handle_canvas_item_moved)
        self.visual_preview.bulk_geometry_change_signal.connect(self.handle_bulk_geometry_change)

    # --- UI ACTIONS ---
    def toggle_file_tree_visibility(self):
        self.file_tree.setVisible(not self.file_tree.isVisible())

    def toggle_object_tree_visibility(self):
        self.object_tree.setVisible(not self.object_tree.isVisible())

    def toggle_property_editor_visibility(self):
        self.property_editor.setVisible(not self.property_editor.isVisible())

    def update_status_bar(self):
        """Updates the status bar with the active root path, file, and object info."""
        root_path = self.file_tree.model.rootPath()
        root_path_info = f"Root: {os.path.basename(root_path)}" if root_path else "Root: Not available"

        file_name = f"File: {os.path.basename(self.selected_file)}" if self.selected_file else "No file selected"

        object_name = "No object selected"
        if self.selected_object:
            try:
                obj_type = self.selected_object.properties.get('WINDOWTYPE', 'UNKNOWN')
                obj_name = self.selected_object.properties.get('NAME', 'Unnamed')
                object_name = f"Object: {obj_type} - {obj_name}"
            except AttributeError:
                object_name = f"{str(self.selected_object)}"

        self.status_bar.showMessage(f"{root_path_info} | {file_name} | {object_name}")

    def set_show_labels(self, show):
        """Global toggle for canvas object name labels."""
        self.show_labels = bool(show)
        if hasattr(self, "visual_preview"):
            self.visual_preview.set_show_labels(self.show_labels)

    def update_modified_state(self, modified):
        self.is_modified = modified
        self.object_tree.update_buttons_state()

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def load_styles(self):
        """Loads application stylesheet."""
        base_style = ""
        try:
            with open("resources/styles.qss", "r") as style_file:
                base_style = style_file.read()
        except FileNotFoundError:
            self.log_manager.log("styles.qss not found in resources directory", level="WARNING")

        # Inject shared Empty State styling programmatically
        empty_state_style = """
            QLabel#emptyStateLabel {
                background-color: #2b2b2b;
                color: #888888;
                font-size: 14px;
                font-style: italic;
            }
        """
        self.setStyleSheet(base_style + empty_state_style)

    def handle_exception(self, exc_type, exc_value, exc_tb):
        """Global handler for uncaught exceptions."""
        stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        self.log_manager.log_exception(exc_value)
        self.log_manager.log_exception(stack_trace)

    def open_settings(self):
        self.settings_widget.show()

    # --- SELECTION & SYNC LOGIC ---
    def select_objects_from_tree(self, window_objects):
        """Triggered when the user changes selection in the Object Tree."""
        if hasattr(self, 'visual_preview'):
            uuids = [obj.window_uuid for obj in window_objects]
            self.visual_preview.select_items(uuids)
        self._update_selection_state(window_objects)

    def select_objects_from_canvas(self, uuids):
        """Triggered when the user changes selection in the visual Canvas."""
        window_objects = []
        if self.parser:
            for uuid in uuids:
                obj = self.object_tree.model._find_window_by_uuid(self.parser.get_windows(), uuid)
                if obj:
                    window_objects.append(obj)

        self.object_tree.select_items_by_uuids(uuids)
        self._update_selection_state(window_objects)

    def _update_selection_state(self, window_objects):
        """Centralized handler to load properties and update the status bar."""
        if len(window_objects) == 1:
            self.selected_object = window_objects[0]
            self.update_status_bar()
            self.load_object_property()
            self.log_manager.log(f"Object selected: {self.selected_object.properties.get('NAME', 'Unnamed')}", level="INFO")
        elif len(window_objects) > 1:
            self.selected_object = None
            self.property_editor.clear()
            self.status_bar.showMessage(f"{len(window_objects)} objects selected. Properties disabled.")
        else:
            self.selected_object = None
            self.property_editor.clear()
            self.update_status_bar()

    def handle_canvas_item_moved(self, window, ul, br):
        """Triggered when an item is dynamically dragged/resized on the visual preview."""
        # 1. Update underlying dictionary data
        if 'SCREENRECT' not in window.properties:
            window.properties['SCREENRECT'] = {}
        window.properties['SCREENRECT']['UPPERLEFT'] = list(ul)
        window.properties['SCREENRECT']['BOTTOMRIGHT'] = list(br)

        # 2. Trigger save state
        self.update_modified_state(True)

        # 3. Synchronize active spinboxes in Property Editor without firing undo commands
        if self.selected_object and getattr(self.selected_object, 'window_uuid', None) == window.window_uuid:
            if hasattr(self.property_editor, 'general_properties'):
                gp = self.property_editor.general_properties
                w = max(0, br[0] - ul[0])
                h = max(0, br[1] - ul[1])
                for spinbox, val in [
                    (gp.upper_left_x_spinbox, ul[0]),
                    (gp.upper_left_y_spinbox, ul[1]),
                    (gp.bottom_right_x_spinbox, br[0]),
                    (gp.bottom_right_y_spinbox, br[1]),
                    (gp.width_spinbox, w),
                    (gp.height_spinbox, h)
                ]:
                    spinbox.blockSignals(True)
                    spinbox.setValue(val)
                    spinbox.blockSignals(False)

    def handle_object_added(self, window_object):
        """Routes object addition to the Tree and Canvas."""
        self.object_tree._refresh_tree_state()
        if hasattr(self, 'visual_preview'):
            # Fetch the data from the source of truth and pass it down
            root_windows = self.parser.get_windows()
            self.visual_preview.add_item_to_canvas(window_object, root_windows)

    def handle_object_deleted(self, window_uuid):
        """Routes object deletion to the Tree and Canvas, clearing properties if selected."""
        self.object_tree._refresh_tree_state()

        if hasattr(self, 'visual_preview'):
            self.visual_preview.remove_item_from_canvas(window_uuid)

        if self.selected_object and self.selected_object.window_uuid == window_uuid:
            self.selected_object = None
            self.property_editor.clear()
            self.update_status_bar()

    def handle_bulk_geometry_change(self, macro_name, changes):
        """Pushes a bulk geometry operation as a single Undo macro."""
        self.undo_stack.beginMacro(macro_name)
        for window_uuid, old_ul, old_br, new_ul, new_br in changes:
            cmd = CommandChangeGeometry(self, window_uuid, old_ul, old_br, new_ul, new_br)
            self.undo_stack.push(cmd)
        self.undo_stack.endMacro()

    # --- FILE & FOLDER OPERATIONS ---
    def select_file(self, file_path):
        """Handles selection of a file from the file tree, prompting for save if modified."""
        if self.is_modified:
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                "You have unsaved changes. Do you want to save before selecting a new file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                self._select_file(file_path)
            elif reply == QMessageBox.StandardButton.No:
                self._select_file(file_path)
        else:
            self._select_file(file_path)

    def _select_file(self, file_path):
        """Internal logic to actually load the file after checks."""
        self.object_tree.clear()
        self.visual_preview.clear()
        self.selected_file = file_path
        self.selected_object = None
        self.load_wnd_file(file_path)
        self.update_status_bar()
        self.log_manager.log(f"File selected: {file_path}", level="INFO")

    def select_folder(self, folder_path):
        """Handles folder selection and resets file and object selections."""
        self.selected_file = folder_path
        self.selected_object = None
        self.object_tree.clear()
        self.property_editor.clear()
        self.visual_preview.clear()
        self.update_status_bar()
        self.log_manager.log(f"Folder selected: {folder_path}", level="INFO")

    def open_file(self):
        """Prompts dialog to open a specific WND file."""
        if self.is_modified:
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                "You have unsaved changes. Do you want to save before opening a new file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                self._open_file()
            elif reply == QMessageBox.StandardButton.No:
                self._open_file()
        else:
            self._open_file()

    def _open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", self.default_directory,
                                              "WND Files (*.wnd);;All Files (*)")
        if file:
            self.log_manager.log(f"File selected: {file}", level="INFO")
            self.selected_file = file
            self.selected_object = None
            self.property_editor.clear()
            self.object_tree.clear()
            self.visual_preview.clear()
            self.update_status_bar()
            self.load_wnd_file(file)

            self.default_directory = os.path.dirname(file)
            EnvironmentManager('resources/user_config.json').set('default_directory', self.default_directory)

    def open_folder(self):
        """Prompts dialog to open a specific directory."""
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.default_directory)
        if folder:
            self.log_manager.log(f"Folder selected: {folder}", level="INFO")
            self.file_tree.set_root_path(folder)
            self.selected_file = folder
            self.selected_object = None
            self.property_editor.clear()
            self.object_tree.clear()
            self.update_status_bar()

            self.default_directory = folder
            EnvironmentManager('resources/user_config.json').set('default_directory', folder)

    def load_wnd_file(self, file_path):
        """Parses the WND file and populates the UI components."""
        try:
            self.selected_file = file_path
            self.selected_object = None
            self.property_editor.clear()

            self.parser = WndParser()
            self.parser.parse_file(file_path)
            windows = self.parser.get_windows()

            self.object_tree.load_objects(windows)
            self.visual_preview.load_hierarchy(windows)
            self.undo_stack.clear()

            self.log_manager.log(f"Loaded objects from file {file_path}", level="INFO")
            self.update_modified_state(False)

        except ValueError as e:
            error_msg = f"Error loading file: {e}"
            self.log_manager.log(error_msg, level="ERROR")
            self.object_tree.display_error(error_msg)
            self.selected_object = error_msg
            self.update_status_bar()
            self.visual_preview.clear()

    def load_object_property(self):
        """Loads properties of the currently selected object into the Property Editor."""
        if self.selected_object:
            try:
                self.property_editor.load_property(self.selected_object)
                self.log_manager.log(
                    f"Loaded properties from object {self.selected_object.properties.get('WINDOWTYPE')} - {self.selected_object.properties.get('NAME', 'Unnamed')}",
                    level="INFO")
            except ValueError as e:
                error_msg = f"Error loading object properties: {e}"
                self.log_manager.log(error_msg, level="ERROR")
                self.property_editor.display_error(error_msg)

    def save_file(self):
        """Saves current data to the selected file using the parser's representation."""
        if self.selected_file and self.parser:
            try:
                self.parser.enforce_file_names(os.path.basename(self.selected_file))

                with open(self.selected_file, 'w') as file:
                    file.write(str(self.parser))
                self.update_modified_state(False)
                self.log_manager.log(f"File saved: {self.selected_file}", level="INFO")
            except Exception as e:
                self.log_manager.log(f"Error saving file: {e}", level="ERROR")
                self.show_error_message("Save Error", f"An error occurred while saving: {e}")
        else:
            self.log_manager.log("No file selected to save", level="ERROR")
            self.show_error_message("Save Error", "No file selected to save.")

    def save_as_file(self):
        """Prompts for location and saves file under a new name."""
        if self.parser:
            file, _ = QFileDialog.getSaveFileName(self, "Save As", "", "WND Files (*.wnd);;All Files (*)")
            if file:
                try:
                    self.parser.enforce_file_names(os.path.basename(self.selected_file))
                    with open(file, 'w') as f:
                        f.write(str(self.parser))
                    self.selected_file = file
                    self.update_modified_state(False)
                    self.log_manager.log(f"File saved as: {file}", level="INFO")
                except Exception as e:
                    self.log_manager.log(f"Error saving file as: {e}", level="ERROR")
                    self.show_error_message("Save As Error", f"An error occurred while saving: {e}")
        else:
            self.log_manager.log("No data to save", level="ERROR")
            self.show_error_message("Save As Error", "No data to save.")

    def add_file_menu(self):
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_file_action_handler(current_path)

    def add_folder_menu(self):
        current_path = self.file_tree.model.rootPath()
        if current_path:
            self.file_tree.add_folder_action_handler(current_path)

    # --- DRAG AND DROP CAPABILITIES ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.endswith(".wnd"):
                self.log_manager.log(f"File dropped: {f}", level="INFO")
                self.load_wnd_file(f)
            else:
                self.log_manager.log(f"Invalid file type dropped: {f}", level="WARNING")

    def closeEvent(self, event):
        """Warns the user if they try to close with unsaved changes."""
        if self.is_modified:
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())