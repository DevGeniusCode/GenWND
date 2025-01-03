import os
import uuid

from PyQt6.QtWidgets import QTreeView, QLabel, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QWidget, QMenu
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray, QDataStream, QIODevice

from src.window.window_properties import ObjectFactory


class ObjectTreeModel(QStandardItemModel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.parser_windows = []  # Store the original windows data

    def set_parser_windows(self, windows):
        self.parser_windows = windows

    def mimeTypes(self):
        return ['application/x-window-object']

    def mimeData(self, indexes):
        if not indexes:
            return None
        item = self.itemFromIndex(indexes[0])
        selected_window = item.data()
        message = f"startDrag - selected item: {selected_window.properties.get('NAME')}"
        self.main_window.log_manager.log(message)

        mime_data = QMimeData()
        data = QByteArray()
        stream = QDataStream(data, QDataStream.OpenModeFlag.WriteOnly)
        encoded_uuid = selected_window.window_uuid.encode('utf-8')
        stream.writeBytes(encoded_uuid)
        mime_data.setData('application/x-window-object', data)
        return mime_data

    def flags(self, index):
        default_flags = super().flags(index)
        if index.isValid():
            return default_flags | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled
        else:
            return default_flags | Qt.ItemFlag.ItemIsDropEnabled

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('application/x-window-object'):
            return False
        stream = QDataStream(data.data('application/x-window-object'), QIODevice.OpenModeFlag.ReadOnly)
        source_window_uuid_bytes = stream.readBytes()
        source_window_uuid = source_window_uuid_bytes.decode('utf-8')

        # Get drop target
        if parent and parent.isValid():
            drop_item = self.itemFromIndex(parent)
            drop_window = drop_item.data()
            if not drop_window:
                self.main_window.log_manager.log(f"dropEvent - no drop window, cannot reorder", level="WARNING")
                drop_window = None  # to be root
                self.main_window.log_manager.log(f"dropEvent - adding to root as fallback")

            # Check if the drop window are parent (USER)
            if drop_window and drop_window.properties.get('WINDOWTYPE') != 'USER':
                self.main_window.log_manager.log(f"dropEvent - drop window not user, adding as sibling", level="INFO")
                source_parent = self._find_window_parent(self.parser_windows, drop_window.window_uuid)
                if source_parent:
                    drop_window = source_parent
                else:
                    drop_window = None  # to be root
        else:
            drop_window = None  # root

        if drop_window:
            self.main_window.log_manager.log(f"dropEvent - source window: {drop_window.properties.get('NAME')}")
        else:
            self.main_window.log_manager.log(f"dropEvent - adding to root")

        self.reorder_windows(source_window_uuid, drop_window, row)

        self.main_window.update_modified_state(True)
        self.main_window.object_tree.update_buttons_state()
        self.clear()
        self.main_window.object_tree._populate_tree(self.parser_windows, self)
        return True

    def reorder_windows(self, source_window_uuid, drop_window, drop_row):
        """Reorder the windows data based on drag and drop"""
        source_window = self._find_window_by_uuid(self.parser_windows, source_window_uuid)
        if not source_window:
            self.main_window.log_manager.log(f"reorder_windows - no source window of uuid {source_window_uuid}",
                                             level="WARNING")
            return

        # Remove the window from its parent
        source_parent_children = self._find_window_parent_children(self.parser_windows, source_window_uuid)
        if source_parent_children:
            source_parent_children.remove(source_window)
            self.main_window.log_manager.log(f"reorder_windows - removed from parent")
            # Reset the list if its empty
            if not source_parent_children:
                source_parent = self._find_window_parent(self.parser_windows, source_window_uuid)
                if source_parent:
                    source_parent.pop('children', None)
        # Add to the new parent
        if drop_window:
            if not hasattr(drop_window, 'children'):
                drop_window.children = []
            # Insert to specific index
            drop_window.children.insert(drop_row, source_window)
            self.main_window.log_manager.log(
                f"reorder_windows - added to new parent: {drop_window.properties.get('NAME')}, index: {drop_row}")

        else:  # Adding to the root
            self.parser_windows.insert(drop_row, source_window)
            self.main_window.log_manager.log(f"reorder_windows - added to root at index {drop_row}")

        self.main_window.log_manager.log(f"reorder_windows - reordered")

    def _find_window_by_uuid(self, windows, window_uuid):
        """Recursive function to find a window by uuid"""
        for window in windows:
            if window.window_uuid == window_uuid:
                return window
        for window in windows:
            if hasattr(window, 'children'):
                found_window = self._find_window_by_uuid(window.children, window_uuid)
                if found_window:
                    return found_window
        return None

    def _find_window_parent_children(self, windows, window_uuid):
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if child.window_uuid == window_uuid:
                        self.main_window.log_manager.log(
                            f"parent found: {window.properties.get('NAME')}, uuid: {window.window_uuid}")
                        return window.children
        for window in windows:
            if hasattr(window, 'children'):
                found_children = self._find_window_parent_children(window.children, window_uuid)
                if found_children:
                    return found_children
        return None

    def _find_window_parent(self, windows, window_uuid):
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if child.window_uuid == window_uuid:
                        self.main_window.log_manager.log(f"parent found: {window.properties.get('NAME')},"
                                                         f" uuid: {window.window_uuid}")
                        return window
        for window in windows:
            if hasattr(window, 'children'):
                found_parent = self._find_window_parent(window.children, window_uuid)
                if found_parent:
                    return found_parent
        return None

    def is_ancestor(self, potential_ancestor, potential_descendant):
        """
        Check if potential_descendant is a descendant of potential_ancestor
        or they are the same object
        """
        if potential_ancestor == potential_descendant:
            return True

        def _recursive_check(parent, descendant):
            if hasattr(parent, 'children'):
                for child in parent.children:
                    if child == descendant:
                        return True
                    if _recursive_check(child, descendant):
                        return True
            return False

        return _recursive_check(potential_ancestor, potential_descendant)

    def is_valid_drop(self, event):
        drop_index = self.main_window.object_tree.tree_view.indexAt(event.position().toPoint())
        drop_item = self.itemFromIndex(drop_index)

        if drop_item:
            drop_window = drop_item.data()
            if drop_window:
                data = event.mimeData().data('application/x-window-object')
                stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
                source_window_uuid_bytes = stream.readBytes()
                source_window_uuid = source_window_uuid_bytes.decode('utf-8')
                source_window = self._find_window_by_uuid(self.parser_windows, source_window_uuid)
                if source_window and source_window.properties.get('WINDOWTYPE') == 'USER':
                    if self.is_ancestor(source_window, drop_window) or self.is_ancestor(drop_window, source_window):
                        return False
        return True


class ObjectTree(QWidget):
    # Signal to notify when an object is selected
    object_selected_signal = pyqtSignal(object)

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.model = ObjectTreeModel(main_window)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        # Create the tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # Enable drag and drop
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setDragDropMode(QTreeView.DragDropMode.InternalMove)

        # Set up signal for item selection
        self.tree_view.selectionModel().selectionChanged.connect(self.on_item_selected)
        self.tree_view.setVisible(False)

        # Create a label to display when there's no content or error
        self.empty_label = QLabel("Select a file to display its Windows.", self)
        self.empty_label.setObjectName("emptyLabel")
        self.empty_label.setWordWrap(True)
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create buttons for saving and resetting
        self.save_button = QPushButton("Save to file")
        self.reset_button = QPushButton("Reset from file")
        self.save_button.setVisible(False)  # Disable until a file is selected
        self.reset_button.setVisible(False)

        # Create the button layout at the bottom
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)

        # Create the tree layout
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree_view)
        self.tree_layout.addLayout(self.button_layout)

        # Create the main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.tree_layout)
        self.layout.setStretch(0, 1)

        # Connect buttons to their functions
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.update_buttons_state()
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

    def load_objects(self, windows):
        """Load the windows into the tree view."""
        if not windows:
            raise ValueError("Empty or invalid file")

        # Hide the empty label and show the buttons if there are file windows
        self.empty_label.setVisible(False)
        self.save_button.setVisible(True)
        self.reset_button.setVisible(True)
        self.tree_view.setVisible(True)
        self.model.set_parser_windows(windows)
        self.model.clear()
        self._populate_tree(windows, self.model)

    def _populate_tree(self, windows, parent_item):
        """
        Recursively populate the tree with windows and their children.
        :param windows: List of Window objects
        :param parent_item: Parent item in the tree to append items
        """
        for window in windows:
            item = QStandardItem(f"{window.properties.get('WINDOWTYPE')} - {window.properties.get('NAME', 'Unnamed')}")
            item.setData(window)
            parent_item.appendRow(item)
            if hasattr(window, 'children'):
                self._populate_tree(window.children, item)
        self.tree_view.expandAll()

    def on_item_selected(self, selected, deselected):
        """
        Handle item selection changes in the object tree.
        """
        selected_indexes = self.tree_view.selectedIndexes()
        if selected_indexes:
            # Get the selected item
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            selected_object = selected_item.data()
            self.object_selected_signal.emit(selected_object)

    def display_error(self, error_message):
        """
        Display an error message in the object tree.
        :param error_message: The error message to display.
        """
        # Clear the model to ensure no old data is left
        self.model.clear()
        self.empty_label.setVisible(False)
        self.tree_view.setVisible(True)

        # Create an error item to show in the tree
        error_item = QStandardItem("Error")
        error_item.setForeground(QColor("red"))
        error_item.setEditable(False)

        # Add the error message as a child item
        error_message_item = QStandardItem(error_message)
        error_message_item.setEditable(False)
        error_item.appendRow(error_message_item)

        # Add the error item as the root item of the model
        self.model.appendRow(error_item)

        # Optionally expand the error item so it's visible
        self.tree_view.expandAll()

    def clear(self):
        self.model.clear()
        self.empty_label.setVisible(True)
        self.save_button.setVisible(False)
        self.reset_button.setVisible(False)
        self.tree_view.setVisible(False)

    def on_save_button_clicked(self):
        """
        Handle save button click event. Calls the save_file function from the main window.
        """
        self.main_window.save_file()

    def on_reset_button_clicked(self):
        """
        Handle reset button click event. Calls the load_wnd_file function from the main window.
        """
        selected_file = self.main_window.selected_file
        self.main_window.load_wnd_file(selected_file)

    def update_buttons_state(self):
        """
        Update the state of the save and reset buttons based on the is_modified flag.
        """
        is_modified = getattr(self.main_window, "is_modified", False)
        if is_modified:
            self.save_button.setEnabled(True)
            self.reset_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
            self.reset_button.setEnabled(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object'):
            if self.model.is_valid_drop(event):
                event.acceptProposedAction()
            else:
                event.ignore()
                self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        else:
            event.ignore()
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object'):
            if self.model.is_valid_drop(event):
                event.acceptProposedAction()
            else:
                event.ignore()
                self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        else:
            event.ignore()
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().dragMoveEvent(event)

    def dragLeaveEvent(self, event):
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # Reset the cursor on drop
        super().dropEvent(event)  # trigger model drop event

    def show_context_menu(self, position):
        """
        Create and show the context menu.
        :param position: The position where the user clicked.
        """

        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        add_action = menu.addMenu("Add New")  # new menu for adding

        factory = ObjectFactory()
        for object_type in factory.control_classes:
            add_action.addAction(object_type)

        selected_index = self.tree_view.indexAt(position)  # Get the selected index of the item
        selected_item = self.model.itemFromIndex(selected_index) if selected_index.isValid() else None
        action = menu.exec(self.tree_view.viewport().mapToGlobal(position))  # Show the context menu

        if action == delete_action:
            if selected_item:
                self.delete_selected_item(selected_item)
        elif action and action.parent() == add_action:
            new_object_type = action.text()
            if selected_item:
                self.add_new_control(selected_item, new_object_type)
            else:
                self.add_new_control(None, new_object_type)

    def add_new_control(self, parent_item, new_object_type):
        """Add a new control to the tree at the given level"""
        window_uuid = str(uuid.uuid4())  # generate a new uuid
        factory = ObjectFactory()  # Use the ObjectFactory to create the new control object
        file_name = os.path.basename(self.main_window.selected_file)
        new_object = factory.create_object(new_object_type, window_uuid=window_uuid,
                                           file_name=file_name)
        if parent_item:
            parent_window = parent_item.data()
            if parent_window.properties.get('WINDOWTYPE') == 'USER':
                if hasattr(parent_window, "children"):
                    parent_window.children.append(new_object)
                else:
                     parent_window.children = [new_object] # add a children to parent that has none
                self.main_window.log_manager.log(f"add_new_control -"
                                                 f" added as child {new_object.properties.get('NAME')},"
                                                 f" to parent: {parent_window.properties.get('NAME')}")

            else: #add as a sibling
                parent = self.model._find_window_parent(self.model.parser_windows, parent_window.window_uuid)
                if parent:
                   index = parent.children.index(parent_window)
                   parent.children.insert(index + 1, new_object)
                   self.main_window.log_manager.log(f"add_new_control -"
                                                    f" added as sibling  {new_object.properties.get('NAME')},"
                                                    f" after: {parent_window.properties.get('NAME')}")
                else:
                    index = self.model.parser_windows.index(parent_window)
                    self.model.parser_windows.insert(index + 1, new_object)
                    self.main_window.log_manager.log(f"add_new_control -"
                                                     f" added to root sibling  {new_object.properties.get('NAME')},"
                                                     f" after: {parent_window.properties.get('NAME')}")
        else:
            self.model.parser_windows.append(new_object)  # add new object as root
            self.main_window.log_manager.log(f"add_new_control - added to root: {new_object.properties.get('NAME')}")
        self.main_window.update_modified_state(True)
        self.update_buttons_state()
        self.model.clear()
        self._populate_tree(self.model.parser_windows, self.model)

    def delete_selected_item(self, item):
        """Remove the selected item from the tree and data source."""
        selected_window = item.data()
        if selected_window:
            if isinstance(self.model.parser_windows, list):
                # Remove the window object, or a child from a list of children
                parent = self.model._find_window_parent(self.model.parser_windows, selected_window.window_uuid)
                if parent:
                    if hasattr(parent, "children"):
                        parent.children.remove(selected_window)
                else:
                    self.model.parser_windows.remove(selected_window)
            self.main_window.update_modified_state(True)
            self.update_buttons_state()
            self.model.clear()
            self._populate_tree(self.model.parser_windows, self.model)
