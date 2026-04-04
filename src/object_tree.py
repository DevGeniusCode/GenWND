import os
import uuid

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QLabel, QPushButton, QMenu, QSizePolicy
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QCursor
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QByteArray, QDataStream, QIODevice

from src.window.window_properties import ObjectFactory
from commands import CommandAddObject, CommandDeleteObject

class ObjectTreeModel(QStandardItemModel):
    """Custom model handling hierarchical WND objects and drag/drop reordering."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.parser_windows = []  # Source of truth array

    def set_parser_windows(self, windows):
        self.parser_windows = windows

    def mimeTypes(self):
        return ['application/x-window-object']

    def mimeData(self, indexes):
        """Serializes the dragged window's UUID into MIME data."""
        if not indexes:
            return None

        item = self.itemFromIndex(indexes[0])
        selected_window = item.data()

        self.main_window.log_manager.log(f"startDrag - selected item: {selected_window.properties.get('NAME')}")

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
        return default_flags | Qt.ItemFlag.ItemIsDropEnabled

    def dropMimeData(self, data, action, row, column, parent):
        """Handles dropping an item and reordering the underlying data structure."""
        if not data.hasFormat('application/x-window-object'):
            return False

        stream = QDataStream(data.data('application/x-window-object'), QIODevice.OpenModeFlag.ReadOnly)
        source_window_uuid = stream.readBytes().decode('utf-8')

        # Determine target drop window
        drop_window = None
        if parent and parent.isValid():
            drop_item = self.itemFromIndex(parent)
            drop_window = drop_item.data()

            if not drop_window:
                self.main_window.log_manager.log("dropEvent - no drop window, adding to root", level="WARNING")
            elif drop_window.properties.get('WINDOWTYPE') != 'USER':
                # Target is not a container, add as sibling
                self.main_window.log_manager.log("dropEvent - target not USER, adding as sibling", level="INFO")
                drop_window = self._find_window_parent(self.parser_windows, drop_window.window_uuid)

        if drop_window:
            self.main_window.log_manager.log(f"dropEvent - dropping into parent: {drop_window.properties.get('NAME')}")
        else:
            self.main_window.log_manager.log("dropEvent - dropping into root")

        self.reorder_windows(source_window_uuid, drop_window, row)

        # Trigger application state update and full tree refresh
        self.main_window.update_modified_state(True)
        self.clear()
        self.main_window.object_tree._populate_tree(self.parser_windows, self)
        return True

    def reorder_windows(self, source_uuid, target_parent, target_row):
        """Moves a window object from its old location to the new parent/index."""
        source_window = self._find_window_by_uuid(self.parser_windows, source_uuid)
        if not source_window:
            self.main_window.log_manager.log(f"reorder_windows - uuid {source_uuid} not found", level="WARNING")
            return

        # 1. Remove from old parent
        old_siblings = self._find_window_parent_children(self.parser_windows, source_uuid)
        if old_siblings and source_window in old_siblings:
            old_siblings.remove(source_window)

            # Clean up empty children arrays on old parent
            if not old_siblings:
                old_parent = self._find_window_parent(self.parser_windows, source_uuid)
                if old_parent and hasattr(old_parent, 'children'):
                    del old_parent.children

        # 2. Add to new target
        if target_parent:
            if not hasattr(target_parent, 'children'):
                target_parent.children = []

            # Prevent index out of bounds on drops at the end of the list
            if target_row < 0 or target_row > len(target_parent.children):
                target_row = len(target_parent.children)

            target_parent.children.insert(target_row, source_window)
        else:
            # Root level insertion
            if target_row < 0 or target_row > len(self.parser_windows):
                target_row = len(self.parser_windows)
            self.parser_windows.insert(target_row, source_window)

    def _find_window_by_uuid(self, windows, window_uuid):
        """Recursively search for a window object by UUID."""
        for window in windows:
            if getattr(window, 'window_uuid', None) == window_uuid:
                return window
            if hasattr(window, 'children'):
                found = self._find_window_by_uuid(window.children, window_uuid)
                if found:
                    return found
        return None

    def _find_window_parent_children(self, windows, window_uuid):
        """Returns the specific list (children array) containing the target UUID."""
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if getattr(child, 'window_uuid', None) == window_uuid:
                        return window.children

                found = self._find_window_parent_children(window.children, window_uuid)
                if found is not None:
                    return found
        return None

    def _find_window_parent(self, windows, window_uuid):
        """Returns the parent object of the target UUID."""
        for window in windows:
            if hasattr(window, 'children'):
                for child in window.children:
                    if getattr(child, 'window_uuid', None) == window_uuid:
                        return window

                found = self._find_window_parent(window.children, window_uuid)
                if found:
                    return found
        return None

    def is_ancestor(self, potential_ancestor, potential_descendant):
        """Check if potential_descendant is a child/grandchild of potential_ancestor to prevent cyclic drops."""
        if potential_ancestor == potential_descendant:
            return True

        def _recursive_check(parent, descendant):
            if hasattr(parent, 'children'):
                for child in parent.children:
                    if child == descendant or _recursive_check(child, descendant):
                        return True
            return False

        return _recursive_check(potential_ancestor, potential_descendant)

    def is_valid_drop(self, event):
        """Validates if the user is attempting a safe drag/drop operation."""
        drop_index = self.main_window.object_tree.tree_view.indexAt(event.position().toPoint())
        drop_item = self.itemFromIndex(drop_index)

        if drop_item:
            drop_window = drop_item.data()
            if drop_window:
                data = event.mimeData().data('application/x-window-object')
                stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
                source_uuid = stream.readBytes().decode('utf-8')
                source_window = self._find_window_by_uuid(self.parser_windows, source_uuid)

                # Prevent dragging containers into themselves
                if source_window and source_window.properties.get('WINDOWTYPE') == 'USER':
                    if self.is_ancestor(source_window, drop_window) or self.is_ancestor(drop_window, source_window):
                        return False
        return True


class ObjectTree(QWidget):
    """The visual hierarchical representation of WND elements."""
    object_selected_signal = pyqtSignal(object)
    visibility_changed_signal = pyqtSignal(str, bool)

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.model = ObjectTreeModel(main_window)
        self.model.setHorizontalHeaderLabels(["Object Tree"])

        self._is_updating_checks = False  # Guard for checkbox recursion

        self._setup_ui()

        # Connect signals
        self.model.itemChanged.connect(self.on_item_changed)
        self.tree_view.selectionModel().selectionChanged.connect(self.on_item_selected)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        self.save_button.clicked.connect(lambda: self.main_window.save_file())
        self.reset_button.clicked.connect(lambda: self.main_window.load_wnd_file(self.main_window.selected_file))

    def _setup_ui(self):
        """Initializes the Tree View, status labels, and buttons."""
        self.layout = QVBoxLayout(self)

        self.empty_label = QLabel("Select a file to display its Windows.", self)
        self.empty_label.setObjectName("emptyStateLabel")  # <-- Added shared style class
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # <-- Fill background
        self.empty_label.setWordWrap(True)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setVisible(False)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setDragDropMode(QTreeView.DragDropMode.InternalMove)
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.save_button = QPushButton("Save to file")
        self.reset_button = QPushButton("Reset from file")
        self.save_button.setVisible(False)
        self.reset_button.setVisible(False)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.reset_button)

        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree_view)
        self.tree_layout.addLayout(self.button_layout)

        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.tree_layout)
        self.layout.setStretch(0, 1)

    def select_item_by_uuid(self, uuid):
        """Recursively search for the item by UUID and visually select it in the tree."""

        def search_item(parent_item):
            for row in range(parent_item.rowCount()):
                child = parent_item.child(row)
                window = child.data()
                if window and getattr(window, 'window_uuid', None) == uuid:
                    return child
                result = search_item(child)
                if result:
                    return result
            return None

        item = search_item(self.model.invisibleRootItem())
        if item:
            self.tree_view.setCurrentIndex(item.index())
            self.tree_view.scrollTo(item.index())

    def load_objects(self, windows):
        """Load the parsed WND data into the tree view."""
        if not windows:
            raise ValueError("Empty or invalid file")

        self.empty_label.setVisible(False)
        self.save_button.setVisible(True)
        self.reset_button.setVisible(True)
        self.tree_view.setVisible(True)
        self.model.set_parser_windows(windows)

        # Build tree without triggering check signals
        self._is_updating_checks = True
        self.model.clear()
        self._populate_tree(windows, self.model)
        self._is_updating_checks = False

    def _populate_tree(self, windows, parent_item):
        """Recursively populates `QStandardItem`s based on object hierarchy."""
        for window in windows:
            label = f"{window.properties.get('WINDOWTYPE')} - {window.properties.get('NAME', 'Unnamed')}"
            item = QStandardItem(label)
            item.setData(window)

            # Setup visibility checkboxes
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Checked)

            parent_item.appendRow(item)
            if hasattr(window, 'children'):
                self._populate_tree(window.children, item)

        self.tree_view.expandAll()

    def on_item_changed(self, item):
        """Triggered when a checkbox in the Object Tree is clicked by the user."""
        if self._is_updating_checks:
            return

        self._is_updating_checks = True
        check_state = item.checkState()
        is_checked = check_state == Qt.CheckState.Checked

        # Update current item canvas visibility
        window = item.data()
        if window and hasattr(window, 'window_uuid'):
            self.visibility_changed_signal.emit(window.window_uuid, is_checked)

        # Update children recursively
        self._update_children_checks(item, check_state)
        self._is_updating_checks = False

    def _update_children_checks(self, parent_item, check_state):
        """Recursively applies the check state to all child items down the tree."""
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)
            child.setCheckState(check_state)

            window = child.data()
            if window and hasattr(window, 'window_uuid'):
                is_checked = check_state == Qt.CheckState.Checked
                self.visibility_changed_signal.emit(window.window_uuid, is_checked)

            self._update_children_checks(child, check_state)

    def on_item_selected(self, selected, deselected):
        """Emit active object to the property editor when clicked in the tree."""
        selected_indexes = self.tree_view.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            self.object_selected_signal.emit(selected_item.data())

    def display_error(self, error_message):
        """Displays parsing errors directly inside the tree view."""
        self.model.clear()
        self.empty_label.setVisible(False)
        self.tree_view.setVisible(True)

        error_item = QStandardItem("Error")
        error_item.setForeground(QColor("red"))
        error_item.setEditable(False)

        error_message_item = QStandardItem(error_message)
        error_message_item.setEditable(False)
        error_item.appendRow(error_message_item)

        self.model.appendRow(error_item)
        self.tree_view.expandAll()

    def clear(self):
        """Resets the tree state when a new folder/file is opened."""
        self.model.clear()
        self.empty_label.setVisible(True)
        self.save_button.setVisible(False)
        self.reset_button.setVisible(False)
        self.tree_view.setVisible(False)

    def update_buttons_state(self):
        """Enables/disables save buttons depending on application modified state."""
        is_modified = getattr(self.main_window, "is_modified", False)
        self.save_button.setEnabled(is_modified)
        self.reset_button.setEnabled(is_modified)

    # --- DRAG EVENT UI FEEDBACK ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object') and self.model.is_valid_drop(event):
            event.acceptProposedAction()
        else:
            event.ignore()
            self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-window-object') and self.model.is_valid_drop(event):
            event.acceptProposedAction()
            self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        else:
            event.ignore()
            self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        super().dragMoveEvent(event)

    def dragLeaveEvent(self, event):
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.tree_view.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().dropEvent(event)

    # --- CONTEXT MENU (Add / Delete) ---
    def show_context_menu(self, position):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        add_menu = menu.addMenu("Add New")

        # Dynamically load control types from factory
        factory = ObjectFactory()
        for object_type in factory.control_classes:
            add_menu.addAction(object_type)

        selected_index = self.tree_view.indexAt(position)
        selected_item = self.model.itemFromIndex(selected_index) if selected_index.isValid() else None

        action = menu.exec(self.tree_view.viewport().mapToGlobal(position))

        if action == delete_action:
            if selected_item:
                self.delete_selected_item(selected_item)
        elif action and action.parent() == add_menu:
            self.add_new_control(selected_item, action.text())

    def add_new_control(self, parent_item, new_object_type):
        """Creates a new WND element and queues an undoable command."""
        factory = ObjectFactory()
        file_name = os.path.basename(self.main_window.selected_file) if self.main_window.selected_file else "Unknown"
        new_object = factory.create_object(
            new_object_type,
            window_uuid=str(uuid.uuid4()),
            file_name=file_name
        )

        parent_uuid = None
        insert_index = 0

        if parent_item:
            parent_window = parent_item.data()
            # If target is a USER container, add as child
            if parent_window.properties.get('WINDOWTYPE') == 'USER':
                parent_uuid = parent_window.window_uuid
                insert_index = len(getattr(parent_window, "children", []))
            else:
                # Add as sibling below the selected item
                parent = self.model._find_window_parent(self.model.parser_windows, parent_window.window_uuid)
                if parent:
                    parent_uuid = parent.window_uuid
                    insert_index = parent.children.index(parent_window) + 1
                else:
                    insert_index = self.model.parser_windows.index(parent_window) + 1
        else:
            insert_index = len(self.model.parser_windows)

        cmd = CommandAddObject(self.main_window, new_object, parent_uuid, insert_index)
        self.main_window.undo_stack.push(cmd)


    def delete_selected_item(self, item):
        """Queues the removal of the active element as an undoable command."""
        selected_window = item.data()
        if not selected_window:
            return

        parent_uuid = None
        insert_index = 0
        parent = self.model._find_window_parent(self.model.parser_windows, selected_window.window_uuid)

        if parent and hasattr(parent, "children"):
            parent_uuid = parent.window_uuid
            insert_index = parent.children.index(selected_window)
        elif selected_window in self.model.parser_windows:
            insert_index = self.model.parser_windows.index(selected_window)

        cmd = CommandDeleteObject(self.main_window, selected_window, parent_uuid, insert_index)
        self.main_window.undo_stack.push(cmd)

    def _refresh_tree_state(self):
        """Triggers a complete model refresh and signals modification to the main window."""
        self.main_window.update_modified_state(True)
        self.model.clear()

        self._is_updating_checks = True
        self._populate_tree(self.model.parser_windows, self.model)
        self._is_updating_checks = False